#!/bin/bash

# OpenCode Dual-Agent Workflow Wrapper
# This script helps manage the thinker ↔ coder agent workflow

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCODE_CMD="opencode"
MODELS_CONFIG="$PROJECT_DIR/.opencode/models.json"
CREDS_CONFIG="$PROJECT_DIR/.opencode-credentials.json"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Source environment variables from .zshrc
if [ -f "$HOME/.zshrc" ]; then
  source "$HOME/.zshrc"
fi

# Load current models
PLAN_MODEL="openrouter/moonshotai/kimi-k2-thinking"
BUILD_MODEL="openrouter/polaris-alpha"
GUARDIAN_MODEL="anthropic/claude-3-5-sonnet"
OPS_MODEL="openrouter/gpt-4o-mini"
VISION_MODEL="openrouter/gpt-5-codex"

if [ -f "$MODELS_CONFIG" ]; then
  read PLAN_MODEL BUILD_MODEL GUARDIAN_MODEL OPS_MODEL VISION_MODEL <<EOF
$(MODELS_CONFIG="$MODELS_CONFIG" python3 <<'PY'
import json
import os
import sys
from pathlib import Path

models_path = Path(os.environ["MODELS_CONFIG"])
try:
    data = json.loads(models_path.read_text())
except Exception:
    print("openrouter/moonshotai/kimi-k2-thinking openrouter/polaris-alpha anthropic/claude-3-5-sonnet openrouter/gpt-4o-mini openrouter/gpt-5-codex")
    sys.exit(0)

current = data.get("current_models", {})
plan = current.get("plan") or "openrouter/moonshotai/kimi-k2-thinking"
build = current.get("build") or "openrouter/polaris-alpha"
guardian = current.get("guardian") or current.get("adversary") or "anthropic/claude-3-5-sonnet"
ops = current.get("ops") or "openrouter/gpt-4o-mini"
vision = current.get("vision") or "openrouter/gpt-5-codex"
print(f"{plan} {build} {guardian} {ops} {vision}")
PY
)
EOF
fi

# Update config files with selected models
PROJECT_DIR="$PROJECT_DIR" PLAN_MODEL="$PLAN_MODEL" BUILD_MODEL="$BUILD_MODEL" GUARDIAN_MODEL="$GUARDIAN_MODEL" OPS_MODEL="$OPS_MODEL" VISION_MODEL="$VISION_MODEL" python3 <<'PY'
import json
import os
import re
from pathlib import Path

project_dir = Path(os.environ["PROJECT_DIR"])
plan_model = os.environ["PLAN_MODEL"]
build_model = os.environ["BUILD_MODEL"]
guardian_model = os.environ["GUARDIAN_MODEL"]
ops_model = os.environ["OPS_MODEL"]
vision_model = os.environ["VISION_MODEL"]

# Update opencode.json
config_path = project_dir / "opencode.json"
if config_path.exists():
    data = json.loads(config_path.read_text())
    data.pop("model", None)
    if "agent" in data:
        if "plan" in data["agent"]:
            data["agent"]["plan"]["model"] = plan_model
        if "build" in data["agent"]:
            data["agent"]["build"]["model"] = build_model
        if "guardian" in data["agent"]:
            data["agent"]["guardian"]["model"] = guardian_model
        if "ops" in data["agent"]:
            data["agent"]["ops"]["model"] = ops_model
    config_path.write_text(json.dumps(data, indent=2) + "\n")

# Update agent markdown files
agent_dir = project_dir / ".opencode" / "agent"
plan_path = agent_dir / "plan.md"
build_path = agent_dir / "build.md"
guardian_path = agent_dir / "guardian.md"
ops_path = agent_dir / "ops.md"
vision_path = agent_dir / "vision.md"

if plan_path.exists():
    text = plan_path.read_text()
    if "model:" in text:
        text = re.sub(r"model:.*", f"model: {plan_model}", text, count=1)
    else:
        text = text.replace("mode: primary", f"mode: primary\nmodel: {plan_model}", 1)
    plan_path.write_text(text)

if build_path.exists():
    text = build_path.read_text()
    if "model:" in text:
        text = re.sub(r"model:.*", f"model: {build_model}", text, count=1)
    else:
        text = text.replace("mode: primary", f"mode: primary\nmodel: {build_model}", 1)
    build_path.write_text(text)

if guardian_path.exists():
    text = guardian_path.read_text()
    if "model:" in text:
        text = re.sub(r"model:.*", f"model: {guardian_model}", text, count=1)
    else:
        text = text.replace("mode: primary", f"mode: primary\nmodel: {guardian_model}", 1)
    guardian_path.write_text(text)

if ops_path.exists():
    text = ops_path.read_text()
    if "model:" in text:
        text = re.sub(r"model:.*", f"model: {ops_model}", text, count=1)
    else:
        text = text.replace("mode: primary", f"mode: primary\nmodel: {ops_model}", 1)
    ops_path.write_text(text)

if vision_path.exists():
    text = vision_path.read_text()
    if "model:" in text:
        text = re.sub(r"model:.*", f"model: {vision_model}", text, count=1)
    else:
        text = text.replace("mode: subagent", f"mode: subagent\nmodel: {vision_model}", 1)
    vision_path.write_text(text)
PY

echo -e "${GREEN}OpenCode Dual-Agent Workflow${NC}"
echo "=============================="
echo ""
echo -e "${BLUE}Plan Agent${NC}: $PLAN_MODEL"
echo -e "${BLUE}Build Agent${NC}: $BUILD_MODEL"
echo -e "${BLUE}Guardian Agent${NC}: $GUARDIAN_MODEL"
echo -e "${BLUE}Ops Agent${NC}: $OPS_MODEL"
echo -e "${BLUE}Vision Subagent${NC}: $VISION_MODEL"
echo ""
echo -e "${YELLOW}Model helper:${NC} ./guardian_system/ops.sh models show"
echo ""
echo -e "${YELLOW}Workflow:${NC}"
echo "1. Start with the Plan agent for analysis"
echo "2. Plan agent produces a TDD-first implementation roadmap"
echo "3. Press TAB to switch to the Build agent"
echo "4. Build agent implements, tests, and reports back"
echo "5. Press TAB to return to Plan for review or next steps"
echo ""
echo -e "${YELLOW}Tips:${NC}"
echo "- Start with: /init to initialize the project"
echo "- Use @mention to reference files: @filename"
echo "- Press TAB to cycle Plan → Build → Guardian → Ops"
echo "- Use /undo to revert changes"
echo "- Use /share to share sessions"
echo ""
echo -e "${GREEN}Starting OpenCode...${NC}"
echo ""

# Change to project directory
cd "$PROJECT_DIR"

# Extract credentials from file if present, otherwise fall back to environment
OPENROUTER_KEY=""
OPENCODE_KEY=""
ANTHROPIC_KEY=""
MOONSHOTAI_KEY=""
GROQ_KEY=""

if [ -f "$CREDS_CONFIG" ]; then
  OPENROUTER_KEY=$(python3 -c "import json; print(json.load(open('$CREDS_CONFIG')).get('openrouter', {}).get('apiKey', ''))" 2>/dev/null || echo "")
  OPENCODE_KEY=$(python3 -c "import json; print(json.load(open('$CREDS_CONFIG')).get('opencode', {}).get('apiKey', ''))" 2>/dev/null || echo "")
  ANTHROPIC_KEY=$(python3 -c "import json; print(json.load(open('$CREDS_CONFIG')).get('anthropic', {}).get('apiKey', ''))" 2>/dev/null || echo "")
  MOONSHOTAI_KEY=$(python3 -c "import json; print(json.load(open('$CREDS_CONFIG')).get('moonshotai', {}).get('apiKey', ''))" 2>/dev/null || echo "")
  GROQ_KEY=$(python3 -c "import json; print(json.load(open('$CREDS_CONFIG')).get('groq', {}).get('apiKey', ''))" 2>/dev/null || echo "")
else
  echo -e "${YELLOW}⚠️  No .opencode-credentials.json found. Falling back to environment variables.${NC}"
fi

# Treat placeholder strings as empty so environment variables can override
case "$OPENROUTER_KEY" in
  ""|"YOUR_OPENROUTER_KEY"|"<OPENROUTER_API_KEY>") OPENROUTER_KEY="";;
esac
case "$OPENCODE_KEY" in
  ""|"YOUR_OPENCODE_KEY"|"<OPENCODE_API_KEY>") OPENCODE_KEY="";;
esac
case "$ANTHROPIC_KEY" in
  ""|"YOUR_ANTHROPIC_KEY"|"<ANTHROPIC_API_KEY>") ANTHROPIC_KEY="";;
esac
case "$MOONSHOTAI_KEY" in
  ""|"YOUR_MOONSHOTAI_KEY"|"<MOONSHOTAI_API_KEY>") MOONSHOTAI_KEY="";;
esac
case "$GROQ_KEY" in
  ""|"YOUR_GROQ_KEY"|"<GROQ_API_KEY>") GROQ_KEY="";;
esac

GLOBAL_CREDS_FILE="$HOME/.config/opencode/credentials.json"
if [ -z "$OPENROUTER_KEY" ] && [ -f "$GLOBAL_CREDS_FILE" ]; then
  OPENROUTER_KEY=$(python3 -c "import json; print(json.load(open('$GLOBAL_CREDS_FILE')).get('openrouter', {}).get('apiKey', ''))" 2>/dev/null || echo "")
fi
if [ -z "$OPENCODE_KEY" ] && [ -f "$GLOBAL_CREDS_FILE" ]; then
  OPENCODE_KEY=$(python3 -c "import json; print(json.load(open('$GLOBAL_CREDS_FILE')).get('opencode', {}).get('apiKey', ''))" 2>/dev/null || echo "")
fi
if [ -z "$ANTHROPIC_KEY" ] && [ -f "$GLOBAL_CREDS_FILE" ]; then
  ANTHROPIC_KEY=$(python3 -c "import json; print(json.load(open('$GLOBAL_CREDS_FILE')).get('anthropic', {}).get('apiKey', ''))" 2>/dev/null || echo "")
fi
if [ -z "$MOONSHOTAI_KEY" ] && [ -f "$GLOBAL_CREDS_FILE" ]; then
  MOONSHOTAI_KEY=$(python3 -c "import json; print(json.load(open('$GLOBAL_CREDS_FILE')).get('moonshotai', {}).get('apiKey', ''))" 2>/dev/null || echo "")
fi
if [ -z "$GROQ_KEY" ] && [ -f "$GLOBAL_CREDS_FILE" ]; then
  GROQ_KEY=$(python3 -c "import json; print(json.load(open('$GLOBAL_CREDS_FILE')).get('groq', {}).get('apiKey', ''))" 2>/dev/null || echo "")
fi

OPENROUTER_KEY="${OPENROUTER_KEY:-${OPENROUTER_API_KEY:-}}"
OPENCODE_KEY="${OPENCODE_KEY:-${OPENCODE_API_KEY:-}}"
ANTHROPIC_KEY="${ANTHROPIC_KEY:-${ANTHROPIC_API_KEY:-}}"
MOONSHOTAI_KEY="${MOONSHOTAI_KEY:-${MOONSHOTAI_API_KEY:-}}"
GROQ_KEY="${GROQ_KEY:-${GROQ_API_KEY:-}}"

if [ -z "$OPENROUTER_KEY" ]; then
  echo -e "${RED}❌ Missing OPENROUTER_API_KEY. Run ./setup-api-keys.sh or ./setup-credentials.sh to populate it.${NC}"
fi
if [ -z "$ANTHROPIC_KEY" ]; then
  echo -e "${YELLOW}⚠️  Missing ANTHROPIC_API_KEY. Guardian/Vision agents may fail.${NC}"
fi
if [ -z "$OPENCODE_KEY" ]; then
  echo -e "${YELLOW}⚠️  Missing OPENCODE_API_KEY. Zen provider features may not work.${NC}"
fi
if [ -z "$MOONSHOTAI_KEY" ]; then
  echo -e "${YELLOW}⚠️  Missing MOONSHOTAI_API_KEY. Plan/Guardian fallback models may require it.${NC}"
fi
if [ -z "$GROQ_KEY" ]; then
  echo -e "${YELLOW}⚠️  Missing GROQ_API_KEY. Groq-based build agents will be unavailable.${NC}"
fi

export OPENROUTER_API_KEY="$OPENROUTER_KEY"
export OPENCODE_API_KEY="$OPENCODE_KEY"
export ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
export MOONSHOTAI_API_KEY="$MOONSHOTAI_KEY"
export GROQ_API_KEY="$GROQ_KEY"

# Start OpenCode with credentials
exec env OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
         OPENCODE_API_KEY="$OPENCODE_API_KEY" \
         ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
         MOONSHOTAI_API_KEY="$MOONSHOTAI_API_KEY" \
         GROQ_API_KEY="$GROQ_API_KEY" \
         $OPENCODE_CMD --agent plan
