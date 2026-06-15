#!/usr/bin/env bash
set -euo pipefail

# D-10: Agent governance projection drift
# Local wrapper for the canonical sentinel-shared implementation.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SENTINEL_SCRIPT=""

for candidate in \
  "$ROOT_DIR/../sentinel-shared/scripts/precheck-agent-governance.sh" \
  "$ROOT_DIR/.sentinel-shared/scripts/precheck-agent-governance.sh"
do
  if [ -f "$candidate" ]; then
    SENTINEL_SCRIPT="$candidate"
    break
  fi
done

if [ -z "$SENTINEL_SCRIPT" ]; then
  echo "D-10 BLOCKED: missing canonical sentinel-shared/scripts/precheck-agent-governance.sh" >&2
  echo "Expected sibling repo: $ROOT_DIR/../sentinel-shared" >&2
  echo "Expected CI checkout: $ROOT_DIR/.sentinel-shared" >&2
  exit 2
fi

cd "$ROOT_DIR"
exec bash "$SENTINEL_SCRIPT"
