# Havoc Mutations on giflib

Run the experiments with a simple

```bash
make
```

This will compile giflib (with a little harness in `gif_parser.c`) instrumented with gcov. Then, Fandango is executed on it twice, once with and once without `havoc_mutate`. The coverage reports of each run end up in `branch_coverage_{havoc,pure}.txt`.