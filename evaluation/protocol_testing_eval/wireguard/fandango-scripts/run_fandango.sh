#!/bin/bash
# In-container entry point for the WireGuard (boringtun) Fandango target.

set -uo pipefail

COV_OUT_DIR="${COV_OUT_DIR:-/home/ubuntu/cov_out}"
if [[ ! "$COV_OUT_DIR" =~ ^/ ]]; then
  COV_OUT_DIR="/home/ubuntu/${COV_OUT_DIR}"
fi
mkdir -p "$COV_OUT_DIR"

BORINGTUN_BIN="${BORINGTUN_BIN:-/opt/boringtun/target/release/boringtun-cli}"
WG_CONFIG_DIR="${WG_CONFIG_DIR:-/home/ubuntu/wg-config}"
WG_IF="wg0"
WG_PORT="${WG_PORT:-51820}"
WG_ADDR="10.13.13.1/24"

FANDANGO_DIR="/home/ubuntu/fandango"
PROFRAW_DIR="$(mktemp -d /tmp/wg-profraw.XXXXXX)"
export LLVM_PROFILE_FILE="${PROFRAW_DIR}/cov-%p-%m.profraw"

FANDANGO_DURATION="${FANDANGO_DURATION:-120}"
SHUTDOWN_WAIT="${SHUTDOWN_WAIT:-15}"

echo "COV_OUT_DIR=$COV_OUT_DIR"
echo "BORINGTUN_BIN=$BORINGTUN_BIN"
echo "LLVM_PROFILE_FILE=$LLVM_PROFILE_FILE"

# Watchdog: kill the whole process group if the run wedges, so the container
# always exits and the host can still collect coverage.
RUN_FANDANGO_TIMEOUT="${RUN_FANDANGO_TIMEOUT:-600}"
(
  sleep "$RUN_FANDANGO_TIMEOUT"
  echo "watchdog timeout reached, killing process group" >&2
  kill -TERM -$$ 2>/dev/null || true
  sleep 30
  kill -KILL -$$ 2>/dev/null || true
) &
watchdog=$!
trap 'kill "$watchdog" 2>/dev/null || true' EXIT

# Bring up boringtun wg0
BORINGTUN_PID=""
TUN_OK=0

ensure_tun_node() {
  if [ ! -e /dev/net/tun ]; then
    mkdir -p /dev/net || true
    mknod /dev/net/tun c 10 200 2>/dev/null || true
    chmod 600 /dev/net/tun 2>/dev/null || true
  fi
}

start_boringtun() {
  TUN_OK=0
  ensure_tun_node

  # boringtun-cli runs the userspace WG device. --foreground keeps it attached so
  # the LLVM profiling runtime can flush on a graceful SIGTERM/SIGINT (atexit).
  echo "starting boringtun on ${WG_IF} ..."
  "$BORINGTUN_BIN" --foreground --disable-drop-privileges --verbosity debug "$WG_IF" \
      > "${PROFRAW_DIR}/boringtun.log" 2>&1 &
  BORINGTUN_PID=$!
  echo "boringtun pid=$BORINGTUN_PID"

  # Wait for the wg0 interface to appear.
  local i
  for i in $(seq 1 40); do
    if ip link show "$WG_IF" >/dev/null 2>&1; then
      TUN_OK=1
      break
    fi
    if ! kill -0 "$BORINGTUN_PID" 2>/dev/null; then
      echo "boringtun exited early; log:" >&2
      cat "${PROFRAW_DIR}/boringtun.log" >&2 || true
      return 1
    fi
    sleep 0.25
  done

  if [ "$TUN_OK" -ne 1 ]; then
    echo "wg0 interface did not appear (TUN unavailable?)." >&2
    cat "${PROFRAW_DIR}/boringtun.log" >&2 || true
    return 1
  fi
  echo "wg0 is up."
  return 0
}

configure_wg() {
  # Retry until 'wg show' confirms BOTH the listen port and the peer are configured.
  local i
  for i in $(seq 1 60); do
    wg setconf "$WG_IF" "${WG_CONFIG_DIR}/wg0.conf" 2>/dev/null
    if wg show "$WG_IF" 2>/dev/null | grep -q "listening port: ${WG_PORT}" \
       && wg show "$WG_IF" 2>/dev/null | grep -q "^peer:"; then
      # Interface address + link up so the container kernel answers ICMP to 10.13.13.1.
      ip addr add "$WG_ADDR" dev "$WG_IF" 2>/dev/null || true
      ip link set "$WG_IF" up 2>/dev/null || true
      echo "wg0 configured:"
      wg show "$WG_IF" 2>/dev/null || true
      ip addr show "$WG_IF" 2>/dev/null || true
      return 0
    fi
    if ! kill -0 "$BORINGTUN_PID" 2>/dev/null; then
      echo "boringtun exited during config; log:" >&2
      cat "${PROFRAW_DIR}/boringtun.log" >&2 || true
      return 1
    fi
    sleep 0.5
  done
  echo "wg setconf did not take after retries (no 'listening port: ${WG_PORT}'); wg show:" >&2
  wg show "$WG_IF" >&2 2>/dev/null || true
  return 1
}

wait_for_udp_port() {
  # Bounded wait until boringtun has bound the UDP listen port.
  local i
  for i in $(seq 1 40); do
    if ss -lun 2>/dev/null | grep -q ":${WG_PORT}\b" || \
       netstat -lun 2>/dev/null | grep -q ":${WG_PORT} "; then
      echo "udp/${WG_PORT} is bound."
      return 0
    fi
    sleep 0.25
  done
  echo "udp/${WG_PORT} not observed bound (continuing anyway)." >&2
  return 1
}

BOOT_OK=0
for attempt in 1 2 3; do
  if start_boringtun && configure_wg; then
    BOOT_OK=1
    wait_for_udp_port || true   # informational: wg show already confirmed the port
    break
  fi
  echo "boringtun bring-up attempt ${attempt} failed; restarting boringtun ..." >&2
  if [ -n "$BORINGTUN_PID" ] && kill -0 "$BORINGTUN_PID" 2>/dev/null; then
    kill -TERM "$BORINGTUN_PID" 2>/dev/null || true
    wait "$BORINGTUN_PID" 2>/dev/null || true
  fi
  ip link del "$WG_IF" 2>/dev/null || true   # drop a lingering wg0 so the next start is clean
  BORINGTUN_PID=""
  sleep 1
done
if [ "$BOOT_OK" -ne 1 ]; then
  echo "boringtun never came up cleanly after retries - Fandango run may exercise little/no code." >&2
fi

# Run Fandango
cd "$FANDANGO_DIR"
if [ "${NO_MESSAGES:-0}" = "1" ]; then
  echo "NO_MESSAGES=1: baseline run, NOT sending any WireGuard messages"
  sleep "${BASELINE_IDLE:-3}"
else
  echo "running Fandango wireguard.py (grammar=${FANDANGO_FAN:-wireguard.fan}) for up to ${FANDANGO_DURATION}s ..."
  timeout "$FANDANGO_DURATION" python3.11 wireguard.py ${FANDANGO_FAN:+"$FANDANGO_FAN"} "$@" || true
  echo "Fandango run finished."
fi

# Graceful (bounded) shutdown so LLVM flushes profraw files on exit
if [ -n "$BORINGTUN_PID" ] && kill -0 "$BORINGTUN_PID" 2>/dev/null; then
  echo "stopping boringtun (pid=$BORINGTUN_PID) gracefully ..."
  kill -TERM "$BORINGTUN_PID" 2>/dev/null || true
  for i in $(seq 1 "$SHUTDOWN_WAIT"); do
    kill -0 "$BORINGTUN_PID" 2>/dev/null || break
    sleep 1
  done
  if kill -0 "$BORINGTUN_PID" 2>/dev/null; then
    echo "boringtun still alive after ${SHUTDOWN_WAIT}s; sending SIGINT then SIGKILL" >&2
    kill -INT "$BORINGTUN_PID" 2>/dev/null || true
    sleep 2
    kill -KILL "$BORINGTUN_PID" 2>/dev/null || true
  fi
  wait "$BORINGTUN_PID" 2>/dev/null || true
fi

# Coverage report
echo "generating coverage report ..."
shopt -s nullglob
PROFRAWS=( "${PROFRAW_DIR}"/*.profraw )
echo "found ${#PROFRAWS[@]} profraw file(s) in ${PROFRAW_DIR}"

PROFDATA="${PROFRAW_DIR}/cov.profdata"

emit_empty_report() {
  local msg="$1"
  echo "${msg}" >&2
  echo "$msg" > "${COV_OUT_DIR}/coverage.txt"
  printf 'metric,percent,covered,total\nlines,0.00,0,0\nbranches,0.00,0,0\n' \
      > "${COV_OUT_DIR}/summary.csv"
  cat > "${COV_OUT_DIR}/index.html" <<HTML
<!DOCTYPE html><html><head><title>WireGuard coverage</title></head>
<body><h1>WireGuard (boringtun) coverage</h1><p>${msg}</p></body></html>
HTML
}

if [ "${#PROFRAWS[@]}" -eq 0 ]; then
  emit_empty_report "No .profraw files were produced - boringtun did not flush coverage (TUN/handshake may have failed)."
else
  if ! llvm-profdata merge -sparse "${PROFRAWS[@]}" -o "$PROFDATA"; then
    emit_empty_report "llvm-profdata merge failed."
  else
    # HTML report
    llvm-cov show "$BORINGTUN_BIN" \
        -instr-profile="$PROFDATA" \
        -format=html \
        -show-branches=count \
        -show-line-counts-or-regions \
        -output-dir="$COV_OUT_DIR" 2>/dev/null || true
    # llvm-cov writes index.html under -output-dir; ensure it exists.
    if [ ! -f "${COV_OUT_DIR}/index.html" ]; then
      # Some llvm-cov versions place it differently; try to find one.
      ALT="$(find "$COV_OUT_DIR" -maxdepth 2 -name 'index.html' | head -n1)"
      if [ -n "$ALT" ] && [ "$ALT" != "${COV_OUT_DIR}/index.html" ]; then
        cp "$ALT" "${COV_OUT_DIR}/index.html"
      fi
    fi
    # Drop the per-source-file HTML tree (mirrors /opt/boringtun absolute paths); keep index.html.
    rm -rf "${COV_OUT_DIR}/coverage"

    # Human-readable text report (line + branch).
    llvm-cov report "$BORINGTUN_BIN" \
        -instr-profile="$PROFDATA" \
        -show-branch-summary \
        > "${COV_OUT_DIR}/coverage.txt" 2>/dev/null || \
      llvm-cov report "$BORINGTUN_BIN" -instr-profile="$PROFDATA" \
        > "${COV_OUT_DIR}/coverage.txt" 2>/dev/null || true

    # summary.csv derived from llvm-cov export JSON totals (lines + branches).
    llvm-cov export "$BORINGTUN_BIN" -instr-profile="$PROFDATA" -format=text \
        > "${PROFRAW_DIR}/cov.json" 2>/dev/null || true

    python3.11 - "$PROFRAW_DIR/cov.json" "$COV_OUT_DIR/summary.csv" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
def row(name, d):
    cov = d.get("covered", 0); tot = d.get("count", 0)
    pct = d.get("percent", (100.0*cov/tot if tot else 0.0))
    return f"{name},{pct:.2f},{cov},{tot}\n"
lines_t = {"covered":0,"count":0,"percent":0.0}
branch_t = {"covered":0,"count":0,"percent":0.0}
try:
    with open(src) as f:
        data = json.load(f)
    tot = data["data"][0]["totals"]
    lines_t = tot.get("lines", lines_t)
    branch_t = tot.get("branches", branch_t)
except Exception as e:
    sys.stderr.write(f"[summary.csv] could not parse export json: {e}\n")
with open(dst, "w") as f:
    f.write("metric,percent,covered,total\n")
    f.write(row("lines", lines_t))
    f.write(row("branches", branch_t))
PY

    echo "---- summary.csv ----"
    cat "${COV_OUT_DIR}/summary.csv" || true
  fi
fi

# Make outputs readable on the host.
chmod -R a+rX "$COV_OUT_DIR" 2>/dev/null || true

echo "done. Report in ${COV_OUT_DIR}"
ls -la "$COV_OUT_DIR" || true
exit 0
