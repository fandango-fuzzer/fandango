# Examples of how to pass data from Fandango to the PUT

Checkout [`Makefile`](./Makefile) for the compilation commands used, and [`example_harness.c`](./example_harness.c) for the harness used for the different modes.

Compile all binaries with a simple

```bash
make
```

Then, to make Fandango pass its input to the target binary using the different options, execute

```bash
make run_fandango_{file,stdin,libfuzzer}
```

Finally, comparing Fandango to libafl_libFuzzer (since libFuzzer is deprecated), can be done by running the following

```bash
make run_fandango_libfuzzer
make run_libfuzzer
```