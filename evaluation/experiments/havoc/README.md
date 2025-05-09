# Havoc Mutations on giflib

Prepare all binaries with

```bash
make
```

Then, use the following targets for experiments:

```bash
# before each gcov or Fandango run, clean the coverage from previous experiments with
make clean_gcov

make run_fandango FAN_FILE={gif,havoc_gif}.fan # run Fandango with the specified fan file
make run_libfuzzer # run libFuzzer
make post_libfuzzer # analyze (run corpus created from the libFuzzer run through the gcov instrumented file)
make gcov RUN_NAME={pure,havoc,libfuzzer} # run gcov analysis on the binary
```

## Results
After 1h across all cores of a MacBook:
- Coverages of 7% (pure Fandango), 54% (Fandango + havoc), and 67% (libFuzzer)
- *Not* always a strict superset, Fandango without havoc finds 2 lines that it didn't discover with havoc mutations enabled on 80% of generated inputs (in the allocated time!)
- 200x more input throughput in libFuzzer compared to Fandango (the former uses in-process fuzzing, doesn't need to generate a population satisfying a grammar and constraints, and uses different instrumentation)