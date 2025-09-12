#!/usr/bin/env bash
set -euo pipefail

# Minimal helper to set assistant.outputStyle in ~/.gemini/settings.json or workspace .gemini/settings.json

usage() {
  cat <<'USAGE'
Usage: tools/cdx/scripts/set-output-style.sh <style> [--scope user|workspace]

Styles: default, table, yaml, ultra-concise, tts-summary, html
USAGE
}

if [[ $# -lt 1 ]]; then usage; exit 2; fi

STYLE="$1"; shift || true
SCOPE="user"
if [[ "${1:-}" == "--scope" ]]; then
  SCOPE="${2:-user}"; shift 2 || true
fi

case "$STYLE" in
  default|table|yaml|ultra-concise|tts-summary|html) ;;
  *) echo "Unknown style: $STYLE" >&2; usage; exit 2 ;;
esac

if [[ "$SCOPE" == "workspace" ]]; then
  ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
  SETTINGS="$ROOT/.gemini/settings.json"
else
  SETTINGS="$HOME/.gemini/settings.json"
fi

mkdir -p "$(dirname "$SETTINGS")"
if [[ ! -s "$SETTINGS" ]]; then echo '{}' > "$SETTINGS"; fi

tmp=$(mktemp)
if command -v jq >/dev/null 2>&1; then
  jq --arg style "$STYLE" '.assistant = (.assistant // {}) | .assistant.outputStyle = $style' \
    "$SETTINGS" > "$tmp"
  mv "$tmp" "$SETTINGS"
else
  # naive fallback (no jq): append/replace a line (best effort)
  cp "$SETTINGS" "$tmp"
  echo "\n  \"assistant\": { \"outputStyle\": \"$STYLE\" }" >> "$tmp"
  mv "$tmp" "$SETTINGS"
fi

echo "Set output style to '$STYLE' in $SETTINGS"

