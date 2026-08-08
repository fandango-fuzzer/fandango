#!/bin/bash
# Run an experiment over the targets, one container per run.
# The image is built once per target. Runs go up to --concurrency at a time and
# write to experiments/<target>/<condition>/run_<n>/ (logs + code coverage).
#
#   ./run_experiments.sh <target|all> <throughput|coverage> \
#       [--runs N] [--concurrency C] [--duration S] [--interval I] [--plateau S] [--start-run N]
# targets are: bind9, lightftp, opensmtpd, wireguard
set -uo pipefail
cd "$(dirname "$0")"

usage() {
  echo "usage: $0 <target|all> <throughput|coverage> [--runs N] [--concurrency C] [--duration S] [--interval I] [--plateau S] [--start-run N]"
  exit 2
}

target=${1:-}
experiment=${2:-}
[ -n "$target" ] && [ -n "$experiment" ] || usage
shift 2

runs=10
concurrency=2
duration=3600
interval=20
plateau=""
start_run=""
while [ $# -gt 0 ]; do
  case $1 in
    --runs)        runs=$2 ;;
    --concurrency) concurrency=$2 ;;
    --duration)    duration=$2 ;;
    --interval)    interval=$2 ;;
    --plateau)     plateau=$2 ;;
    --start-run)   start_run=$2 ;;
    *) usage ;;
  esac
  shift 2
done

plateau_opt=""
[ -n "$plateau" ] && plateau_opt="--plateau-timeout $plateau"

case $experiment in
  throughput) conditions="1:throughput" ;;
  coverage)   conditions="1:coverage_guided 0:coverage_unguided" ;;
  *) usage ;;
esac

[ "$target" = all ] && targets="opensmtpd bind9 lightftp wireguard" || targets="$target"

for t in $targets; do
  [ -f "$t/Dockerfile-fandango" ] || { echo "no such target: $t" >&2; continue; }

  echo "building $t (from local fandango checkout)"
  ./stage_fandango.sh "$t" || { echo "failed to stage local fandango for $t" >&2; continue; }
  docker build "$t" -f "$t/Dockerfile-fandango" \
    --build-arg CACHEBUST="$(git rev-parse HEAD 2>/dev/null)" -t "$t-fandango:latest"
  build_rc=$?
  rm -rf "$t/_fandango_src"
  [ $build_rc -eq 0 ] || continue

  if [ -n "$start_run" ]; then
    first=$start_run
  else
    first=1
    for c in $conditions; do
      condition=${c#*:}
      for d in "experiments/$t/$condition"/run_*; do
        [ -d "$d" ] || continue
        num=${d##*/run_}
        case $num in *[!0-9]*) continue ;; esac
        [ "$num" -ge "$first" ] && first=$((num + 1))
      done
    done
  fi
  last=$((first + runs - 1))
  echo "  runs $first..$last"

  for c in $conditions; do
    guidance=${c%%:*}
    condition=${c#*:}
    for n in $(seq "$first" "$last"); do
      while [ "$(jobs -r | wc -l)" -ge "$concurrency" ]; do sleep 1; done
      dir="experiments/$t/$condition/run_$n"
      mkdir -p "$dir"
      echo "  $condition run $n"
      ./run_coverage.sh "$t" "$dir" --skip-build \
        --experiment "$experiment" --duration "$duration" \
        --guidance "$guidance" --interval "$interval" --run-id "$n" \
        $plateau_opt \
        > "$dir/run.log" 2>&1 &
    done
  done
  wait
  echo "done $t -> experiments/$t"
done
