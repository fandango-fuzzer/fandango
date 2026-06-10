#!/bin/sh

docker build . -f Dockerfile-fandango -t exim-fandango

docker run --rm -it \
  -v ./results-fandango/:/home/ubuntu/experiments/cov_out/ \
  -e COV_OUT_DIR=/home/ubuntu/experiments/cov_out/ \
  -e FUZZ_TIME="${FUZZ_TIME:-3600}" \
  exim-fandango:latest \
  experiments/fandango/run_fandango.sh
