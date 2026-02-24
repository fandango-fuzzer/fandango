#!/bin/bash

TARGET_DIR="LightFTP"
PORT="${PORT:-2200}"
COV_OUT_DIR="${COV_OUT_DIR:-/cov_out}"
# If COV_OUT_DIR is relative, make it relative to WORKDIR. If absolute, leave it.
if [[ ! "$COV_OUT_DIR" =~ ^/ ]]; then
  COV_OUT_DIR="${WORKDIR}/${COV_OUT_DIR}"
fi

mkdir -p "${COV_OUT_DIR}"

cd "${WORKDIR}/${TARGET_DIR}-fandango/Source/Release"

gcovr -r .. -s -d > /dev/null 2>&1 || true

./fftp fftp.conf "${PORT}" > /dev/null 2>&1 &
SERVER_PID=$!

cd $WORKDIR/fandango

for i in {1..20}; do
  if netstat -ltn 2>/dev/null | grep -q ":${PORT} "; then
    break
  fi
  sleep 0.1
done

python3.11 ftp.py

kill -SIGUSR1 $SERVER_PID 2>/dev/null || true
wait $SERVER_PID || true

cd "${WORKDIR}/${TARGET_DIR}-fandango/Source/Release"

gcovr -r .. \
  --html --html-details \
  -o "${COV_OUT_DIR}index.html"

echo "Wrote coverage HTML to: ${COV_OUT_DIR}index.html"