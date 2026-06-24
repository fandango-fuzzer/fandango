#!/bin/bash
# In-container entry point for the OpenSMTPD Fandango coverage target.

set -u

BUILD_DIR="${BUILD_DIR:-/home/ubuntu/OpenSMTPD-7.7.0p0}"
SMTPD_CONF="${SMTPD_CONF:-/etc/smtpd.conf}"
GCOV_SUBDIR="usr.sbin/smtpd"           # sources we care about, relative to BUILD_DIR
COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
FANDANGO_DURATION="${FANDANGO_DURATION:-120}"
RUN_FANDANGO_TIMEOUT="${RUN_FANDANGO_TIMEOUT:-600}"
FANDANGO_DIR="/home/ubuntu/fandango"

mkdir -p "${COV_OUT_DIR}"

# Watchdog: kill the whole process group if the run wedges, so the container
# always exits and the host can still collect coverage.
(
  sleep "${RUN_FANDANGO_TIMEOUT}"
  echo "watchdog timeout reached, killing process group" >&2
  kill -TERM -- "-$$" 2>/dev/null || true
  sleep 5
  kill -KILL -- "-$$" 2>/dev/null || true
) &
watchdog=$!
trap 'kill "$watchdog" 2>/dev/null || true' EXIT

# Reset stale coverage counters in the build tree.
echo "Resetting stale .gcda counters under ${BUILD_DIR}"
find "${BUILD_DIR}" -name '*.gcda' -delete 2>/dev/null || true

# symlink subdirs
for d in queue incoming purge temporary offline corrupt; do
  sudo ln -sfn "/var/spool/smtpd/$d" "/$d"
done

# Start stunnel (TLS front, 8025 -> 8026) and smtpd
echo "Starting stunnel (8025 -> 127.0.0.1:8026)"
sudo stunnel /etc/stunnel/stunnel.conf >/tmp/stunnel.log 2>&1 &
STUNNEL_PID=$!

echo "Starting smtpd (-d -v -f ${SMTPD_CONF}, listens on 8026)"
sudo smtpd -d -v -f "${SMTPD_CONF}" >/tmp/smtpd.log 2>&1 &
SMTPD_PID=$!

# Wait until 8026 and 8025 are ready.
port_open() { (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null && { exec 3>&- 3<&-; return 0; }; return 1; }

echo "Waiting for smtpd (8026) and stunnel (8025) to accept connections"
READY=0
for i in $(seq 1 40); do
  if port_open 8026 && port_open 8025; then
    READY=1
    break
  fi
  sleep 0.5
done
if [ "${READY}" -ne 1 ]; then
  echo "Ports not ready (8026 open: $(port_open 8026 && echo yes || echo no), 8025 open: $(port_open 8025 && echo yes || echo no)); continuing to attempt report" >&2
  echo "---- smtpd.log ----" >&2; tail -n 40 /tmp/smtpd.log >&2 || true
  echo "---- stunnel.log ----" >&2; tail -n 40 /tmp/stunnel.log >&2 || true
else
  echo "Ports 8026 and 8025 are ready"
fi

# Run the Fandango, time-bounded so it always returns.
cd "${FANDANGO_DIR}"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "NO_MESSAGES=1: baseline run, NOT sending any SMTP messages"
  sleep "${BASELINE_IDLE:-3}"
else
  echo "Running Fandango smtp.py (grammar=${FANDANGO_FAN:-smtp_client.fan}) for up to ${FANDANGO_DURATION}s"
  timeout "${FANDANGO_DURATION}" python3.11 smtp.py ${FANDANGO_FAN:+"$FANDANGO_FAN"} "$@" || true
  echo "Fandango run finished"
fi

# Flush gcov from every privsep process; each dumps into a per-pid GCOV_PREFIX tree.
COV_RAW="/cov_raw"
sudo rm -rf "$COV_RAW" 2>/dev/null || true
sudo mkdir -p "$COV_RAW"; sudo chmod 1777 "$COV_RAW"

echo "Flushing coverage: SIGUSR1 to ALL smtpd processes (per-pid GCOV_PREFIX)"
sudo pkill -USR1 -x smtpd 2>/dev/null || true

# Wait for everything to dump and exit.
for i in $(seq 1 30); do
  sudo pgrep -x smtpd >/dev/null 2>&1 || break
  sleep 0.5
done
if sudo pgrep -x smtpd >/dev/null 2>&1; then
  echo "smtpd still alive after SIGUSR1; sending SIGTERM"
  sudo pkill -TERM -x smtpd 2>/dev/null || true
  for i in $(seq 1 10); do
    sudo pgrep -x smtpd >/dev/null 2>&1 || break
    sleep 0.5
  done
fi
if sudo pgrep -x smtpd >/dev/null 2>&1; then
  echo "smtpd still alive after SIGTERM; sending SIGKILL"
  sudo pkill -KILL -x smtpd 2>/dev/null || true
fi

# Stop stunnel.
sudo pkill -x stunnel 2>/dev/null || true
kill "${STUNNEL_PID}" "${SMTPD_PID}" 2>/dev/null || true

# Make sure all dumped files are readable/owned by the ubuntu user.
sudo chown -R "$(id -u):$(id -g)" "$COV_RAW" "${BUILD_DIR}" 2>/dev/null || true

# Merge the per-pid gcda trees with gcov-tool.
GCOV_TOOL="$(command -v gcov-tool || command -v gcov-tool-12 || command -v gcov-tool-11 || true)"
echo "gcov-tool: ${GCOV_TOOL:-not found}"
ACC="/home/ubuntu/cov_acc"
sudo rm -rf "$ACC" 2>/dev/null || true
PID_TREES=""
for d in "$COV_RAW"/*; do
  [ -d "$d" ] || continue
  # The per-pid tree mirrors the absolute build path beneath $d.
  sub="$d${BUILD_DIR}"
  [ -d "$sub" ] || continue
  PID_TREES="$PID_TREES $sub"
done
echo "per-pid gcda trees found:$(echo "$PID_TREES" | wc -w | tr -d ' ')"

if [ -n "$GCOV_TOOL" ] && [ -n "$PID_TREES" ]; then
  for tree in $PID_TREES; do
    if [ ! -d "$ACC" ]; then
      cp -a "$tree" "$ACC"
    else
      if "$GCOV_TOOL" merge "$ACC" "$tree" -o "${ACC}.new" >/dev/null 2>&1; then
        rm -rf "$ACC"; mv "${ACC}.new" "$ACC"
      fi
    fi
  done
  if [ -d "$ACC" ]; then
    ( cd "$ACC" && find . -name '*.gcda' | while IFS= read -r f; do
        cp -f "$f" "${BUILD_DIR}/$f" 2>/dev/null || true
      done )
    echo "Merged per-pid coverage into build tree"
  fi
else
  echo "gcov-tool/per-pid trees unavailable; falling back to whatever is in build tree"
fi

GCDA_COUNT="$(find "${BUILD_DIR}/${GCOV_SUBDIR}" -name '*.gcda' 2>/dev/null | wc -l | tr -d ' ')"
echo ".gcda files in build tree under ${GCOV_SUBDIR}: ${GCDA_COUNT}"

# Produce the report
echo "Generating coverage report into ${COV_OUT_DIR}"
cd "${BUILD_DIR}"

# Human-readable summary -> coverage.txt
gcovr -r "${BUILD_DIR}" --filter "${GCOV_SUBDIR}/" -s \
  > "${COV_OUT_DIR}/coverage.txt" 2>/dev/null || true

echo "---- coverage.txt ----"
cat "${COV_OUT_DIR}/coverage.txt" 2>/dev/null || true

# HTML report
gcovr -r "${BUILD_DIR}" --filter "${GCOV_SUBDIR}/" \
  --html --html-details \
  -o "${COV_OUT_DIR}/index.html" 2>/dev/null || true

# Per-file table
gcovr -r "${BUILD_DIR}" --filter "${GCOV_SUBDIR}/" \
  > "${COV_OUT_DIR}/coverage_files.txt" 2>/dev/null || true

python3.11 - "${BUILD_DIR}" "${GCOV_SUBDIR}/" "${COV_OUT_DIR}/summary.csv" <<'PYEOF'
import re
import subprocess
import sys

build_dir, filt, out_csv = sys.argv[1], sys.argv[2], sys.argv[3]

try:
    out = subprocess.run(
        ["gcovr", "-r", build_dir, "--filter", filt, "-s"],
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

echo "---- summary.csv ----"
cat "${COV_OUT_DIR}/summary.csv" 2>/dev/null || true

echo "Coverage report written to ${COV_OUT_DIR}"
ls -la "${COV_OUT_DIR}" || true

exit 0
