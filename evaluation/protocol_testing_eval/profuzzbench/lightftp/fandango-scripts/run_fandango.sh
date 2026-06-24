#!/bin/bash
# In-container entry point for the LightFTP (FTP) Fandango coverage

set -u

WORKDIR="${WORKDIR:-/home/ubuntu}"
LIGHTFTP_SRC="${LIGHTFTP_SRC:-/home/ubuntu/LightFTP-fandango}"
RELEASE_DIR="${LIGHTFTP_SRC}/src/Release"
PORT="${PORT:-2200}"
export FTP_PORT="${PORT}"

COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
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
  echo "watchdog: RUN_FANDANGO_TIMEOUT (${RUN_FANDANGO_TIMEOUT}s) reached, killing process group" >&2
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
echo "resetting gcov counters in ${LIGHTFTP_SRC}"
gcovr -r "${LIGHTFTP_SRC}/src" -d >/dev/null 2>&1 || true
find "$LIGHTFTP_SRC" -name '*.gcda' -delete 2>/dev/null || true

# Start the instrumented fftp server (reads the listen port from argv[2]).
cd "$RELEASE_DIR" || { echo "missing ${RELEASE_DIR}" >&2; cleanup_watchdog; exit 1; }
echo "starting fftp: ./fftp fftp.conf ${PORT}"
./fftp fftp.conf "${PORT}" > "${COV_OUT_DIR}fftp.log" 2>&1 &
SERVER_PID=$!

READY=0
for i in $(seq 1 20); do
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "fftp exited early; see ${COV_OUT_DIR}fftp.log" >&2
    break
  fi
  if netstat -ltn 2>/dev/null | grep -q ":${PORT} " || \
     ss -ltn 2>/dev/null | grep -q ":${PORT}\b"; then
    READY=1
    break
  fi
  sleep 0.5
done
if [ "$READY" -eq 1 ]; then
  echo "fftp is listening on ${PORT}/tcp"
else
  echo "WARNING: fftp not confirmed ready on ${PORT}/tcp; proceeding anyway" >&2
fi

# Run the Fandango client, time-bounded. NO_MESSAGES=1 => baseline (server
cd "${WORKDIR}/fandango"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "NO_MESSAGES=1: baseline run, NOT sending any FTP messages"
  sleep "${BASELINE_IDLE:-3}"
else
  echo "running Fandango ftp.py (grammar=${FANDANGO_FAN:-ftp_client.fan}) for up to ${FANDANGO_DURATION}s"
  timeout "${FANDANGO_DURATION}" python3.11 ftp.py ${FANDANGO_FAN:+"$FANDANGO_FAN"} || true
  echo "Fandango run finished"
fi

# Stop fftp via SIGUSR1 so gcov data is flushed. Bounded wait, then SIGKILL.
if kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "sending SIGUSR1 to fftp (pid ${SERVER_PID}) to flush gcov"
  kill -SIGUSR1 "$SERVER_PID" 2>/dev/null || true
  for i in $(seq 1 "$SHUTDOWN_WAIT"); do
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
      break
    fi
    sleep 1
  done
  if kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "fftp still alive after ${SHUTDOWN_WAIT}s; escalating to SIGKILL" >&2
    kill -KILL "$SERVER_PID" 2>/dev/null || true
  fi
fi
wait "$SERVER_PID" 2>/dev/null || true

sleep 1
GCDA_COUNT=$(find "$LIGHTFTP_SRC" -name '*.gcda' 2>/dev/null | wc -l | tr -d ' ')
echo ".gcda files after shutdown: ${GCDA_COUNT}"
if [ "$GCDA_COUNT" -eq 0 ]; then
  echo "no .gcda files were produced; coverage will be 0" >&2
fi

# Produce the report artifacts into COV_OUT_DIR.
echo "generating coverage report in ${COV_OUT_DIR}"
GCOVR_ROOT="${LIGHTFTP_SRC}/src"

gcovr -r "$GCOVR_ROOT" --html \
  -o "${COV_OUT_DIR}index.html" 2>/dev/null || \
  echo "gcovr HTML overview generation failed" >&2

# Emit full coverage report
HTML_DETAIL_DIR="${COV_OUT_DIR}html"
mkdir -p "$HTML_DETAIL_DIR"
gcovr -r "$GCOVR_ROOT" --html-details \
  -o "${HTML_DETAIL_DIR}/index.html" 2>/dev/null || \
  echo "gcovr HTML detail generation failed" >&2

gcovr -r "$GCOVR_ROOT" -s > "${COV_OUT_DIR}coverage.txt" 2>/dev/null || \
  echo "lines: 0% branches: 0%" > "${COV_OUT_DIR}coverage.txt"

cat "${COV_OUT_DIR}coverage.txt" || true

gcovr -r "$GCOVR_ROOT" > "${COV_OUT_DIR}coverage_files.txt" 2>/dev/null || true

python3.11 - "$GCOVR_ROOT" "${COV_OUT_DIR}summary.csv" <<'PYEOF'
import re
import subprocess
import sys

root, out_csv = sys.argv[1], sys.argv[2]

try:
    out = subprocess.run(
        ["gcovr", "-r", root, "-s"],
        capture_output=True, text=True, timeout=600,
    ).stdout
except Exception:
    out = ""


def parse(metric_label):
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

echo "coverage artifacts:"
ls -la "${COV_OUT_DIR}" || true

cleanup_watchdog
echo "done"
