"""Measurement runs for the experiments. The target's driver always calls run();
the --experiment argument decides what happens:

  (no --experiment)         run Fandango normally (guidance on, stop at full
                            grammar coverage, no measurement output).
  --experiment throughput   same, but never stop early -- keep generating for the
                            whole --duration, then dump input/output/tree counts.
  --experiment coverage     guidance per --guidance, log grammar coverage every
                            --interval steps, stop at 100% coverage, --duration,
                            or (if --plateau-timeout > 0) once start-symbol
                            coverage stops rising for that many seconds.
"""
import argparse
import signal
import time

from fandango.language.grammar import FuzzingMode

# Transport/timer parties, not protocol messages.
PLUMBING = {"SocketControlServer", "SocketControlClient", "StdOut"}


class _Deadline(BaseException):
    pass


def _deadline(signum, frame):
    raise _Deadline


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("grammar", nargs="?")
    p.add_argument("--experiment", choices=["throughput", "coverage"])
    p.add_argument("--duration", type=float, default=3600)
    p.add_argument("--guidance", type=int, default=1)
    p.add_argument("--interval", type=int, default=20)
    p.add_argument("--out-dir", default=".")
    p.add_argument("--run-id", default="1")
    p.add_argument("--plateau-timeout", type=float, default=0.0)
    return p.parse_args()


def run(fandango, args, max_generations=None):
    if args.experiment == "throughput":
        # keep generating for the whole --duration, don't stop at full coverage
        fandango.stop_on_full_coverage = False
        fandango.enable_guidance(True)
    elif args.experiment == "coverage":
        fandango.coverage_log_interval = args.interval
        fandango.stop_on_full_coverage = True
        fandango.enable_guidance(bool(args.guidance))
        fandango.coverage_plateau_timeout = args.plateau_timeout

    tally = {"inputs": 0, "outputs": 0, "trees": 0}

    start = time.time()
    if args.experiment:
        signal.signal(signal.SIGALRM, _deadline)
        signal.signal(signal.SIGTERM, _deadline)
        signal.alarm(int(args.duration))
    try:
        for tree in fandango.generate(mode=FuzzingMode.IO, max_generations=max_generations):
            _tally_messages(fandango, tree, tally)
            if args.experiment and time.time() - start >= args.duration:
                break
    except _Deadline:
        pass
    finally:
        if args.experiment:
            signal.alarm(0)
        if args.experiment == "throughput":
            _tally_messages(fandango, fandango._protocol_tree, tally)  # in-progress run
            write_throughput(fandango, args, start, tally)
        elif args.experiment == "coverage":
            write_coverage(fandango, args, start)


def _tally_messages(fandango, tree, tally):
    """Add a derivation tree's protocol messages to the running input/output tally."""
    tally["trees"] += 1
    for msg in tree.protocol_msgs():
        if msg.sender in PLUMBING:
            continue
        if fandango._io_instance.parties[msg.sender].is_fuzzer_controlled():
            tally["inputs"] += 1
        else:
            tally["outputs"] += 1


def write_throughput(fandango, args, start, tally):
    grammar_coverage = fandango._packet_selector.coverage_percent(alt_cache=True) * 100
    with open(f"{args.out_dir}/throughput_{args.run_id}.txt", "w") as f:
        f.write(f"input messages:   {tally['inputs']}\n")
        f.write(f"output messages:  {tally['outputs']}\n")
        f.write(f"derivation trees: {tally['trees']}\n")
        f.write(f"time:             {time.time() - start:.1f}s\n")
        f.write(f"grammar coverage: {grammar_coverage:.2f}%\n")


def write_coverage(fandango, args, start):
    write_log(f"{args.out_dir}/coverage_{args.run_id}.csv", start, fandango.coverage_log)
    write_log(f"{args.out_dir}/coverage_overlap_{args.run_id}.csv", start, fandango.coverage_log_overlap)


def write_log(path, start, log):
    symbols = sorted({s for _, coverage in log for s in coverage}, key=str)
    with open(path, "w") as f:
        f.write("time," + ",".join(f"covered_{s},total_{s},percent_{s}" for s in symbols) + "\n")
        for timestamp, coverage in log:
            cells = [f"{timestamp - start:.1f}"]
            for s in symbols:
                covered, total = coverage.get(s, (0, 0))
                percent = covered / total if total else 0
                cells.append(f"{covered},{total},{percent}")
            f.write(",".join(cells) + "\n")
