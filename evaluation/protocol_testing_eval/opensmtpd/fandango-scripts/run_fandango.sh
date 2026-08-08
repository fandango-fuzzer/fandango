#!/bin/bash

set -u

BUILD_DIR="${BUILD_DIR:-/home/ubuntu/OpenSMTPD-7.7.0p0}"
SMTPD_CONF="${SMTPD_CONF:-/etc/smtpd.conf}"
GCOV_SUBDIR="usr.sbin/smtpd"           # sources we care about, relative to BUILD_DIR
COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
COV_OUT_DIR="${COV_OUT_DIR%/}/"
FANDANGO_DURATION="${FANDANGO_DURATION:-120}"
RUN_FANDANGO_TIMEOUT="${RUN_FANDANGO_TIMEOUT:-600}"
FANDANGO_DIR="/home/ubuntu/fandango"

mkdir -p "${COV_OUT_DIR}"

# Watchdog: kill the whole process group if the run times out.
(
  sleep "${RUN_FANDANGO_TIMEOUT}"
  echo "watchdog timeout reached, killing process group" >&2
  kill -TERM -- "-$$" 2>/dev/null || true
  sleep 30
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

# Run the Fandango, time-bounded.
cd "${FANDANGO_DIR}"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "NO_MESSAGES=1: baseline run, NOT sending any messages"
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

# Run gcovr from the build root so --filter (matched relative to --root) scopes
# the report to usr.sbin/smtpd/.
echo "writing coverage report to $COV_OUT_DIR"
cd "${BUILD_DIR}"

# Remove coverage artifacts gcov cannot read, which would otherwise abort the
# report: everything outside usr.sbin/smtpd/ (openbsd-compat, conftest.*, ...),
# and never-executed helpers (mail.lmtp, makemap, ...) whose .gcda is missing.
find "${BUILD_DIR}" \( -name '*.gcda' -o -name '*.gcno' \) -not -path "*/${GCOV_SUBDIR}/*" -delete 2>/dev/null || true
find "${BUILD_DIR}/${GCOV_SUBDIR}" -name '*.gcno' 2>/dev/null | while read -r gcno; do
  [ -s "${gcno%.gcno}.gcda" ] || rm -f "$gcno"
done

# export coverage
gcovr -r "${BUILD_DIR}" --filter "${GCOV_SUBDIR}/" --csv -o "${COV_OUT_DIR}coverage_branches.csv" || true

echo "artifacts:"; ls -la "$COV_OUT_DIR" || true
echo "done"