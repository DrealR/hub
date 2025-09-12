#!/usr/bin/env bash
set -euo pipefail

# setup-fast-tools: Append FAST-TOOLS PROMPT v1 to AGENTS.md (idempotent)
# Notes:
# - No package installation is performed, even with --install-deps.
# - For install guidance, see tools/cdx/agents/fast-tools.md.

usage() {
  cat <<'USAGE'
Usage: tools/cdx/scripts/setup-fast-tools.sh [--dry-run] [--non-interactive] [--install-deps]

Actions:
  - Appends tools/cdx/agents/fast-tools.md to AGENTS.md if watermark not present.
  - Never installs system packages. --install-deps only prints guidance.

Flags:
  --dry-run          Print actions without modifying files
  --non-interactive  Suppress any prompts (no prompts are used currently)
  --install-deps     Print best-effort install tips (no sudo commands are run)
USAGE
}

INSTALL_DEPS=false
NON_INTERACTIVE=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --install-deps) INSTALL_DEPS=true ;;
    --non-interactive) NON_INTERACTIVE=true ;;
    --dry-run) DRY_RUN=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; usage; exit 2 ;;
  esac
done

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
agents="$repo_root/AGENTS.md"
prompt_src="$repo_root/tools/cdx/agents/fast-tools.md"

if [[ ! -f "$agents" ]]; then
  echo "AGENTS.md not found under $repo_root" >&2
  exit 1
fi
if [[ ! -f "$prompt_src" ]]; then
  echo "Prompt file missing: $prompt_src" >&2
  exit 1
fi

has_watermark() {
  if command -v rg >/dev/null 2>&1; then
    rg -q "FAST-TOOLS PROMPT v1" "$agents"
  else
    grep -q "FAST-TOOLS PROMPT v1" "$agents"
  fi
}

if has_watermark; then
  echo "FAST-TOOLS prompt already present — nothing to do."
else
  if $DRY_RUN; then
    echo "[dry-run] Would append fast-tools prompt to $agents"
  else
    printf "\n\n" >> "$agents"
    cat "$prompt_src" >> "$agents"
    echo "Appended fast-tools prompt to AGENTS.md"
  fi
fi

if $INSTALL_DEPS; then
  echo "--install-deps requested: printing guidance only (no installs)."
  cat <<'GUIDE'
Recommended manual installs (run yourself):
  macOS (Homebrew):   brew install ripgrep fd jq
  Debian/Ubuntu:      sudo apt-get install ripgrep fd-find jq
                      # then: alias fd=fdfind
  Fedora:             sudo dnf install ripgrep fd-find jq
  Arch:               sudo pacman -S ripgrep fd jq

Non-interactive options:
  - Use --non-interactive with your package manager if available.
  - Or vendor binaries in your CI image and ensure PATH includes them.
GUIDE
fi

exit 0

