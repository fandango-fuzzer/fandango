#!/bin/bash
set -u

WORKDIR="${WORKDIR:-/home/ubuntu}"
LIGHTFTP_SRC="${LIGHTFTP_SRC:-/home/ubuntu/LightFTP-fandango}"
RELEASE_DIR="${LIGHTFTP_SRC}/src/Release"
GCOVR_ROOT="${LIGHTFTP_SRC}/src"
PORT="${PORT:-2200}"
PEACH_DIR="${WORKDIR}/peach"
PEACH_DURATION="${PEACH_DURATION:-120}"
SHUTDOWN_WAIT="${SHUTDOWN_WAIT:-15}"

while [ $# -gt 0 ]; do
  case "$1" in
    --duration) PEACH_DURATION="${2%.*}"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
COV_OUT_DIR="${COV_OUT_DIR%/}/"
mkdir -p "$COV_OUT_DIR"

(
  sleep "${RUN_PEACH_TIMEOUT:-$((PEACH_DURATION + 300))}"
  echo "watchdog timeout reached, killing process group" >&2
  kill -TERM -$$ 2>/dev/null || true
  sleep 30
  kill -KILL -$$ 2>/dev/null || true
) &
watchdog=$!
stop_watchdog() { kill "$watchdog" 2>/dev/null || true; wait "$watchdog" 2>/dev/null || true; }

echo "resetting gcov counters in $LIGHTFTP_SRC"
gcovr -r "$GCOVR_ROOT" -d >/dev/null 2>&1 || true
find "$LIGHTFTP_SRC" -name '*.gcda' -delete 2>/dev/null || true

cd "$RELEASE_DIR" || { echo "missing $RELEASE_DIR" >&2; stop_watchdog; exit 1; }
echo "starting fftp on ${PORT}/tcp"
./fftp fftp.conf "$PORT" > "${COV_OUT_DIR}fftp.log" 2>&1 &
server=$!

echo "starting ftp_proxy.py (control 2121, data 50100)"
python3.11 "${PEACH_DIR}/ftp_proxy.py" --server-port "$PORT" > "${COV_OUT_DIR}ftp_proxy.log" 2>&1 &
proxy=$!

ready=0
for _ in $(seq 1 20); do
  kill -0 "$server" 2>/dev/null || { echo "fftp exited early; see ${COV_OUT_DIR}fftp.log" >&2; break; }
  if ss -ltn 2>/dev/null | grep -q ":${PORT}\b" && ss -ltn 2>/dev/null | grep -q ":2121\b"; then
    ready=1; break
  fi
  if netstat -ltn 2>/dev/null | grep -q ":${PORT} " && netstat -ltn 2>/dev/null | grep -q ":2121 "; then
    ready=1; break
  fi
  sleep 0.5
done
[ "$ready" = 1 ] && echo "fftp and proxy are listening" \
                 || echo "fftp/proxy not confirmed ready; proceeding anyway" >&2

mkdir -p "${COV_OUT_DIR}peach"
rm -rf /opt/peach/Logs && ln -s "${COV_OUT_DIR}peach" /opt/peach/Logs
cd "${COV_OUT_DIR}peach"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "baseline run: sending no messages"
  sleep "${BASELINE_IDLE:-3}"
else
  duration=$(printf '%d.%02d:%02d:%02d' $((PEACH_DURATION / 86400)) $((PEACH_DURATION % 86400 / 3600)) \
                                        $((PEACH_DURATION % 3600 / 60)) $((PEACH_DURATION % 60)))
  echo "running peach (ftp.xml) for ${PEACH_DURATION}s"
  timeout -k 30 "$((PEACH_DURATION + 60))" \
    mono /opt/peach/Peach.exe --noweb --polite --duration="$duration" "${PEACH_DIR}/ftp.xml" \
    > "${COV_OUT_DIR}peach.log" 2>&1 || true
fi

kill "$proxy" 2>/dev/null || true

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
find "$GCOVR_ROOT" \( -name 'a-conftest.*' -o -name 'conftest.*' \) -delete 2>/dev/null || true
gcovr -r "$GCOVR_ROOT" --csv -o "${COV_OUT_DIR}coverage_branches.csv" || true

echo "artifacts:"; ls -la "$COV_OUT_DIR" || true
stop_watchdog
echo "done"
