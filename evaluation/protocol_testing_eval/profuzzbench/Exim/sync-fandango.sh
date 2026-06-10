#!/bin/bash
# Copy the LOCAL Fandango checkout (the current branch on this disk) into the
# Docker build context so Dockerfile-fandango can install it, instead of cloning
# the io_replication branch from GitHub. Run this before building the image.

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
DEST="$HERE/.fandango-local"

if ! grep -q "fandango-fuzzer" "$REPO_ROOT/pyproject.toml" 2>/dev/null; then
  echo "ERROR: $REPO_ROOT does not look like the Fandango repo root" >&2
  exit 1
fi

branch="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
echo "Syncing Fandango ($branch) from $REPO_ROOT -> $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"
rsync -a \
  --exclude '.git' --exclude '.venv' --exclude 'evaluation' --exclude 'docs' \
  --exclude '_build' --exclude 'node_modules' --exclude '__pycache__' \
  --exclude '.mypy_cache' --exclude '.pytest_cache' --exclude '*.egg-info' \
  --exclude 'build' --exclude 'dist' --exclude '*.so' \
  "$REPO_ROOT"/ "$DEST"/
echo "Done. $(du -sh "$DEST" | cut -f1) copied to $DEST"
