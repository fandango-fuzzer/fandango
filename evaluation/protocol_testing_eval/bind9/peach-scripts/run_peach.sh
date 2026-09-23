#!/bin/bash
set -u

WORKDIR="${WORKDIR:-/home/ubuntu}"
BIND_SRC="${BIND_SRC:-/home/ubuntu/bind9-src}"
BIND_PREFIX="${BIND_PREFIX:-/home/ubuntu/bind9-install}"
NAMED="${BIND_PREFIX}/sbin/named"
NAMED_CONF="${NAMED_CONF:-/home/ubuntu/bind-conf/named.conf}"
PORT="${PORT:-25566}"
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

echo "resetting gcov counters in $BIND_SRC"
gcovr -r "$BIND_SRC" -d >/dev/null 2>&1 || true
find "$BIND_SRC" -name '*.gcda' -delete 2>/dev/null || true

echo "starting named on ${PORT}/udp"
"$NAMED" -f -g -c "$NAMED_CONF" -n 1 > "${COV_OUT_DIR}named.log" 2>&1 &
server=$!

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

echo "starting traffic_recorder.py (25567 -> 25566/udp)"
python3.11 "${PEACH_DIR}/traffic_recorder.py" --out "${COV_OUT_DIR}traffic.jsonl" \
  --udp 25567:25566:dns > "${COV_OUT_DIR}traffic_recorder.log" 2>&1 &
recorder=$!

mkdir -p "${COV_OUT_DIR}peach"
rm -rf /opt/peach/Logs && ln -s "${COV_OUT_DIR}peach" /opt/peach/Logs
cd "${COV_OUT_DIR}peach"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "baseline run: sending no DNS messages"
  sleep "${BASELINE_IDLE:-3}"
else
  duration=$(printf '%d.%02d:%02d:%02d' $((PEACH_DURATION / 86400)) $((PEACH_DURATION % 86400 / 3600)) \
                                        $((PEACH_DURATION % 3600 / 60)) $((PEACH_DURATION % 60)))
  echo "running peach (dns.xml) for ${PEACH_DURATION}s"
  timeout -k 30 "$((PEACH_DURATION + 60))" \
    mono /opt/peach/Peach.exe --noweb --polite --duration="$duration" "${PEACH_DIR}/dns.xml" \
    > "${COV_OUT_DIR}peach.log" 2>&1 || true
fi
kill "$recorder" 2>/dev/null || true

if kill -0 "$server" 2>/dev/null; then
  echo "stopping named (pid $server)"
  kill -TERM "$server" 2>/dev/null || true
  for _ in $(seq 1 "$SHUTDOWN_WAIT"); do kill -0 "$server" 2>/dev/null || break; sleep 1; done
  kill -0 "$server" 2>/dev/null && kill -KILL "$server" 2>/dev/null || true
fi
wait "$server" 2>/dev/null || true
sleep 1

gcda=$(find "$BIND_SRC" -name '*.gcda' 2>/dev/null | wc -l | tr -d ' ')
echo ".gcda files written: $gcda"
[ "$gcda" = 0 ] && echo "no .gcda files produced" >&2

echo "writing coverage report to $COV_OUT_DIR"
find "$BIND_SRC" \( -name 'a-conftest.*' -o -name 'conftest.*' \) -delete 2>/dev/null || true

gcovr -r "$BIND_SRC" --csv -o "${COV_OUT_DIR}coverage_branches.csv" || true

echo "artifacts:"; ls -la "$COV_OUT_DIR" || true
stop_watchdog
echo "done"
