#!/bin/bash
# In-container entry point for the bind9 (DNS) Fandango coverage target.

set -u

WORKDIR="${WORKDIR:-/home/ubuntu}"
BIND_SRC="${BIND_SRC:-/home/ubuntu/bind9-src}"
BIND_PREFIX="${BIND_PREFIX:-/home/ubuntu/bind9-install}"
NAMED="${BIND_PREFIX}/sbin/named"
NAMED_CONF="${NAMED_CONF:-/home/ubuntu/bind-conf/named.conf}"
PORT="${PORT:-25566}"

COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
# Normalise to a trailing slash so "${COV_OUT_DIR}file" is always correct.
case "$COV_OUT_DIR" in
  */) : ;;
  *) COV_OUT_DIR="${COV_OUT_DIR}/" ;;
esac
mkdir -p "$COV_OUT_DIR"

FANDANGO_DURATION="${FANDANGO_DURATION:-120}"
SHUTDOWN_WAIT="${SHUTDOWN_WAIT:-15}"

# Overall watchdog: if anything wedges, kill our whole process group so the
# container always exits and the host can still collect coverage.
RUN_FANDANGO_TIMEOUT="${RUN_FANDANGO_TIMEOUT:-600}"
SELF_PGID=$$
(
  sleep "$RUN_FANDANGO_TIMEOUT"
  echo "[run_fandango] watchdog: RUN_FANDANGO_TIMEOUT (${RUN_FANDANGO_TIMEOUT}s) reached, killing process group" >&2
  kill -TERM -"$SELF_PGID" 2>/dev/null || true
  sleep 5
  kill -KILL -"$SELF_PGID" 2>/dev/null || true
) &
WATCHDOG_PID=$!

cleanup_watchdog() {
  kill "$WATCHDOG_PID" 2>/dev/null || true
  wait "$WATCHDOG_PID" 2>/dev/null || true
}

# Reset stale coverage counters in the instrumented build tree.
echo "[run_fandango] resetting gcov counters in ${BIND_SRC}"
gcovr -r "$BIND_SRC" -d >/dev/null 2>&1 || true
find "$BIND_SRC" -name '*.gcda' -delete 2>/dev/null || true

# 3. Start instrumented named in the foreground, backgrounded by the shell.
# -f : foreground, -g : log to stderr, -c : config, -n 1 : single worker.
echo "[run_fandango] starting named: ${NAMED} -f -g -c ${NAMED_CONF} -n 1"
"$NAMED" -f -g -c "$NAMED_CONF" -n 1 > "${COV_OUT_DIR}named.log" 2>&1 &
SERVER_PID=$!

# Wait until 25566/udp is ready (max ~20 x 0.5s = 10s).
READY=0
for i in $(seq 1 20); do
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "[run_fandango] named exited early; see ${COV_OUT_DIR}named.log" >&2
    break
  fi
  # UDP listener shows as a local address in `ss`/`netstat`.
  if ss -lun 2>/dev/null | grep -q ":${PORT}\b" || \
     netstat -lun 2>/dev/null | grep -q ":${PORT} "; then
    READY=1
    break
  fi
  # Functional probe: a query against the local zone must answer.
  if command -v dig >/dev/null 2>&1; then
    if dig @127.0.0.1 -p "${PORT}" +time=1 +tries=1 cispa.de A >/dev/null 2>&1; then
      READY=1
      break
    fi
  fi
  sleep 0.5
done

if [ "$READY" -eq 1 ]; then
  echo "[run_fandango] named is listening on ${PORT}/udp"
else
  echo "[run_fandango] WARNING: named not confirmed ready on ${PORT}/udp; proceeding anyway" >&2
fi

# Run the Fandango client, time-bounded.
cd "${WORKDIR}/fandango"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "[run_fandango] NO_MESSAGES=1: baseline run, NOT sending any DNS messages"
  sleep "${BASELINE_IDLE:-3}"
else
  echo "[run_fandango] running Fandango dns.py (grammar=${FANDANGO_FAN:-dns.fan}) for up to ${FANDANGO_DURATION}s"
  timeout "${FANDANGO_DURATION}" python3.11 dns.py ${FANDANGO_FAN:+"$FANDANGO_FAN"} || true
  echo "[run_fandango] Fandango run finished"
fi

# Stop named so gcov data is flushed. Bounded wait, then SIGKILL.
if kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "[run_fandango] sending SIGTERM to named (pid ${SERVER_PID})"
  kill -TERM "$SERVER_PID" 2>/dev/null || true
  for i in $(seq 1 "$SHUTDOWN_WAIT"); do
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
      break
    fi
    sleep 1
  done
  if kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "[run_fandango] named still alive after ${SHUTDOWN_WAIT}s; escalating to SIGKILL" >&2
    kill -KILL "$SERVER_PID" 2>/dev/null || true
  fi
fi
wait "$SERVER_PID" 2>/dev/null || true

# Give the gcov runtime a moment to finish writing .gcda files.
sleep 1
GCDA_COUNT=$(find "$BIND_SRC" -name '*.gcda' 2>/dev/null | wc -l | tr -d ' ')
echo "[run_fandango] .gcda files after shutdown: ${GCDA_COUNT}"
if [ "$GCDA_COUNT" -eq 0 ]; then
  echo "[run_fandango] WARNING: no .gcda files were produced; coverage will be 0" >&2
fi

# Produce the report artifacts into COV_OUT_DIR.
echo "[run_fandango] generating coverage report in ${COV_OUT_DIR}"

gcovr -r "$BIND_SRC" \
  --html --html-details \
  -o "${COV_OUT_DIR}index.html" 2>/dev/null || \
  echo "[run_fandango] WARNING: gcovr HTML generation failed" >&2

gcovr -r "$BIND_SRC" -s > "${COV_OUT_DIR}coverage.txt" 2>/dev/null || \
  echo "lines: 0% branches: 0%" > "${COV_OUT_DIR}coverage.txt"

cat "${COV_OUT_DIR}coverage.txt" || true

gcovr -r "$BIND_SRC" > "${COV_OUT_DIR}coverage_files.txt" 2>/dev/null || true

python3.11 - "$BIND_SRC" "${COV_OUT_DIR}summary.csv" <<'PYEOF'
import re
import subprocess
import sys

bind_src, out_csv = sys.argv[1], sys.argv[2]

try:
    out = subprocess.run(
        ["gcovr", "-r", bind_src, "-s"],
        capture_output=True, text=True, timeout=600,
    ).stdout
except Exception:
    out = ""


def parse(metric_label):
    """Return (percent, covered, total) for a gcovr -s summary metric."""
    m = re.search(
        rf"{metric_label}[.\s]*:\s*([0-9.]+)%\s*\((\d+)\s+out of\s+(\d+)\)",
        out, re.IGNORECASE,
    )
    if m:
        return (float(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(
        rf"{metric_label}[.\s]*:\s*([0-9.]+)%\s+(\d+)\s*/\s*(\d+)",
        out, re.IGNORECASE,
    )
    if m:
        return (float(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(rf"{metric_label}[.\s]*:\s*([0-9.]+)%", out, re.IGNORECASE)
    if m:
        return (float(m.group(1)), 0, 0)
    return (0.0, 0, 0)

lines = parse("lines")
branches = parse("branches")

with open(out_csv, "w") as f:
    f.write("metric,percent,covered,total\n")
    f.write("lines,%s,%d,%d\n" % (lines[0], lines[1], lines[2]))
    f.write("branches,%s,%d,%d\n" % (branches[0], branches[1], branches[2]))

print("summary.csv: lines=%.2f%% (%d/%d) branches=%.2f%% (%d/%d)" % (
    lines[0], lines[1], lines[2], branches[0], branches[1], branches[2]))
PYEOF

echo "[run_fandango] coverage artifacts:"
ls -la "${COV_OUT_DIR}" || true

cleanup_watchdog
echo "[run_fandango] done"
