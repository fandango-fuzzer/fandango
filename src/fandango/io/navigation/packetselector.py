import enum
from typing import Optional

from fandango.io import FandangoIO
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.stategrammarconverter import StateGrammarConverter
from fandango.io.navigation.powerschedule import (
    PowerScheduleCoverage,
    PowerScheduleKPath,
)
from fandango.language.tree import DerivationTree
from fandango.io.navigation.packetforecaster import (
    ForecastingPacket,
    PacketForecaster,
    ForecastingResult,
)
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal, Symbol
from fandango.logger import log_guidance_hint

class CoverageGoal(enum.Enum):
    INPUTS = 0
    STATE_INPUTS = 1
    STATE_INPUTS_OUTPUTS = 2

class PacketSelector:
    def __init__(
        self,
        grammar: Grammar,
        io_instance: FandangoIO,
        history_tree: DerivationTree,
        diversity_k: int,
    ):
        self.start_symbol = NonTerminal("<start>")
        self.coverage_goal = CoverageGoal.STATE_INPUTS_OUTPUTS
        self.grammar = grammar
        self.state_grammar_symbols = self._get_state_grammar_symbols(self.start_symbol)
        self.k_path_starters = self.compute_k_path_starters(self.coverage_goal)
        self.msg_power_schedule = PowerScheduleCoverage()
        self.state_path_power_schedule = PowerScheduleKPath()
        self.io_instance = io_instance
        self.navigator = PacketNavigator(grammar, self.start_symbol)
        self.forecaster = PacketForecaster(self.grammar)
        self.diversity_k = diversity_k
        self.parst_derivations: list[DerivationTree] = []
        self.prev_past_derivations_len = 0
        self.history_tree: DerivationTree = DerivationTree(NonTerminal("<start>"))
        self.max_messages_per_tree = 200
        self._forecasting_result: Optional[ForecastingResult] = None
        self._next_packets: Optional[list[ForecastingPacket]] = None
        self._coverage_scores: Optional[list[tuple[NonTerminal, float]]] = None
        self._prev_session_msgs: list[DerivationTree] = []
        self._guide_to_end = False
        self._guide_target: Optional[tuple[NonTerminal, ...]] = None
        self._guide_path: Optional[list[PacketNonTerminal | NonTerminal | None]] = None
        self._current_covered_k_paths: set[KPath] = set()
        self._all_past_covered_k_paths: set[KPath] = set()
        self.compute(history_tree, self.parst_derivations)

    def _get_state_grammar_symbols(self, starting_symbol: NonTerminal):
        state_grammar = StateGrammarConverter(self.grammar.grammar_settings).process(
            self.grammar.rules, starting_symbol
        )
        symbols = set(state_grammar.keys())
        symbols.update(
            map(lambda x: x.symbol, self.grammar.get_protocol_messages(starting_symbol))
        )
        symbols = set(filter(lambda x: x in self.grammar.rules, symbols))
        return symbols

    def _group_messages_by_nt(
        self,
        trees: list[DerivationTree],
        non_terminals: Optional[set[NonTerminal]] = None,
    ):
        if non_terminals is None:
            non_terminals = self.state_grammar_symbols
        messages: list[DerivationTree] = []
        for tree in trees:
            for subtree in tree.flatten():
                if subtree.symbol in non_terminals:
                    messages.append(subtree)
        messages_by_nt: dict[NonTerminal, list[DerivationTree]] = {}
        for msg in messages:
            assert isinstance(msg.symbol, NonTerminal)
            messages_by_nt.setdefault(msg.symbol, []).append(msg)
        return messages_by_nt

    @staticmethod
    def _tuple_contains(sub: tuple, full: tuple) -> bool:
        n, m = len(sub), len(full)
        if n == 0:
            return True
        for i in range(m - n + 1):
            if full[i : i + n] == sub:
                return True
        return False

    def _compute_coverage_score(
        self, k: int, overlap_to_root: bool = False
    ) -> list[tuple[NonTerminal, float]]:
        """
        Computes the coverage score for each NonTerminal in the given DerivationTrees.
        The score is the ratio of the number of trees containing the NonTerminal to the total number of trees.

        :param trees: List of DerivationTrees to analyze.
        :param k: The k-path length for coverage computation.
        :return: Dictionary mapping NonTerminals to their coverage scores.
        """
        messages_by_nt = self._group_messages_by_nt(self._all_derivation_trees())
        nt_coverage = {}
        for symbol in self.state_grammar_symbols:
            if symbol not in messages_by_nt:
                nt_coverage[symbol] = 0.0
                continue
            nt_coverage[symbol] = self.grammar.compute_kpath_coverage(
                messages_by_nt[symbol], k, symbol, overlap_to_root
            )
        nt_coverage_list = list(
            sorted(nt_coverage.items(), key=lambda x: (x[1], x[0].name()))
        )
        return nt_coverage_list

    def _get_guide_to_end_packet(self) -> list[ForecastingPacket]:
        path = self.navigator.astar_search_end(
            self.history_tree, included_k_paths=self._current_covered_k_paths
        )
        if path is None:
            return []
        if len(path) > 0:
            next_packet = next(
                filter(lambda x: isinstance(x, PacketNonTerminal), path), None
            )
            if next_packet is None:
                return []
            assert isinstance(next_packet, PacketNonTerminal)
            return self.find_packets(
                sender=next_packet.sender, packet_symbol=next_packet.symbol
            )
        return []

    def compute(
        self, history_tree: DerivationTree, parst_derivations: list[DerivationTree]
    ):
        self.history_tree = history_tree
        self.parst_derivations = parst_derivations
        self._forecasting_result = None
        self._coverage_scores = None
        self._next_packets = None

    @property
    def forecasting_result(self) -> ForecastingResult:
        if self._forecasting_result is None:
            self._forecasting_result = self.forecaster.predict(self.history_tree)
        return self._forecasting_result

    @property
    def coverage_scores(
        self,
    ) -> list[tuple[NonTerminal, float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_coverage_score(self.diversity_k)
        return self._coverage_scores

    @property
    def next_packets(self) -> list[ForecastingPacket]:
        if self._next_packets is None:
            self._next_packets = self._select_next_packet()
        return self._next_packets

    def is_guide_to_end(self) -> bool:
        if self._next_packets is None:
            self._next_packets = self._select_next_packet()
        return self._guide_to_end

    def is_complete(self) -> bool:
        assert self.forecasting_result is not None
        return len(self.forecasting_result.complete_trees) != 0

    def next_fuzzer_parties(self) -> list[str]:
        assert self.forecasting_result is not None
        return list(
            filter(
                lambda x: self.io_instance.parties[x].is_fuzzer_controlled(),
                self.forecasting_result.get_msg_parties(),
            )
        )

    def get_fuzzer_packets(self):
        assert self.forecasting_result is not None
        return [
            packet
            for sender in self.next_fuzzer_parties()
            for packet in self.forecasting_result.parties_to_packets[
                sender
            ].nt_to_packet.values()
        ]

    def next_external_parties(self) -> list[str]:
        assert self.forecasting_result is not None
        return list(
            filter(
                lambda x: not self.io_instance.parties[x].is_fuzzer_controlled(),
                self.forecasting_result.get_msg_parties(),
            )
        )

    def get_next_parties(self) -> list[str]:
        return list(self.forecasting_result.get_msg_parties())

    def _all_derivation_trees(self):
        all_derivation_trees = list(self.parst_derivations)
        all_derivation_trees.append(self.history_tree)
        return all_derivation_trees

    def _uncovered_paths(self):
        return self.grammar.get_uncovered_k_paths(
            self._all_derivation_trees(), self.diversity_k, self.start_symbol
        )

    def _select_next_target(self) -> tuple[NonTerminal, ...]:
        uncovered_paths = self._uncovered_paths()
        for list_idx, path in enumerate(list(uncovered_paths)):
            remaining_path = path
            for path_idx, symbol in enumerate(path[::-1]):
                if symbol in self.state_grammar_symbols:
                    break
                last_idx = len(path) - path_idx - 1
                remaining_path = remaining_path[:last_idx]
            uncovered_paths[list_idx] = remaining_path
        uncovered_paths = list(filter(lambda x: len(x) > 0, uncovered_paths))
        if len(uncovered_paths) == 0:
            protocol_msgs = self.grammar.get_protocol_messages(self.start_symbol)
            message_nts = set(map(lambda x: x.symbol, protocol_msgs))
            message_coverage = dict(
                filter(lambda x: x[0] in message_nts, self.coverage_scores)
            )
            m_ps = self.msg_power_schedule
            m_ps.assign_energy_coverage(message_coverage)
            target = m_ps.choose()
            m_ps.add_past_target(target)
            return target
        s_ps = self.state_path_power_schedule
        s_ps.assign_energy_k_path(uncovered_paths)
        selected_path = s_ps.choose()
        s_ps.add_past_target(selected_path)
        return selected_path

    def _is_tree_contains_paths(
        self, paths: set[tuple[Symbol, ...]], tree: DerivationTree
    ) -> bool:
        found_trees, include_k_paths = self.navigator._find_trees_including_k_paths(
            paths, tree
        )
        return include_k_paths

    def _confirm_covered_path(self, path: tuple[Symbol, ...]):
        self._current_covered_k_paths.add(path)
        self._all_past_covered_k_paths.add(path)

    def _remember_messages(self):
        if self.history_tree is None:
            self._prev_session_msgs = []
            return
        self._prev_session_msgs = list(
            map(lambda x: x.msg, self.history_tree.protocol_msgs())
        )

    def _new_msgs(self, is_new_tree: bool) -> list[DerivationTree]:
        prev_msgs = []
        if is_new_tree:
            prev_msgs = list(
                map(lambda x: x.msg, self.parst_derivations[-1].protocol_msgs())
            )
        current_session_msgs = list(
            map(lambda x: x.msg, self.history_tree.protocol_msgs())
        )
        all_current_msgs = prev_msgs + current_session_msgs
        new_msgs = []
        for prev, new in zip(self._prev_session_msgs, all_current_msgs):
            if prev != new:
                new_msgs.extend(current_session_msgs)
                return new_msgs
        if len(all_current_msgs) > len(self._prev_session_msgs):
            return all_current_msgs[len(self._prev_session_msgs) :]
        return new_msgs

    def _get_next_packet(self):
        if self._guide_path is None:
            return None
        return next(
            (x for x in self._guide_path if isinstance(x, PacketNonTerminal)), None
        )

    def _select_next_packet(self) -> list[ForecastingPacket]:
        if len(self.next_fuzzer_parties()) == 0:
            return []

        is_new_tree = len(self.parst_derivations) > self.prev_past_derivations_len
        if is_new_tree:
            self._current_covered_k_paths.clear()
        self.prev_past_derivations_len = len(self.parst_derivations)

        self._guide_to_end = False
        if (
            len(self.history_tree.protocol_msgs()) > self.max_messages_per_tree
            or len(self._uncovered_paths()) == 0
        ):
            if len(self._uncovered_paths()) == 0:
                log_guidance_hint("Full coverage reached. Guiding to end of tree.")
                if self._guide_target is not None:
                    self._confirm_covered_path(self._guide_target)
            else:
                log_guidance_hint(
                    f"Current tree contains more then {self.max_messages_per_tree} messages. Guiding to end of tree."
                )
            self._guide_to_end = True
            return self._get_guide_to_end_packet()

        left_path = True
        if self._guide_path is not None:
            left_path = False
            for msg in self._new_msgs(is_new_tree):
                old_next_packet = self._get_next_packet()
                if old_next_packet is None or old_next_packet.symbol != msg.symbol:
                    left_path = True
                    break
                self._guide_path = self._guide_path[
                    self._guide_path.index(old_next_packet) + 1 :
                ]

        if self._guide_target is None or len(self._guide_path) == 0 or left_path:
            if self._guide_target is not None:
                should_covered_paths = self._current_covered_k_paths.union(
                    [self._guide_target]
                )
                if self._is_tree_contains_paths(
                    should_covered_paths, self.history_tree
                ):
                    self._confirm_covered_path(self._guide_target)

            self._guide_target = self._select_next_target()
            found_guide_path = self.navigator.astar_tree_including_k_paths(
                tree=self.history_tree,
                destination_k_path=self._guide_target,
                included_k_paths=self._current_covered_k_paths,
            )
            assert found_guide_path is not None
            self._guide_path = found_guide_path
        self._guide_to_end = (
            len(list(filter(lambda p: p is None, self._guide_path))) > 0
        )
        selected_packets = []
        next_packet = self._get_next_packet()
        hookin_states: Optional[list[Symbol]] = None
        if next_packet is not None:
            assert self._guide_path is not None
            packet_idx = self._guide_path.index(next_packet)
            hookin_states = []
            for symbol in self._guide_path[:packet_idx]:
                assert isinstance(symbol, Symbol)
                hookin_states.append(symbol)
            packet_sender = next_packet.sender
            packet_symbol = next_packet.symbol
        else:
            if self._guide_path is not None:
                hookin_states = []
                for symbol in self._guide_path:
                    assert isinstance(symbol, Symbol)
                    hookin_states.append(symbol)
            packet_sender = None
            packet_symbol = None

        selected_packets.extend(
            self.find_packets(
                sender=packet_sender,
                hookin_states=hookin_states,
                packet_symbol=packet_symbol,
            )
        )

        if len(selected_packets) == 0:
            selected_packets.extend(self.get_fuzzer_packets())
        self._remember_messages()
        return selected_packets

    def find_packets(
        self,
        *,
        sender: Optional[str] = None,
        hookin_states: Optional[list[Symbol]] = None,
        packet_symbol: Optional[NonTerminal] = None,
    ) -> list[ForecastingPacket]:
        packets = []
        hookin_states_tp: tuple[Symbol, ...] = tuple()
        if hookin_states is not None:
            hookin_states_tp = tuple(hookin_states)

        for current_sender in self.next_fuzzer_parties():
            if sender is not None and current_sender != sender:
                continue
            for packet in self.forecasting_result[current_sender].nt_to_packet.values():
                if packet_symbol is not None and packet.node.symbol != packet_symbol:
                    continue
                append_packet = ForecastingPacket(packet.node)
                for hookin_path in packet.paths:
                    if not self._is_tree_contains_paths(
                        self._current_covered_k_paths, hookin_path.tree
                    ):
                        continue
                    packet_hookin_states = tuple(
                        map(lambda y: y[0], filter(lambda x: x[1], hookin_path.path))
                    )
                    if not PacketSelector._tuple_contains(
                        hookin_states_tp, packet_hookin_states
                    ):
                        continue
                    append_packet.paths.add(hookin_path)
                if len(append_packet.paths) != 0:
                    packets.append(append_packet)
        return packets

    def coverage_percent(self) -> float:
        u_paths = self._uncovered_paths()
        if len(u_paths) == 0:
            return 1.0
        all_paths = self.grammar.compute_k_paths(self.diversity_k)
        if len(all_paths) == 0:
            return 1.0
        return 1.0 - (len(u_paths) / len(all_paths))

    def _compute_coverage_trees(
        self, overlap_to_root: bool = False
    ) -> dict[NonTerminal, tuple[int, int]]:
        messages_by_nt = self._group_messages_by_nt(self._all_derivation_trees())
        paths_by_role = {}
        roles_by_symbol = dict()
        paths_by_role["all_party"] = {
            "covered": list(),
            "covered_unique": set(),
            "all": list(),
            "all_unique": set(),
            "symbols": set(),
        }
        for p_nt in self.grammar.get_protocol_messages(self.start_symbol):
            if p_nt.sender not in paths_by_role:
                paths_by_role[p_nt.sender] = {
                    "covered": list(),
                    "covered_unique": set(),
                    "all": list(),
                    "all_unique": set(),
                    "symbols": set(),
                }
            paths_by_role[p_nt.sender]["symbols"].add(p_nt.symbol)
            paths_by_role["all_party"]["symbols"].add(p_nt.symbol)
            roles_by_symbol.setdefault(p_nt.symbol, set()).add(p_nt.sender)
            roles_by_symbol[p_nt.symbol].add("all_party")

        nt_coverage = {}
        for symbol in self.state_grammar_symbols:
            all_k_paths = self.grammar.generate_all_k_paths(
                self.diversity_k, symbol, overlap_to_root
            )

            covered_k_paths = set()
            if symbol in messages_by_nt:
                for tree in messages_by_nt[symbol]:
                    covered_k_paths.update(
                        self.grammar._extract_k_paths_from_tree(
                            tree, self.diversity_k, overlap_to_root
                        )
                    )
            if symbol in roles_by_symbol:
                for role in roles_by_symbol[symbol]:
                    paths_by_role[role]["all"].extend(all_k_paths)
                    paths_by_role[role]["all_unique"].update(all_k_paths)
                    paths_by_role[role]["covered"].extend(covered_k_paths)
                    paths_by_role[role]["covered_unique"].update(covered_k_paths)
            nt_coverage[symbol] = (len(covered_k_paths), len(all_k_paths))
        for role, paths in paths_by_role.items():
            nt_coverage[NonTerminal("__role_" + role)] = (
                len(paths["covered"]),
                len(paths["all"]),
            )
            nt_coverage[NonTerminal("__role_unique_" + role)] = (
                len(paths["covered_unique"]),
                len(paths["all_unique"]),
            )
        return nt_coverage

    def set_coverage_goal(self, goal: CoverageGoal):
        self.coverage_goal = goal
        self.k_path_starters = self.compute_k_path_starters(self.coverage_goal)

    def compute_k_path_starters(self, coverage_goal: CoverageGoal) -> set[NonTerminal]:
        input_starters = set()
        output_starters = set()
        state_starters = set()
        p_nts = self.grammar.get_protocol_messages(self.start_symbol)
        for p_nt in p_nts:
            msg_starters = self.grammar[p_nt.symbol].descendents(self.grammar, filter_controlflow=True)
            if self.io_instance.parties[p_nt.sender].is_fuzzer_controlled():
                input_starters.add(p_nt.symbol)
                input_starters.update(msg_starters)
            else:
                output_starters.add(p_nt.symbol)
                input_starters.update(msg_starters)
        for nt in self.state_grammar_symbols:
            if nt not in input_starters and nt not in output_starters:
                state_starters.add(nt)

        starters = set()
        if coverage_goal == CoverageGoal.INPUTS:
            starters.update(input_starters)
        elif coverage_goal == CoverageGoal.STATE_INPUTS:
            starters.update(input_starters)
            starters.update(state_starters)
        elif coverage_goal == CoverageGoal.STATE_INPUTS_OUTPUTS:
            starters.update(input_starters)
            starters.update(output_starters)
            starters.update(state_starters)
        return starters