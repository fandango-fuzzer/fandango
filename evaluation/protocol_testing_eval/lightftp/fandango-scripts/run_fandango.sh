#!/bin/bash
set -u

WORKDIR="${WORKDIR:-/home/ubuntu}"
LIGHTFTP_SRC="${LIGHTFTP_SRC:-/home/ubuntu/LightFTP-fandango}"
RELEASE_DIR="${LIGHTFTP_SRC}/src/Release"
GCOVR_ROOT="${LIGHTFTP_SRC}/src"
PORT="${PORT:-2200}"
export FTP_PORT="${PORT}"
FANDANGO_DURATION="${FANDANGO_DURATION:-120}"
SHUTDOWN_WAIT="${SHUTDOWN_WAIT:-15}"

COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
COV_OUT_DIR="${COV_OUT_DIR%/}/"
mkdir -p "$COV_OUT_DIR"

# Watchdog: kill the whole process group if the run times out.
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
echo "resetting gcov counters in $LIGHTFTP_SRC"
gcovr -r "$GCOVR_ROOT" -d >/dev/null 2>&1 || true
find "$LIGHTFTP_SRC" -name '*.gcda' -delete 2>/dev/null || true

# fftp reads its listen port from argv[2].
cd "$RELEASE_DIR" || { echo "missing $RELEASE_DIR" >&2; stop_watchdog; exit 1; }
echo "starting fftp on ${PORT}/tcp"
./fftp fftp.conf "$PORT" > "${COV_OUT_DIR}fftp.log" 2>&1 &
server=$!

# Wait (up to ~10s) for the port to start listening.
ready=0
for _ in $(seq 1 20); do
  kill -0 "$server" 2>/dev/null || { echo "fftp exited early; see ${COV_OUT_DIR}fftp.log" >&2; break; }
  if ss -ltn 2>/dev/null | grep -q ":${PORT}\b" || netstat -ltn 2>/dev/null | grep -q ":${PORT} "; then
    ready=1; break
  fi
  sleep 0.5
done
[ "$ready" = 1 ] && echo "fftp is listening on ${PORT}/tcp" \
                 || echo "fftp not confirmed ready; proceeding anyway" >&2

# Run Fandango, or idle for a baseline run that sends nothing.
cd "${WORKDIR}/fandango"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "baseline run: sending no messages"
  sleep "${BASELINE_IDLE:-3}"
else
  echo "running ftp.py (grammar=${FANDANGO_FAN:-ftp_client.fan}) for up to ${FANDANGO_DURATION}s"
  timeout "$FANDANGO_DURATION" python3.11 ftp.py ${FANDANGO_FAN:+"$FANDANGO_FAN"} "$@" || true
fi

# fftp flushes gcov on SIGUSR1; wait, then SIGKILL.
if kill -0 "$server" 2>/dev/null; then
  echo "flushing fftp gcov (SIGUSR1, pid $server)"
  kill -SIGUSR1 "$server" 2>/dev/null || true
  for _ in $(seq 1 "$SHUTDOWN_WAIT"); do kill -0 "$server" 2>/dev/null || break; sleep 1; done
  kill -0 "$server" 2>/dev/null && kill -KILL "$server" 2>/dev/null || true
fi
wait "$server" 2>/dev/null || true
sleep 1

gcda=$(find "$LIGHTFTP_SRC" -name '*.gcda' 2>/dev/null | wc -l | tr -d ' ')
echo ".gcda files written: $gcda"
[ "$gcda" = 0 ] && echo "no .gcda files produced" >&2

echo "writing coverage report to $COV_OUT_DIR"
# Remove stray autoconf configure-test artifacts (conftest.*) whose .gcda cannot
# be opened. gcov treats them as an error
find "$GCOVR_ROOT" \( -name 'a-conftest.*' -o -name 'conftest.*' \) -delete 2>/dev/null || true

# export coverage
gcovr -r "$GCOVR_ROOT" --csv -o "${COV_OUT_DIR}coverage_branches.csv" || true

echo "artifacts:"; ls -la "$COV_OUT_DIR" || true
stop_watchdog
echo "done"
