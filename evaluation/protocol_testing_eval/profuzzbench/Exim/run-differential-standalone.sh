#!/bin/sh

# Copy the local Fandango checkout into the build context, then build.
./sync-fandango.sh
docker build . -f Dockerfile-fandango -t exim-fandango

mkdir -p ./results-diff
docker run --rm \
  -v ./results-diff/:/home/ubuntu/experiments/cov_out/ \
  -e COV_OUT_DIR=/home/ubuntu/experiments/cov_out/ \
  -e FUZZ_TIME="${FUZZ_TIME:-120}" \
  -e TRIALS="${TRIALS:-1}" \
  exim-fandango:latest \
  experiments/fandango/run_differential.sh
