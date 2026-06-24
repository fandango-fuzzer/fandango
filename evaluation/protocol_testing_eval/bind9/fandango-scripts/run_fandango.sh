#!/bin/bash
# In-container entry point for the bind9 (DNS) target: start instrumented named,
# run Fandango against it, then write the gcov report into COV_OUT_DIR.
set -u

WORKDIR="${WORKDIR:-/home/ubuntu}"
BIND_SRC="${BIND_SRC:-/home/ubuntu/bind9-src}"
BIND_PREFIX="${BIND_PREFIX:-/home/ubuntu/bind9-install}"
NAMED="${BIND_PREFIX}/sbin/named"
NAMED_CONF="${NAMED_CONF:-/home/ubuntu/bind-conf/named.conf}"
PORT="${PORT:-25566}"
FANDANGO_DURATION="${FANDANGO_DURATION:-120}"
SHUTDOWN_WAIT="${SHUTDOWN_WAIT:-15}"

COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
COV_OUT_DIR="${COV_OUT_DIR%/}/"
mkdir -p "$COV_OUT_DIR"

# Watchdog: if anything wedges, kill the whole process group so the container
# always exits and the host can still collect coverage.
(
  sleep "${RUN_FANDANGO_TIMEOUT:-600}"
  echo "watchdog timeout reached, killing process group" >&2
  kill -TERM -$$ 2>/dev/null || true
  sleep 30
  kill -KILL -$$ 2>/dev/null || true
) &
watchdog=$!
stop_watchdog() { kill "$watchdog" 2>/dev/null || true; wait "$watchdog" 2>/dev/null || true; }

# Start from clean counters.
echo "resetting gcov counters in $BIND_SRC"
gcovr -r "$BIND_SRC" -d >/dev/null 2>&1 || true
find "$BIND_SRC" -name '*.gcda' -delete 2>/dev/null || true

# named: -f foreground, -g log to stderr, -c config, -n 1 single worker.
echo "starting named on ${PORT}/udp"
"$NAMED" -f -g -c "$NAMED_CONF" -n 1 > "${COV_OUT_DIR}named.log" 2>&1 &
server=$!

# Wait (up to ~10s) for the port to bind or a probe query to answer.
ready=0
for _ in $(seq 1 20); do
  kill -0 "$server" 2>/dev/null || { echo "named exited early; see ${COV_OUT_DIR}named.log" >&2; break; }
  if ss -lun 2>/dev/null | grep -q ":${PORT}\b" || netstat -lun 2>/dev/null | grep -q ":${PORT} "; then
    ready=1; break
  fi
  if command -v dig >/dev/null 2>&1 && dig @127.0.0.1 -p "$PORT" +time=1 +tries=1 example.com A >/dev/null 2>&1; then
    ready=1; break
  fi
  sleep 0.5
done
[ "$ready" = 1 ] && echo "named is listening on ${PORT}/udp" \
                 || echo "named not confirmed ready; proceeding anyway" >&2

# Run Fandango, or idle for a baseline run that sends nothing.
cd "${WORKDIR}/fandango"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "baseline run: sending no DNS messages"
  sleep "${BASELINE_IDLE:-3}"
else
  echo "running dns.py (grammar=${FANDANGO_FAN:-dns_client.fan}) for up to ${FANDANGO_DURATION}s"
  timeout "$FANDANGO_DURATION" python3.11 dns.py ${FANDANGO_FAN:+"$FANDANGO_FAN"} "$@" || true
fi

# Stop named so gcov flushes: SIGTERM, wait, then SIGKILL.
if kill -0 "$server" 2>/dev/null; then
  echo "stopping named (pid $server)"
  kill -TERM "$server" 2>/dev/null || true
  for _ in $(seq 1 "$SHUTDOWN_WAIT"); do kill -0 "$server" 2>/dev/null || break; sleep 1; done
  kill -0 "$server" 2>/dev/null && kill -KILL "$server" 2>/dev/null || true
fi
wait "$server" 2>/dev/null || true
sleep 1   # let the gcov runtime finish writing .gcda files

gcda=$(find "$BIND_SRC" -name '*.gcda' 2>/dev/null | wc -l | tr -d ' ')
echo ".gcda files written: $gcda"
[ "$gcda" = 0 ] && echo "no .gcda files produced; coverage will be 0" >&2

echo "writing coverage report to $COV_OUT_DIR"
# Remove stray autoconf configure-test artifacts (conftest.*) whose .gcda cannot
# be opened. gcov treats them as an error
find "$BIND_SRC" \( -name 'a-conftest.*' -o -name 'conftest.*' \) -delete 2>/dev/null || true

gcovr -r "$BIND_SRC" --txt -o "${COV_OUT_DIR}coverage.txt" || echo "lines: 0% branches: 0%" > "${COV_OUT_DIR}coverage.txt"
gcovr -r "$BIND_SRC" --csv -o "${COV_OUT_DIR}coverage_branches.csv" || true  # per-file line+branch

echo "artifacts:"; ls -la "$COV_OUT_DIR" || true
stop_watchdog
echo "done"
