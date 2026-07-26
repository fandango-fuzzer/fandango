#!/bin/bash
#
# Build a target's instrumented-server image, and runs Fandango on it within docker.
#   ./run_coverage.sh <target> [results_dir] [driver flags...]
#   target       bind9 | opensmtpd | wireguard | lightftp
#   results_dir  where the report lands (default: ./results-<target>)
#   driver flags --experiment --duration --guidance --interval --run-id
#                --plateau-timeout --skip-build

set -eo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# arguments
target="${1:-}"
if [ -z "$target" ]; then
  echo "usage: $0 <bind9|opensmtpd|wireguard|lightftp> [results_dir] [driver flags...]" >&2
  exit 2
fi
shift

target_dir="$here/$target"
if [ ! -f "$target_dir/Dockerfile-fandango" ]; then
  echo "unknown target: $target" >&2
  exit 1
fi

# The first argument is the results dir, unless it's already a --flag.
results_dir="$here/results-$target"
case "${1:-}" in
  ""|--*) ;;
  *) results_dir="$1"; shift ;;
esac

# Remaining arguments are flags for the driver in the container. We consume
# --skip-build ourselves and note --duration so we can contigure the timeout.
driver_flags=()
meas_duration=""
while [ $# -gt 0 ]; do
  case "$1" in
    --skip-build)
      SKIP_BUILD=1; shift ;;
    --duration)
      meas_duration="$2"; driver_flags+=("$1" "$2"); shift 2 ;;
    --experiment|--guidance|--interval|--run-id|--plateau-timeout)
      driver_flags+=("$1" "$2"); shift 2 ;;
    *)
      echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

# Tell the driver where to write coverage.
if [ ${#driver_flags[@]} -gt 0 ]; then
  driver_flags+=(--out-dir /home/ubuntu/cov_out)
fi

mkdir -p "$results_dir"
results_dir="$(cd "$results_dir" && pwd)"
image="$target-fandango"

# build
if [ "${SKIP_BUILD:-0}" = "1" ]; then
  echo "reusing image $image:latest"
else
  echo "building $image from $target_dir (local fandango checkout)"

  # CACHEBUST invalidates the layer that copies in the local checkout whenever
  # the git head changes
  cachebust="${CACHEBUST:-$(git -C "$here" rev-parse HEAD 2>/dev/null || echo 0)}"

  if "$here/stage_fandango.sh" "$target_dir" &&
     docker build "$target_dir" -f "$target_dir/Dockerfile-fandango" \
       --build-arg "CACHEBUST=$cachebust" -t "$image:latest"; then
    rm -rf "$target_dir/_fandango_src"
  else
    rc=$?
    rm -rf "$target_dir/_fandango_src"
    exit "$rc"
  fi
fi

# timeouts
# While measuring (--duration given) the budgets track the requested duration.
# Otherwise fall back to fixed defaults.
if [ -n "$meas_duration" ]; then
  : "${FANDANGO_DURATION:=$((meas_duration + 180))}"
  : "${OVERALL_TIMEOUT:=$((meas_duration + 480))}"
fi
: "${FANDANGO_DURATION:=120}"
: "${OVERALL_TIMEOUT:=1800}"
: "${RUN_FANDANGO_TIMEOUT:=$((FANDANGO_DURATION + 120))}"

# run
# Per-target extra docker flags, e.g. wireguard's --cap-add / --device.
extra_args=""
if [ -f "$target_dir/docker-args" ]; then
  extra_args="$(grep -v '^[[:space:]]*#' "$target_dir/docker-args" | tr '\n' ' ')"
fi

# Hard-kill the container if it outlives OVERALL_TIMEOUT.
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
# extra_args is a word-split
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

# Container is done. Stop the watchdog.
kill "$watchdog" 2>/dev/null || true
wait "$watchdog" 2>/dev/null || true

if [ "$rc" -ne 0 ]; then
  echo "container exited with code $rc (collecting whatever coverage was produced)"
fi

# report
echo
echo "report for $target in $results_dir:"
ls -la "$results_dir"
if [ -f "$results_dir/coverage.txt" ]; then
  echo "---- coverage.txt ----"
  cat "$results_dir/coverage.txt"
fi