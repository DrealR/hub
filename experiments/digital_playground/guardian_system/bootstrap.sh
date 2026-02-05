#!/bin/bash
# Copy Guardian Framework assets into a target repository.
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"
FORCE=0

usage() {
  cat <<'EOF'
Usage: guardian_system/bootstrap.sh <target-path> [--force]

Copies the Guardian agent configuration into <target-path>. Existing files are preserved unless --force is provided.
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown option: $1" >&2; usage; exit 1;;
  esac
done

if [[ ! -d "$TARGET" ]]; then
  echo "Error: target path '$TARGET' does not exist." >&2
  exit 1
fi

copy_file() {
  local src="$1"
  local dest="$2"
  if [[ -e "$dest" && $FORCE -ne 1 ]]; then
    echo "Skipping existing $dest (use --force to overwrite)"
  else
    mkdir -p "$(dirname "$dest")"
    cp -R "$src" "$dest"
    echo "Copied $(basename "$src")"
  fi
}

copy_file "$SOURCE_ROOT/.opencode" "$TARGET/.opencode"
copy_file "$SOURCE_ROOT/opencode.json" "$TARGET/opencode.json"
copy_file "$SOURCE_ROOT/.opencode-workflow.json" "$TARGET/.opencode-workflow.json"
copy_file "$SOURCE_ROOT/opencode-dual-agent.sh" "$TARGET/opencode-dual-agent.sh"
copy_file "$SOURCE_ROOT/GUARDIAN_WORKFLOW.md" "$TARGET/GUARDIAN_WORKFLOW.md"
copy_file "$SOURCE_ROOT/guardian_system/ops.sh" "$TARGET/guardian_system/ops.sh"

if [[ ! -f "$TARGET/.gitignore" ]]; then
  touch "$TARGET/.gitignore"
fi
if ! grep -q "^\.opencode-credentials\.json$" "$TARGET/.gitignore"; then
  echo ".opencode-credentials.json" >> "$TARGET/.gitignore"
fi

echo "Bootstrap complete. Run ./opencode-dual-agent.sh inside $TARGET to initialize the framework."
