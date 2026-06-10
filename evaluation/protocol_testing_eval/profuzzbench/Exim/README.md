# Fuzzing Exim server with AFLNet and AFLnwe
Please follow the steps below to run and collect experimental results for Exim.

## Step-1. Build a docker image
The following commands create a docker image tagged exim. The image should have everything available for fuzzing and code coverage calculation.

```bash
cd $PFBENCH
cd subjects/SMTP/Exim
docker build . -t exim
```

## Step-2. Run fuzzing
The following commands run 4 instances of AFLNet and 4 instances of AFLnwe to simultaenously fuzz Exim in 60 minutes.

```bash
cd $PFBENCH
mkdir results-exim

profuzzbench_exec_common.sh exim 4 results-exim aflnet out-exim-aflnet "-P SMTP -D 10000 -q 3 -s 3 -E -K -W 100" 3600 5 &
profuzzbench_exec_common.sh exim 4 results-exim aflnwe out-exim-aflnwe "-D 10000 -K -W 100" 3600 5
```

## Step-3. Collect the results
The following commands collect the  code coverage results produced by AFLNet and AFLnwe and save them to results.csv.

```bash
cd $PFBENCH/results-exim

profuzzbench_generate_csv.sh exim 4 aflnet results.csv 0
profuzzbench_generate_csv.sh exim 4 aflnwe results.csv 1
```

## Step-4. Analyze the results
The results collected in step 3 (i.e., results.csv) can be used for plotting. Use the following command to plot the coverage over time and save it to a file.

```
cd $PFBENCH/results-exim

profuzzbench_plot.py -i results.csv -p exim -r 4 -c 60 -s 1 -o cov_over_time.png
```

## Step-5. Run Fandango
The following commands run Fandango to measure the code coverage it reaches on Exim
(SMTP). It builds a dedicated image (`Dockerfile-fandango`) that contains an
additional gcov-instrumented Exim build (`exim-fandango`) and a plaintext
`AUTH LOGIN` authenticator (`the_user` / `the_password`).

```bash
cd $PFBENCH/subjects/SMTP/Exim

mkdir results-fandango
./run-fandango-standalone.sh
```

Set `FUZZ_TIME` to limit how long Fandango is allowed to run:

```bash
FUZZ_TIME=120 ./run-fandango-standalone.sh
```

The resulting line/branch coverage report is written as HTML into
`results-fandango/` (`index.html`), and the final line/branch totals are printed
to stdout.