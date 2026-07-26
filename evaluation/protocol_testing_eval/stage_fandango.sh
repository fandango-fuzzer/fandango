#!/bin/bash
# Stage the locally checked-out fandango code into <target_dir>/_fandango_src

set -euo pipefail

target_dir=${1:?usage: stage_fandango.sh <target_dir>}
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$here" rev-parse --show-toplevel)"
dest="$target_dir/_fandango_src"

rm -rf "$dest"
mkdir -p "$dest"
rsync -a \
  --exclude='.git' \
  --exclude='.venv' \
  --exclude='_build' \
  --exclude='build' \
  --exclude='evaluation' \
  --exclude='__pycache__' \
  --exclude='*.egg-info' \
  --exclude='*.so' \
  --exclude='*.dylib' \
  --exclude='*.pyd' \
  --exclude='.mypy_cache' \
  --exclude='.pytest_cache' \
  --exclude='.ruff_cache' \
  --exclude='.benchmarks' \
  --exclude='.DS_Store' \
  "$repo_root/" "$dest/"
