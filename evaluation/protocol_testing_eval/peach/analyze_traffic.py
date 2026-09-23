"""
Replays traffic.jsonl (written by traffic_recorder.py) through Fandango's parser
and reports the k-path coverage it reaches, in the same format as measure.py.

Each session is replayed message by message, the way ProtocolAlgorithm handles
remote messages: PacketForecaster predicts the expected message nonterminals,
IterativeParser parses the next message against them, the tree is appended to
the session's history and the constraints are checked. A session stops at the
first message that does not parse (or violates a constraint); the prefix parsed
until then counts towards coverage.

Runs inside the <target>-fandango image:
  python3.11 analyze_traffic.py ftp /data/traffic.jsonl --out /data/kpath_coverage.csv
"""
import argparse
import base64
import json
import multiprocessing
import sys
import time
from collections import defaultdict

import fandango.io
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.algorithm import LoggerLevel, SimpleGeneticAlgorithm
from fandango.io.navigation.graph.packetforecaster import PacketForecaster
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.parser.iterative_parser import IterativeParser
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

START = NonTerminal("<start>")

PROTOCOLS = {
    "ftp": {
        "fan": "/home/ubuntu/fandango/ftp_client.fan",
        "parties": {
            ("control", "client"): "ClientControl",
            ("control", "server"): "ServerControl",
            ("data", "client"): "ClientData",
            ("data", "server"): "ServerData",
        },
        "text": True,
    },
    "smtp": {
        "fan": "/home/ubuntu/fandango/smtp_client.fan",
        "parties": {("smtp", "client"): "Client", ("smtp", "server"): "Server"},
        "text": True,
    },
    "dns": {
        "fan": "/home/ubuntu/fandango/dns_client.fan",
        "parties": {("dns", "client"): "Client", ("dns", "server"): "Server"},
        "text": False,
    },
}

# ftp_client.fan: data socket closes and the TLS upgrade are messages of the helper parties.
CLOSE_DATA = "999 Data socket closed.\r\n"
AUTH_TLS_NEGOTIATE = "998 TLS upgrade.\r\n"

WAIT, FAIL = "wait", "fail"
BEAM = 16


class Replayer:
    def __init__(self, protocol, fan, k, check_constraints):
        fandango.io.UdpTcpProtocolImplementation.start = lambda self: None
        with open(fan) as f:
            self.grammar, constraints = parse(f, use_stdlib=True)
        self.protocol = protocol
        self.k = k
        self.forecaster = PacketForecaster(self.grammar)
        self.model = ProtocolModel(self.grammar, START)
        self.evaluator = None
        if check_constraints:
            self.evaluator = SimpleGeneticAlgorithm(
                grammar=self.grammar, constraints=constraints, logger_level=LoggerLevel.ERROR
            ).evaluator
        env, _ = self.grammar.get_spec_env()
        self.decompress = env.get("decompress_msg") if protocol == "dns" else None

    def satisfies_constraints(self, tree):
        if self.evaluator is None:
            return True
        _, (fitness, _, _) = GeneratorWithReturn(self.evaluator.evaluate_individual(tree)).collect()
        return fitness >= 1.0

    def longest_complete_prefix(self, nt, hookin_point, buf):
        """(consumed, tree) of the longest prefix of buf that parses as nt, and whether
        the parser could still continue after the whole buffer."""
        parser = IterativeParser(self.grammar.rules)
        parser.new_parse(start=nt, mode=ParsingMode.COMPLETE, hookin_parent=hookin_point)
        tree = self.complete_tree(parser, buf)
        if tree is not None:
            return len(buf), tree, False
        can_continue = parser.can_continue()
        # Regex terminals match maximally when a fragment is consumed at once
        # ('USER webadmin\r\n' as <word> swallows the \r\n), but not when it is fed
        # piecewise, so the buffer is fed char by char as well.
        parser = IterativeParser(self.grammar.rules)
        parser.new_parse(start=nt, mode=ParsingMode.COMPLETE, hookin_parent=hookin_point)
        best = (0, None)
        for idx in range(len(buf)):
            tree = self.complete_tree(parser, buf[idx:idx + 1])
            if tree is not None:
                best = (idx + 1, tree)
            if not parser.can_continue():
                break
        return best[0], best[1], can_continue and best[1] is None

    @staticmethod
    def complete_tree(parser, fragment):
        """Consume fragment; a complete derivation if there is one among the parses
        (a message like 'USER x\\r\\n' can also be the prefix of a longer <word>)."""
        for tree, complete in parser.consume(fragment):
            if complete:
                return parser.collapse(tree)
        return None

    def parse_next(self, history, party, buf):
        """Parse the next message of party from buf into history.
        Returns the readings [(new_history, consumed)], WAIT (buf is an incomplete
        message or party is not expected yet) or FAIL."""
        forecast = self.forecaster.predict(history)
        if party not in forecast.get_msg_parties():
            return WAIT
        packets = forecast[party]
        candidates = []
        can_continue = False
        # Whether a message parses can depend on the hook-in point (parse_next_remote_packet
        # picks one at random), so every mounting path is tried and the tree is mounted
        # at the path it was parsed at.
        for nt in packets.get_non_terminals():
            packet = packets[nt]
            for option in sorted(packet.paths, key=repr):
                path = [step[0] for step in option.path if not step[1]]
                hookin_point = option.tree.get_last_by_path(path)
                consumed, tree, cont = self.longest_complete_prefix(nt, hookin_point, buf)
                can_continue |= cont
                if tree is None:
                    continue
                tree.sender = packet.node.sender
                tree.recipient = packet.node.recipient
                try:
                    self.grammar.populate_sources(tree)
                except Exception:
                    continue
                candidates.append((consumed, option, tree))
        readings = []
        seen = set()
        for consumed, option, tree in candidates:
            new_history = option.tree.deepcopy(copy_parent=False)
            new_history.append(option.path[1:-1], tree.deepcopy(copy_parent=False))
            key = (hash(new_history), consumed)
            if key in seen:
                continue
            seen.add(key)
            if self.satisfies_constraints(new_history):
                readings.append((new_history, consumed))
        if readings:
            return readings
        if candidates:
            return FAIL
        return WAIT if can_continue else FAIL

    def drain(self, hypothesis):
        """Parse as many pending messages as possible. A message with several readings
        (e.g. 'AUTH PLAIN <b64>' as correct or incorrect login) forks the hypothesis;
        later messages decide which reading survives.
        Returns (waiting hypotheses, failed hypotheses)."""
        waiting, failed = [], []
        stack = [hypothesis]
        while stack:
            history, pending, parsed = stack.pop()
            for party, buf in pending.items():
                result = self.parse_next(history, party, buf)
                if result == WAIT:
                    continue
                if result == FAIL:
                    failed.append((history, pending, parsed))
                    break
                for new_history, consumed in result:
                    rest = dict(pending)
                    if buf[consumed:]:
                        rest[party] = buf[consumed:]
                    else:
                        del rest[party]
                    stack.append((new_history, rest, parsed + 1))
                break
            else:
                waiting.append((history, pending, parsed))
        return waiting, failed

    def replay(self, units):
        """units: [(party, payload)] in time order. Returns (tree, parsed messages, complete)
        of the reading that parses furthest."""
        alive = [(DerivationTree(START), {}, 0)]
        dead = []
        for party, payload in units:
            next_alive = []
            for history, pending, parsed in alive:
                pending = dict(pending)
                pending[party] = pending.get(party, payload[:0]) + payload
                waiting, failed = self.drain((history, pending, parsed))
                next_alive += waiting
                dead += failed
            if not next_alive:
                alive = []
                break
            next_alive.sort(key=lambda h: -h[2])
            alive = next_alive[:BEAM]
        for history, pending, parsed in alive:
            if not pending and len(self.forecaster.predict(history).get_msg_parties()) == 0:
                return history, parsed, True
        history, _, parsed = max(alive + dead, key=lambda h: h[2])
        return history, parsed, False

    def covered(self, tree):
        covered = defaultdict(set)
        for symbol, subtrees in self.model.group_messages_by_nt([tree]).items():
            for subtree in subtrees:
                for path in self.grammar._extract_k_paths_from_tree(subtree, self.k, False, alt_cache=True):
                    covered[symbol.name()].add(path_key(path))
        return covered


def path_key(path):
    return tuple(f"{type(s).__name__}:{s}" for s in path)


def load_records(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    records.sort(key=lambda r: r["time"])
    return records


def build_sessions(protocol, records):
    """Split the records into sessions: [(end_time, [(time, channel, sender, payload)])]."""
    if protocol == "dns":
        sessions = []
        current = {}
        for r in records:
            if r["event"] != "data":
                continue
            item = (r["time"], r["channel"], r["sender"], base64.b64decode(r["data"]))
            if r["sender"] == "client":
                current[r["conn"]] = [item]
                sessions.append(current[r["conn"]])
            elif r["conn"] in current:
                current[r["conn"]].append(item)
        return [(s[-1][0], s) for s in sessions]

    main_channel = "control" if protocol == "ftp" else "smtp"
    sessions = {}
    session_order = []
    data_owner = {}
    data_closed = set()
    last_session = None
    for r in records:
        conn, channel = r["conn"], r["channel"]
        if channel == main_channel:
            if r["event"] == "open":
                sessions[conn] = []
                session_order.append(conn)
                last_session = conn
            elif r["event"] == "data" and conn in sessions:
                sessions[conn].append((r["time"], channel, r["sender"], base64.b64decode(r["data"])))
            continue
        if r["event"] == "open":
            data_owner[conn] = last_session
            continue
        owner = data_owner.get(conn)
        if owner is None:
            continue
        if r["event"] == "data":
            sessions[owner].append((r["time"], channel, r["sender"], base64.b64decode(r["data"])))
        elif r["event"] == "close" and conn not in data_closed:
            data_closed.add(conn)
            closer = "SocketControlServer" if r["sender"] == "server" else "SocketControlClient"
            sessions[owner].append((r["time"], "helper", closer, CLOSE_DATA.encode()))
    return [(sessions[c][-1][0], sessions[c]) for c in session_order if sessions[c]]


def to_units(spec, events, decompress):
    """Decode the chunks like the .fan parties do and merge consecutive chunks of one party.
    An undecodable text chunk ends the session, as the fandango party would drop it."""
    units = []
    for _, channel, sender, payload in events:
        party = sender if channel == "helper" else spec["parties"][(channel, sender)]
        if decompress is not None:
            try:
                payload = decompress(payload)
            except Exception:
                pass
            units.append((party, payload))
            continue
        try:
            payload = payload.decode("utf-8")
        except UnicodeDecodeError:
            break
        if units and units[-1][0] == party:
            units[-1] = (party, units[-1][1] + payload)
        else:
            units.append((party, payload))
        if party == "ServerControl" and any(line.startswith("234") for line in payload.split("\r\n")):
            units.append(("SocketControlClient", AUTH_TLS_NEGOTIATE))
    return units


_replayer = None
_spec = None


def _init_worker(protocol, fan, k, check_constraints):
    global _replayer, _spec
    if _replayer is not None:
        return
    sys.setrecursionlimit(10**6)
    _spec = PROTOCOLS[protocol]
    _replayer = Replayer(protocol, fan, k, check_constraints)


def _analyze(session):
    end_time, events = session
    units = to_units(_spec, events, _replayer.decompress)
    try:
        tree, parsed, complete = _replayer.replay(units)
        covered = _replayer.covered(tree)
    except Exception as e:
        return end_time, 0, False, {}, repr(e)
    return end_time, parsed, complete, covered, None


def coverage_row(replayer, covered_by_symbol):
    """Mirrors CoverageTracker.coverage_trees(overlap_to_root=False)."""
    roles_by_symbol = defaultdict(set)
    roles = {"all_party"}
    for pnt in replayer.grammar.get_protocol_messages(START):
        roles.add(pnt.sender)
        roles_by_symbol[pnt.symbol].update({pnt.sender, "all_party"})
    by_role = {r: {"covered": 0, "all": 0, "covered_unique": set(), "all_unique": set()} for r in roles}
    row = {}
    for symbol in replayer.model.state_grammar_symbols:
        all_paths = {path_key(p) for p in replayer.grammar.generate_all_k_paths(
            k=replayer.k, non_terminal=symbol, overlap_to_root=False, alt_cache=True)}
        covered = covered_by_symbol.get(symbol.name(), set())
        for role in roles_by_symbol.get(symbol, ()):
            by_role[role]["all"] += len(all_paths)
            by_role[role]["all_unique"] |= all_paths
            by_role[role]["covered"] += len(covered)
            by_role[role]["covered_unique"] |= covered
        row[symbol.name()] = (len(covered), len(all_paths))
    for role, paths in by_role.items():
        row[f"__role_{role}"] = (paths["covered"], paths["all"])
        row[f"__role_unique_{role}"] = (len(paths["covered_unique"]), len(paths["all_unique"]))
    return row


def write_log(path, log):
    symbols = sorted({s for _, coverage in log for s in coverage})
    with open(path, "w") as f:
        f.write("time," + ",".join(f"covered_{s},total_{s},percent_{s}" for s in symbols) + "\n")
        for timestamp, coverage in log:
            cells = [f"{timestamp:.1f}"]
            for s in symbols:
                covered, total = coverage.get(s, (0, 0))
                cells.append(f"{covered},{total},{covered / total if total else 0}")
            f.write(",".join(cells) + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("protocol", choices=sorted(PROTOCOLS))
    p.add_argument("traffic")
    p.add_argument("--out", default="kpath_coverage.csv")
    p.add_argument("--fan", help="client .fan (default: the one of the fandango runs)")
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--interval", type=float, default=60.0, help="seconds between coverage rows")
    p.add_argument("--no-constraints", action="store_true")
    p.add_argument("--workers", type=int, default=min(8, multiprocessing.cpu_count()))
    p.add_argument("--sessions-per-worker", type=int, default=20,
                   help="restart workers after this many sessions; bounds fandango's caches")
    args = p.parse_args()

    fan = args.fan or PROTOCOLS[args.protocol]["fan"]
    records = load_records(args.traffic)
    if not records:
        sys.exit("no records")
    start = records[0]["time"]
    sessions = sorted(build_sessions(args.protocol, records), key=lambda s: s[0])
    print(f"{len(records)} records, {len(sessions)} sessions")

    init_args = (args.protocol, fan, args.k, not args.no_constraints)
    _init_worker(*init_args)
    covered_by_symbol = defaultdict(set)
    log = []
    next_row = args.interval
    stats = {"sessions": 0, "complete": 0, "messages": 0, "errors": 0}
    began = time.time()
    with multiprocessing.get_context("fork").Pool(
        args.workers, _init_worker, init_args, maxtasksperchild=args.sessions_per_worker
    ) as pool:
        for end_time, parsed, complete, covered, error in pool.imap(_analyze, sessions, chunksize=1):
            while end_time - start >= next_row:
                log.append((next_row, coverage_row(_replayer, covered_by_symbol)))
                write_log(args.out, log)
                row = log[-1][1].get(START.name(), (0, 0))
                print(f"  t={next_row:.0f}s: {START.name()} {row[0]}/{row[1]}", flush=True)
                next_row += args.interval
            if stats["sessions"] % 50 == 0:
                print(f"{stats['sessions']}/{len(sessions)} sessions after {time.time() - began:.0f}s", flush=True)
            stats["sessions"] += 1
            stats["complete"] += complete
            stats["messages"] += parsed
            stats["errors"] += error is not None
            for symbol, paths in covered.items():
                covered_by_symbol[symbol] |= paths
    log.append((sessions[-1][0] - start, coverage_row(_replayer, covered_by_symbol)))
    write_log(args.out, log)

    final = log[-1][1]
    whole = final.get(START.name(), (0, 0))
    per_message = final.get("__role_unique_all_party", (0, 0))
    print(f"sessions: {stats['sessions']}, fully parsed: {stats['complete']}, "
          f"parsed messages: {stats['messages']}, errors: {stats['errors']}")
    print(f"k-path coverage of {START.name()} (k={args.k}): {whole[0]}/{whole[1]}")
    print(f"k-path coverage below message/state symbols (__role_unique_all_party): {per_message[0]}/{per_message[1]}")
    print(f"written: {args.out}")


if __name__ == "__main__":
    main()
