#!/bin/sh


docker build . -f Dockerfile-fandango -t lightftp-fandango

docker run --rm -it \
  -v ./results-fandango/:/home/ubuntu/experiments/cov_out/ \
  -e COV_OUT_DIR=/home/ubuntu/experiments/cov_out/ \
  lightftp-fandango:latest \
  experiments/fandango/run_fandango.sh