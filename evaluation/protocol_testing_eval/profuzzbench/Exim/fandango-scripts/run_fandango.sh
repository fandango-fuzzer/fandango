#!/bin/bash

TARGET_DIR="exim-fandango"
PORT="${PORT:-8025}"
# Wall-clock budget for the Fandango run.
# Exim writes gcov data incrementally as each SMTP session
# ends, so stopping after FUZZ_TIME still captures all coverage reached so far.
FUZZ_TIME="${FUZZ_TIME:-3600}"
COV_OUT_DIR="${COV_OUT_DIR:-/cov_out}"
# If COV_OUT_DIR is relative, make it relative to WORKDIR. If absolute, leave it.
if [[ ! "$COV_OUT_DIR" =~ ^/ ]]; then
  COV_OUT_DIR="${WORKDIR}/${COV_OUT_DIR}"
fi

mkdir -p "${COV_OUT_DIR}"

# Use the gcov-instrumented Exim build for coverage measurement.
# The build directory is named per architecture (build-Linux-x86_64,
# build-Linux-arm64, ...), so glob it instead of hardcoding the arch.
cd "${WORKDIR}/${TARGET_DIR}"
cp ./src/build-Linux-*/exim /usr/exim/bin/exim

# Reset any previously collected coverage counters.
gcovr -r . -s -d > /dev/null 2>&1 || true

# Start the Exim daemon listening on ${PORT}.
# Run it in the background: in some environments (e.g. when launched as PID 1
# inside a container) "exim -bd" stays in the foreground instead of detaching,
# which would otherwise block this script. The pid file (-oP) still records the
# daemon's pid so it can be stopped afterwards.
exim -bd -oX "${PORT}" -oP /var/lock/exim.pid > /dev/null 2>&1 &

# Wait for the daemon to start listening.
for i in {1..50}; do
  if netstat -ltn 2>/dev/null | grep -q ":${PORT} "; then
    break
  fi
  sleep 0.1
done

cd "${WORKDIR}/fandango"

# Run Fandango for at most FUZZ_TIME seconds. SIGINT lets smtp.py unwind its
# try/finally cleanly; -k force-kills if it does not stop in time.
timeout -k 10 -s INT "${FUZZ_TIME}" python3.11 smtp.py || true

# Stop the Exim daemon. The connection-handling children already dumped their
# gcov data when each SMTP session ended; this just shuts down the listener.
pkill -F /var/lock/exim.pid 2>/dev/null || true
killall exim 2>/dev/null || true
sleep 1

cd "${WORKDIR}/${TARGET_DIR}"

# Exim copies some helper sources into the build dir and removes them after the
# build (lookups/lf_*.c and the local_scan.c hook stub). Exclude them, otherwise
# gcovr errors trying to read their now-missing source.
GCOVR_EXCLUDE="--exclude .*lf_.*\.c --exclude .*local_scan\.c"

# Final line/branch summary to stdout.
echo "=== Fandango code coverage on Exim ==="
gcovr -r . ${GCOVR_EXCLUDE} -s | grep -iE "lines:|branches:"

# Detailed HTML report.
gcovr -r . ${GCOVR_EXCLUDE} \
  --html --html-details \
  -o "${COV_OUT_DIR}index.html"

echo "Wrote coverage HTML to: ${COV_OUT_DIR}index.html"
