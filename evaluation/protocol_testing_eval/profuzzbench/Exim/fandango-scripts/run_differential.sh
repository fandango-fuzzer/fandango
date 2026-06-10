#!/bin/bash
# Differential coverage: AFLNet vs Fandango on Exim, using gcov.
#
# Both fuzzers are measured on the SAME gcov build (exim-gcov), with gcov data
# reset between them, so line/branch identifiers match exactly and the comparison
# is unbiased:
#   - Fandango drives exim-gcov live (grammar in smtp.fan).
#   - AFLNet fuzzes the AFL-instrumented Exim, then its queue is replayed against
#     exim-gcov (with our replay.py, since aflnet-replay aborts on some inputs).
#
# Per trial we export one gcovr JSON per approach, then diff_coverage.py reports
# Fandango-only / AFLNet-only / shared line and branch coverage.
set -u

TRIALS="${TRIALS:-1}"
FUZZ_TIME="${FUZZ_TIME:-120}"
PORT="${PORT:-8025}"
OUT="${COV_OUT_DIR:-/cov_out}"
OUT="${OUT%/}"

GCOVDIR="${WORKDIR}/exim-gcov"
GCOVEXIM=$(ls ${GCOVDIR}/src/build-Linux-*/exim)
AFLEXIM=$(ls ${WORKDIR}/exim/src/build-Linux-*/exim)
mkdir -p "${OUT}"

# Keep AFL's shared-memory env vars so the forked Exim children record edges.
sed -i 's/^keep_environment = ASAN_OPTIONS.*/keep_environment = ASAN_OPTIONS : __AFL_SHM_ID : __AFL_PERSISTENT : __AFL_OLD_FORKSRV_PERSISTENT/' /usr/exim/configure

free_port() {  # $1 = port
  pkill -F /var/lock/exim.pid 2>/dev/null
  fuser -k "$1/tcp" 2>/dev/null
  killall -9 exim 2>/dev/null
  for i in $(seq 1 40); do
    netstat -ltn 2>/dev/null | grep -q ":$1 " || break
    fuser -k "$1/tcp" 2>/dev/null; sleep 0.25
  done
  sleep 0.5
}

# Reclaim the port, install the gcov binary, reset gcov counters, start daemon.
start_gcov() {
  free_port "${PORT}"
  cd "${GCOVDIR}"
  cp "${GCOVEXIM}" /usr/exim/bin/exim
  gcovr -r . -d >/dev/null 2>&1 || true
  exim -bd -oX "${PORT}" -oP /var/lock/exim.pid >/dev/null 2>&1 &
  for i in $(seq 1 80); do netstat -ltn 2>/dev/null | grep -q ":${PORT} " && break; sleep 0.1; done
}

stop_gcov() { sleep 1; pkill -F /var/lock/exim.pid 2>/dev/null; killall -9 exim 2>/dev/null; sleep 1; }

gcov_json() {  # $1 = output json
  cd "${GCOVDIR}"
  gcovr -r . --json -o "$1" 2>/dev/null
  echo "  $(basename "$1"): $(gcovr -r . -s 2>/dev/null | grep -iE '^lines:|^branches:' | tr '\n' ' ')"
}

replay_dir() {  # $1 = dir of raw test cases
  for f in "$1"/*; do
    [ -f "$f" ] || continue
    python3.11 "${WORKDIR}/fandango/replay.py" "$f" "${PORT}" >/dev/null 2>&1
  done
}

for t in $(seq 1 "${TRIALS}"); do
  echo "### trial ${t}: Fandango (${FUZZ_TIME}s)"
  start_gcov
  ( cd "${WORKDIR}/fandango" && timeout -k 10 -s INT "${FUZZ_TIME}" python3.11 smtp.py >/dev/null 2>&1 || true )
  stop_gcov
  gcov_json "${OUT}/fandango_${t}.json"

  echo "### trial ${t}: AFLNet (${FUZZ_TIME}s fuzz + replay)"
  free_port "${PORT}"
  cp "${AFLEXIM}" /usr/exim/bin/exim
  rm -rf "${WORKDIR}/exim/aflout_${t}"
  ( cd "${WORKDIR}/exim" && timeout -k 0 --preserve-status "${FUZZ_TIME}" \
      afl-fuzz -d -m none -i "${WORKDIR}/in-smtp" -x "${WORKDIR}/smtp.dict" -o "aflout_${t}" \
      -N "tcp://127.0.0.1/${PORT}" -P SMTP -D 10000 -q 3 -s 3 -E -K -W 100 \
      -c "${WORKDIR}/clean" exim -bd -d -oX "${PORT}" -oP /var/lock/exim.pid >/dev/null 2>&1 || true )
  killall -9 afl-fuzz 2>/dev/null; sleep 1
  echo "  queue entries: $(ls ${WORKDIR}/exim/aflout_${t}/queue 2>/dev/null | wc -l)"
  start_gcov
  replay_dir "${WORKDIR}/exim/aflout_${t}/queue"
  stop_gcov
  gcov_json "${OUT}/aflnet_${t}.json"
done

echo; echo "================ differential coverage ================"
python3.11 "${WORKDIR}/fandango/diff_coverage.py" \
    "${OUT}/fandango_1.json" "${OUT}/aflnet_1.json" 2>&1 | tee "${OUT}/differential.txt"
echo; echo "Done. JSONs + differential.txt under ${OUT}"
