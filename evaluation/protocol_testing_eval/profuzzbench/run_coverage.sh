#!/usr/bin/env bash
# Usage:
#   ./run_coverage.sh <target> [results_dir]
#
#   <target>: bind9 | opensmtpd | wireguard | lightftp
#   [results_dir]: host directory the coverage report is written to (default: ./results-<target>)
#
# Optional environment overrides:
#   FANDANGO_DURATION: seconds Fandango drives the server (default 120)
#   OVERALL_TIMEOUT: host watchdog: hard-kill the container (default 1800)
#   NO_MESSAGES=1: baseline run: start server, send nothing (default 0)
#   BASELINE_IDLE: idle seconds for a baseline run (default 3)
#   FANDANGO_FAN: override the grammar the driver loads from the container's
#                 fandango-scripts folder, e.g.
#                 FANDANGO_FAN=other.fan ./run_coverage.sh bind9

set -eo pipefail

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  echo "usage: $0 <bind9|opensmtpd|wireguard|lightftp> [results_dir]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${SCRIPT_DIR}/${TARGET}"
if [ ! -f "${TARGET_DIR}/Dockerfile-fandango" ]; then
  echo "Unknown target '${TARGET}' (no ${TARGET_DIR}/Dockerfile-fandango)" >&2
  exit 1
fi

RESULTS_DIR="${2:-${SCRIPT_DIR}/results-${TARGET}}"
mkdir -p "$RESULTS_DIR"
RESULTS_DIR="$(cd "$RESULTS_DIR" && pwd)"

IMAGE="${TARGET}-fandango"

# Optional per-target extra `docker run` flags (one flag per line).
EXTRA_ARGS=""
if [ -f "${TARGET_DIR}/docker-args" ]; then
  EXTRA_ARGS="$(grep -v '^[[:space:]]*#' "${TARGET_DIR}/docker-args" | tr '\n' ' ')"
fi

echo "Building image ${IMAGE} from ${TARGET_DIR} ..."
docker build "${TARGET_DIR}" -f "${TARGET_DIR}/Dockerfile-fandango" -t "${IMAGE}:latest"

# Overall watchdog: never let the run hang forever. Kill the
# container after OVERALL_TIMEOUT seconds.
CONTAINER="${TARGET}-fandango-run-$$"
OVERALL_TIMEOUT="${OVERALL_TIMEOUT:-1800}"
(
  sleep "$OVERALL_TIMEOUT"
  if [ -n "$(docker ps -q -f "name=^${CONTAINER}$")" ]; then
    echo "OVERALL_TIMEOUT (${OVERALL_TIMEOUT}s) reached - killing ${CONTAINER}" >&2
    docker kill "$CONTAINER" >/dev/null 2>&1 || true
  fi
) &
WATCHDOG=$!

echo "Running ${TARGET} coverage (timeout ${OVERALL_TIMEOUT}s); report -> ${RESULTS_DIR}"
RUN_RC=0
# shellcheck disable=SC2086
docker run --rm --name "$CONTAINER" \
  -v "${RESULTS_DIR}:/home/ubuntu/cov_out" \
  -e COV_OUT_DIR=/home/ubuntu/cov_out \
  -e "NO_MESSAGES=${NO_MESSAGES:-0}" \
  -e "FANDANGO_DURATION=${FANDANGO_DURATION:-120}" \
  -e "BASELINE_IDLE=${BASELINE_IDLE:-3}" \
  -e "FANDANGO_FAN=${FANDANGO_FAN:-}" \
  ${EXTRA_ARGS} \
  "${IMAGE}:latest" \
  /home/ubuntu/fandango/run_fandango.sh || RUN_RC=$?

kill "$WATCHDOG" 2>/dev/null || true
wait "$WATCHDOG" 2>/dev/null || true
[ "$RUN_RC" -eq 0 ] || echo "container exited with code ${RUN_RC} (collecting any coverage produced)"

echo
echo "Coverage report for ${TARGET} written to ${RESULTS_DIR}:"
ls -la "${RESULTS_DIR}"
if [ -f "${RESULTS_DIR}/coverage.txt" ]; then
  echo "---- coverage.txt ----"
  cat "${RESULTS_DIR}/coverage.txt"
fi
