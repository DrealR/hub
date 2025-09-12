#!/usr/bin/env bash
set -euo pipefail

# Append/merge an "assistant" preferences block into ~/.gemini/settings.json.
# - Idempotent (checks for __profileVersion watermark v1)
# - No sudo; only touches user settings
# - Requires jq (prints guidance if missing)

GEMINI_DIR="$HOME/.gemini"
SETTINGS="$GEMINI_DIR/settings.json"
SRC="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/tools/cdx/agents/assistant-preferences.json"

usage() {
  cat <<'USAGE'
Usage: tools/cdx/scripts/setup-agent-preferences.sh [--dry-run]

Adds an "assistant" preferences block to ~/.gemini/settings.json.
Idempotent: skips if __profileVersion=v1 is present.

Flags:
  --dry-run   Print actions without changing files
USAGE
}

DRY=false
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $a" >&2; usage; exit 2 ;;
  esac
done

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required to merge JSON. Please install jq (see tools/cdx/agents/fast-tools.md)." >&2
  exit 1
fi

mkdir -p "$GEMINI_DIR"
touch "$SETTINGS"
if [ ! -s "$SETTINGS" ]; then echo '{}' > "$SETTINGS"; fi

if jq -e '.assistant.__profileVersion == "v1"' "$SETTINGS" >/dev/null 2>&1; then
  echo "Assistant preferences already present (v1) — nothing to do."
  exit 0
fi

BK="$SETTINGS.bak.$(date +%s)"
cp "$SETTINGS" "$BK"
echo "Backed up current settings to $BK"

merged=$(jq -s '.[0] * .[1]' "$SETTINGS" "$SRC")

if $DRY; then
  echo "[dry-run] Would write merged settings to $SETTINGS"
  echo "$merged" | jq . | sed -n '1,120p'
else
  echo "$merged" > "$SETTINGS"
  echo "Updated $SETTINGS with assistant preferences (v1)."
fi

exit 0

