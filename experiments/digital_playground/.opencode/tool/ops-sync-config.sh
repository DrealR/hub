#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MODELS_FILE="$CONFIG_ROOT/models.json"
CREDS_FILE="${HOME}/.config/opencode/credentials.json"

PLAN_OVERRIDE=""
BUILD_OVERRIDE=""
GUARDIAN_OVERRIDE=""
OPS_OVERRIDE=""
VISION_OVERRIDE=""
WRITE_CREDS=0
SHOW_ONLY=0

usage() {
  cat <<'EOF'
Usage: ops-sync-config.sh [options]

Options:
  --plan MODEL        Set the plan agent model
  --build MODEL       Set the build agent model
  --guardian MODEL    Set the guardian agent model
  --ops MODEL         Set the ops agent model
  --vision MODEL      Set the vision agent model
  --write-credentials Update ~/.config/opencode/credentials.json using exported env vars
  --show              Print current model selections (does not modify files)
  -h, --help          Show this help message

Environment variables consumed when --write-credentials is supplied:
  OPENROUTER_API_KEY, ANTHROPIC_API_KEY, OPENCODE_API_KEY, MOONSHOTAI_API_KEY
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --plan) PLAN_OVERRIDE="$2"; shift 2;;
    --build) BUILD_OVERRIDE="$2"; shift 2;;
    --guardian) GUARDIAN_OVERRIDE="$2"; shift 2;;
    --ops) OPS_OVERRIDE="$2"; shift 2;;
    --vision) VISION_OVERRIDE="$2"; shift 2;;
    --write-credentials) WRITE_CREDS=1; shift;;
    --show) SHOW_ONLY=1; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown option: $1" >&2; usage; exit 1;;
  esac
done

if [[ ! -f "$MODELS_FILE" ]]; then
  echo "Error: models.json not found at $MODELS_FILE" >&2
  exit 1
fi

python3 "-" "$MODELS_FILE" "$PROJECT_ROOT" "$PLAN_OVERRIDE" "$BUILD_OVERRIDE" "$GUARDIAN_OVERRIDE" "$OPS_OVERRIDE" "$VISION_OVERRIDE" "$SHOW_ONLY" <<'PY'
import json
import re
import sys
from pathlib import Path

try:
    models_path = Path(sys.argv[1])
    project_root = Path(sys.argv[2])
    plan_override = sys.argv[3]
    build_override = sys.argv[4]
    guardian_override = sys.argv[5]
    ops_override = sys.argv[6]
    vision_override = sys.argv[7]
    show_only = sys.argv[8] == "1"
except IndexError:
    print("Invalid invocation: missing required arguments", file=sys.stderr)
    sys.exit(1)

if not models_path.exists():
    print(f"Error: models.json not found at {models_path}", file=sys.stderr)
    sys.exit(1)

agent_dir = project_root / ".opencode" / "agent"
opencode_path = project_root / "opencode.json"

data = json.loads(models_path.read_text())
current = data.setdefault("current_models", {})

override_map = {
    "plan": plan_override or "",
    "build": build_override or "",
    "guardian": guardian_override or "",
    "ops": ops_override or "",
    "vision": vision_override or "",
}

changes = {k: v for k, v in override_map.items() if v}

preview_current = dict(current)
preview_current.update(changes)

if show_only:
    print(json.dumps(preview_current, indent=2))
    sys.exit(0)

if changes:
    current.update(changes)
    models_path.write_text(json.dumps(data, indent=2) + "\n")
    summary = ", ".join(f"{k}→{v}" for k, v in changes.items())
    print(f"Updated models: {summary}")
else:
    models_path.write_text(json.dumps(data, indent=2) + "\n")
    print("No model overrides supplied. Current selections:")
    print(json.dumps(current, indent=2))

if opencode_path.exists():
    try:
        config = json.loads(opencode_path.read_text())
    except json.JSONDecodeError as err:
        print(f"Warning: could not parse {opencode_path}: {err}", file=sys.stderr)
    else:
        agents = config.get("agent", {})
        changed = False
        for key, model in current.items():
            section = agents.get(key)
            if isinstance(section, dict) and section.get("model") != model:
                section["model"] = model
                changed = True
        if changed:
            opencode_path.write_text(json.dumps(config, indent=2) + "\n")

agent_models = {
    "plan": current.get("plan"),
    "build": current.get("build"),
    "guardian": current.get("guardian"),
    "ops": current.get("ops"),
    "vision": current.get("vision"),
}

def apply_model(text, model_value):
    if not model_value:
        return text
    if "model:" in text:
        return re.sub(r"model:\s*.*", f"model: {model_value}", text, count=1)
    return re.sub(r"(mode:\s*[^\n]+)\n", r"\1\nmodel: " + model_value + "\n", text, count=1)

for agent, filename in (
    ("plan", "plan.md"),
    ("build", "build.md"),
    ("guardian", "guardian.md"),
    ("ops", "ops.md"),
    ("vision", "vision.md"),
):
    path = agent_dir / filename
    model_value = agent_models.get(agent)
    if not path.exists() or not model_value:
        continue
    original = path.read_text()
    updated = apply_model(original, model_value)
    if updated != original:
        path.write_text(updated)

print("Configuration sync complete")
PY

if [[ $SHOW_ONLY -eq 1 ]]; then
  exit 0
fi

if [[ $WRITE_CREDS -eq 1 ]]; then
env PLAN_OVERRIDE="$PLAN_OVERRIDE" \
    BUILD_OVERRIDE="$BUILD_OVERRIDE" \
    GUARDIAN_OVERRIDE="$GUARDIAN_OVERRIDE" \
    OPS_OVERRIDE="$OPS_OVERRIDE" \
    VISION_OVERRIDE="$VISION_OVERRIDE" \
    SHOW_ONLY="$SHOW_ONLY" \
    PROJECT_ROOT="$PROJECT_ROOT" \
    MODELS_FILE="$MODELS_FILE" \
    python3 <<'PY'
import json

import os
from pathlib import Path

creds_path = Path("$CREDS_FILE")
creds_path.parent.mkdir(parents=True, exist_ok=True)
existing = {}
if creds_path.exists():
    try:
        existing = json.loads(creds_path.read_text())
    except Exception:
        existing = {}

updated = dict(existing)

for provider, env_var in (
    ("openrouter", "OPENROUTER_API_KEY"),
    ("anthropic", "ANTHROPIC_API_KEY"),
    ("opencode", "OPENCODE_API_KEY"),
    ("moonshotai", "MOONSHOTAI_API_KEY"),
):
    value = os.environ.get(env_var)
    if value:
        updated.setdefault(provider, {})['apiKey'] = value

if updated != existing:
    creds_path.write_text(json.dumps(updated, indent=2) + "\n")
    providers = ", ".join(updated.keys())
    print(f"Credentials synced for: {providers}")
else:
    print("No credential environment variables supplied. Nothing written.")
PY
fi

echo "ops-sync-config.sh complete"
