"""Measurement runs for the experiments. The target's driver always calls run();
the --experiment argument decides what happens:

  (no --experiment)         run Fandango normally (guidance on, stop at full
                            grammar coverage, no measurement output).
  --experiment throughput   same, but never stop early -- keep generating for the
                            whole --duration, then dump input/output/tree counts.
  --experiment coverage     guidance per --guidance, log grammar coverage every
                            --interval steps, stop at 100% coverage or --duration.
"""
import argparse
import time

from fandango.language.grammar import FuzzingMode

# Transport/timer parties, not protocol messages.
PLUMBING = {"SocketControlServer", "SocketControlClient", "TimerControl", "TimerEvent", "StdOut"}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("grammar", nargs="?")
    p.add_argument("--experiment", choices=["throughput", "coverage"])
    p.add_argument("--duration", type=float, default=3600)
    p.add_argument("--guidance", type=int, default=1)
    p.add_argument("--interval", type=int, default=20)
    p.add_argument("--out-dir", default=".")
    p.add_argument("--run-id", default="1")
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

    start = time.time()
    try:
        for _ in fandango.generate(mode=FuzzingMode.IO, max_generations=max_generations):
            if args.experiment and time.time() - start >= args.duration:
                break
    finally:
        if args.experiment == "throughput":
            write_throughput(fandango, args, start)
        elif args.experiment == "coverage":
            write_coverage(fandango, args, start)


def write_throughput(fandango, args, start):
    trees = fandango._packet_selector._all_derivation_trees()
    inputs = outputs = 0
    for tree in trees:
        for msg in tree.protocol_msgs():
            if msg.sender in PLUMBING:
                continue
            if fandango._io_instance.parties[msg.sender].is_fuzzer_controlled():
                inputs += 1
            else:
                outputs += 1
    grammar_coverage = fandango._packet_selector.coverage_percent(alt_cache=True) * 100
    with open(f"{args.out_dir}/throughput_{args.run_id}.txt", "w") as f:
        f.write(f"input messages:   {inputs}\n")
        f.write(f"output messages:  {outputs}\n")
        f.write(f"derivation trees: {len(trees)}\n")
        f.write(f"time:             {time.time() - start:.1f}s\n")
        f.write(f"grammar coverage: {grammar_coverage:.2f}%\n")


def write_coverage(fandango, args, start):
    write_log(f"{args.out_dir}/coverage_{args.run_id}.csv", start, fandango.coverage_log)
    write_log(f"{args.out_dir}/coverage_overlap_{args.run_id}.csv", start, fandango.coverage_log_overlap)


def write_log(path, start, log):
    with open(path, "w") as f:
        symbols = None
        for timestamp, coverage in log:
            if symbols is None:
                symbols = sorted(coverage, key=str)
                f.write("time," + ",".join(f"covered_{s},total_{s}" for s in symbols) + "\n")
            cells = [f"{timestamp - start:.1f}"]
            for s in symbols:
                covered, total = coverage[s]
                cells.append(f"{covered},{total}")
            f.write(",".join(cells) + "\n")
