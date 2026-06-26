#!/usr/bin/env bash
# Build a target's instrumented-server image, run Fandango against it in a
# container, and collect the code-coverage report.
#
#   ./run_coverage.sh <target> [results_dir] [driver flags]
#
# target       bind9 | opensmtpd | wireguard | lightftp
# results_dir  where the report lands (default: ./results-<target>)
# driver flags --experiment X --duration S --guidance G --interval I --run-id N
#              passed straight through to the in-container driver (see run_experiments.sh)
#
# Env knobs: FANDANGO_DURATION, OVERALL_TIMEOUT, NO_MESSAGES, BASELINE_IDLE,
#            FANDANGO_FAN (grammar override), SKIP_BUILD=1 (reuse the image).

set -eo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

target="${1:-}"
if [ -z "$target" ]; then
  echo "usage: $0 <bind9|opensmtpd|wireguard|lightftp> [results_dir] [--experiment X --duration S ...]" >&2
  exit 2
fi
shift

target_dir="$here/$target"
[ -f "$target_dir/Dockerfile-fandango" ] || { echo "unknown target: $target" >&2; exit 1; }

# A leading non-flag argument is the results dir; everything after it goes to the driver.
results_dir="$here/results-$target"
if [ $# -gt 0 ] && [ "${1#--}" = "$1" ]; then results_dir="$1"; shift; fi

driver_flags=()
meas_duration=""
while [ $# -gt 0 ]; do
  case "$1" in
    --duration) meas_duration="$2"; driver_flags+=("$1" "$2"); shift 2;;
    --experiment|--guidance|--interval|--run-id|--plateau-timeout) driver_flags+=("$1" "$2"); shift 2;;
    --skip-build) SKIP_BUILD=1; shift;;
    *) echo "unknown option: $1" >&2; exit 2;;
  esac
done
[ ${#driver_flags[@]} -gt 0 ] && driver_flags+=(--out-dir /home/ubuntu/cov_out)

mkdir -p "$results_dir"
results_dir="$(cd "$results_dir" && pwd)"
image="$target-fandango"

# Build the image from the local fandango checkout (CACHEBUST busts the layer
# when HEAD moved). Skip with SKIP_BUILD=1.
if [ "${SKIP_BUILD:-0}" = "1" ]; then
  echo "reusing image $image:latest"
else
  echo "building $image from $target_dir (local fandango checkout)"
  cachebust="${CACHEBUST:-$(git -C "$here" rev-parse HEAD 2>/dev/null || echo 0)}"
  "$here/_stage_fandango.sh" "$target_dir"
  docker build "$target_dir" -f "$target_dir/Dockerfile-fandango" \
    --build-arg "CACHEBUST=$cachebust" -t "$image:latest"
  build_rc=$?
  rm -rf "$target_dir/_fandango_src"
  [ $build_rc -eq 0 ] || exit $build_rc
fi

# Watchdog budgets: derive from --duration when measuring, otherwise use the defaults.
if [ -n "$meas_duration" ]; then
  FANDANGO_DURATION="${FANDANGO_DURATION:-$((meas_duration + 180))}"
  OVERALL_TIMEOUT="${OVERALL_TIMEOUT:-$((meas_duration + 480))}"
fi
FANDANGO_DURATION="${FANDANGO_DURATION:-120}"
OVERALL_TIMEOUT="${OVERALL_TIMEOUT:-1800}"
RUN_FANDANGO_TIMEOUT="${RUN_FANDANGO_TIMEOUT:-$((FANDANGO_DURATION + 120))}"

# Per-target extra docker flags (e.g. wireguard's --cap-add / --device).
extra_args=""
[ -f "$target_dir/docker-args" ] && extra_args="$(grep -v '^[[:space:]]*#' "$target_dir/docker-args" | tr '\n' ' ')"

# Host watchdog: hard-kill the container if it outlives OVERALL_TIMEOUT.
container="$target-fandango-run-$$"
(
  sleep "$OVERALL_TIMEOUT"
  if [ -n "$(docker ps -q -f "name=^${container}$")" ]; then
    echo "timeout ${OVERALL_TIMEOUT}s reached, killing $container" >&2
    docker kill "$container" >/dev/null 2>&1 || true
  fi
) &
watchdog=$!

echo "running $target (timeout ${OVERALL_TIMEOUT}s); report -> $results_dir"
rc=0
# shellcheck disable=SC2086
docker run --rm --name "$container" \
  -v "$results_dir:/home/ubuntu/cov_out" \
  -e COV_OUT_DIR=/home/ubuntu/cov_out \
  -e "NO_MESSAGES=${NO_MESSAGES:-0}" \
  -e "FANDANGO_DURATION=$FANDANGO_DURATION" \
  -e "RUN_FANDANGO_TIMEOUT=$RUN_FANDANGO_TIMEOUT" \
  -e "BASELINE_IDLE=${BASELINE_IDLE:-3}" \
  -e "FANDANGO_FAN=${FANDANGO_FAN:-}" \
  $extra_args \
  "$image:latest" \
  /home/ubuntu/fandango/run_fandango.sh "${driver_flags[@]}" || rc=$?

kill "$watchdog" 2>/dev/null || true
wait "$watchdog" 2>/dev/null || true
[ "$rc" -eq 0 ] || echo "container exited with code $rc (collecting whatever coverage was produced)"

echo
echo "report for $target in $results_dir:"
ls -la "$results_dir"
[ -f "$results_dir/coverage.txt" ] && { echo "---- coverage.txt ----"; cat "$results_dir/coverage.txt"; }
