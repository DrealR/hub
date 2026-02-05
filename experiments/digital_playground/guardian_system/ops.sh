#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPS_SYNC_SCRIPT="$ROOT_DIR/.opencode/tool/ops-sync-config.sh"
MODELS_JSON="$ROOT_DIR/.opencode/models.json"
CREDS_FILE="$HOME/.config/opencode/credentials.json"
PROJECT_CREDS_FILE="$ROOT_DIR/.opencode-credentials.json"

usage() {
  cat <<'EOF'
Guardian Ops Helper

Usage:
  ops.sh models list                # Show catalogued models by agent
  ops.sh models show                # Display current model assignments
  ops.sh models set <agent> <model> [<agent> <model>...]
  ops.sh credentials status         # Check which credentials are configured
  ops.sh credentials sync           # Write ~/.config/opencode/credentials.json from env vars
  ops.sh status                     # Full framework health check
  ops.sh doctor                     # Diagnose common issues
  ops.sh backup [name]              # Backup configurations (default: timestamp)
  ops.sh restore <name>             # Restore configurations from backup
EOF
}

require_ops_sync() {
  if [[ ! -x "$OPS_SYNC_SCRIPT" ]]; then
    echo "Error: ops-sync-config.sh not found at $OPS_SYNC_SCRIPT" >&2
    exit 1
  fi
}

models_list() {
  if [[ ! -f "$MODELS_JSON" ]]; then
    echo "Error: models.json not found at $MODELS_JSON" >&2
    exit 1
  fi
  MODELS_JSON="$MODELS_JSON" python3 <<'PY'
import json
import os
from pathlib import Path

models_path = Path(os.environ["MODELS_JSON"])
data = json.loads(models_path.read_text())
sections = {
    "plan_models": "Plan",
    "build_models": "Build",
    "guardian_models": "Guardian",
    "ops_models": "Ops",
    "vision_models": "Vision",
}
for key, title in sections.items():
    entries = data.get(key, {})
    if not entries:
        continue
    print(f"{title} models:")
    for model, meta in entries.items():
        desc = meta.get("description", "")
        provider = meta.get("provider", "")
        info = f" - {model}"
        if provider:
            info += f" (provider: {provider})"
        if desc:
            info += f" — {desc}"
        print(info)
    print()
PY
}

models_show() {
  require_ops_sync
  "$OPS_SYNC_SCRIPT" --show
}

models_set() {
  require_ops_sync
  if [[ $# -lt 2 || $(( $# % 2 )) -ne 0 ]]; then
    echo "Error: provide pairs of <agent> <model>." >&2
    exit 1
  fi
  declare -a args
  while [[ $# -gt 0 ]]; do
    agent="$1"; shift
    model="$1"; shift
    case "$agent" in
      plan|build|guardian|ops|vision)
        args+=("--$agent" "$model")
        ;;
      *)
        echo "Error: unknown agent '$agent'. Expected plan, build, guardian, ops, or vision." >&2
        exit 1
        ;;
    esac
  done
  "$OPS_SYNC_SCRIPT" "${args[@]}"
}

credentials_status() {
  report_file() {
    local file="$1"
    local label="$2"
    if [[ -f "$file" ]]; then
      CREDS_STATUS_FILE="$file" CREDS_STATUS_LABEL="$label" python3 - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["CREDS_STATUS_FILE"])
label = os.environ["CREDS_STATUS_LABEL"]
try:
    data = json.loads(path.read_text())
except Exception:
    print(f"{label}: present but unreadable")
else:
    providers = []
    for provider, meta in sorted(data.items()):
        api_key = meta.get("apiKey") or meta.get("api_key")
        status = "set" if api_key else "missing"
        providers.append(f"  - {provider}: {status}")
    print(f"{label}:")
    if providers:
        print("\n".join(providers))
    else:
        print("  (no providers configured)")
PY
    else
      echo "$label: not found"
    fi
  }

  report_file "$CREDS_FILE" "Global credentials (~/.config/opencode/credentials.json)"
  report_file "$PROJECT_CREDS_FILE" "Project credentials (.opencode-credentials.json)"
}

credentials_sync() {
  require_ops_sync
  "$OPS_SYNC_SCRIPT" --write-credentials
}

framework_status() {
  echo "🔍 Guardian Framework Status Check"
  echo "=================================="
  echo ""
  
  # Check required files
  echo "📁 Required Files:"
  required_files=(
    "$MODELS_JSON"
    "$ROOT_DIR/opencode.json"
    "$ROOT_DIR/.opencode/agent/plan.md"
    "$ROOT_DIR/.opencode/agent/build.md"
    "$ROOT_DIR/.opencode/agent/guardian.md"
    "$ROOT_DIR/.opencode/agent/ops.md"
    "$ROOT_DIR/.opencode/agent/vision.md"
  )
  
  all_files_present=true
  for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
      echo "  ✅ $(basename "$file")"
    else
      echo "  ❌ $(basename "$file") - MISSING"
      all_files_present=false
    fi
  done
  echo ""
  
  # Check model synchronization
  echo "🔄 Model Synchronization:"
  if [[ -f "$ROOT_DIR/.opencode/tests/test_framework.py" ]]; then
    if python3 "$ROOT_DIR/.opencode/tests/test_framework.py" > /dev/null 2>&1; then
      echo "  ✅ All models synchronized"
    else
      echo "  ❌ Model synchronization issues detected"
      python3 "$ROOT_DIR/.opencode/tests/test_framework.py" | grep "❌" | sed 's/^/     /'
    fi
  else
    echo "  ⚠️  Test framework not found"
  fi
  echo ""
  
  # Check anomaly ledger
  echo "🛡️  Anomaly Ledger:"
  ledger_file="$ROOT_DIR/.opencode/anomaly-ledger.json"
  if [[ -f "$ledger_file" ]]; then
    if python3 "$ROOT_DIR/.opencode/tool/guardian-automation.py" report > /dev/null 2>&1; then
      system_state=$(python3 -c "import json; print(json.load(open('$ledger_file')).get('system_state', 'UNKNOWN'))")
      active_count=$(python3 -c "import json; data=json.load(open('$ledger_file')); print(sum(1 for a in data.get('anomalies', []) if a.get('status') != 'resolved'))")
      
      if [[ "$system_state" == "STABLE" ]]; then
        echo "  ✅ System is STABLE ($active_count active anomalies)"
      else
        echo "  ⚠️  System is $system_state ($active_count active anomalies)"
      fi
    else
      echo "  ❌ Unable to read anomaly ledger"
    fi
  else
    echo "  ❌ Anomaly ledger not found"
  fi
  echo ""
  
  # Check credentials
  echo "🔑 Credentials:"
  credentials_status | grep -E "(openrouter|anthropic|opencode|moonshotai)" | sed 's/^/  /'
  echo ""
  
  # Check automation tools
  echo "🤖 Automation Tools:"
  if [[ -f "$ROOT_DIR/.opencode/tool/vision-workflow.py" ]]; then
    echo "  ✅ Vision workflow integration"
  else
    echo "  ❌ Vision workflow not found"
  fi
  
  if [[ -f "$ROOT_DIR/.opencode/tool/guardian-automation.py" ]]; then
    echo "  ✅ Guardian automation system"
  else
    echo "  ❌ Guardian automation not found"
  fi
  
  if [[ -f "$ROOT_DIR/guardian_system/scaffold.py" ]]; then
    echo "  ✅ Project scaffolding"
  else
    echo "  ❌ Scaffolding not found"
  fi
  echo ""
  
  # Overall status
  if [[ "$all_files_present" == true ]]; then
    echo "🎉 Framework is properly configured and ready"
  else
    echo "💥 Framework has configuration issues that need attention"
  fi
}

doctor() {
  echo "🚑 Guardian Framework Doctor"
  echo "============================"
  echo ""
  
  issues_found=0
  
  # Check 1: Python version
  echo "🔍 Check 1: Python Version"
  python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
  echo "  Python version: $python_version"
  if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "  ✅ Python 3.8+ is available"
  else
    echo "  ❌ Python 3.8+ is required"
    issues_found=$((issues_found + 1))
  fi
  echo ""
  
  # Check 2: Required tools
  echo "🔍 Check 2: Required Tools"
  required_tools=("python3" "bash" "grep" "sed" "awk")
  for tool in "${required_tools[@]}"; do
    if command -v "$tool" > /dev/null 2>&1; then
      echo "  ✅ $tool is available"
    else
      echo "  ❌ $tool is missing"
      issues_found=$((issues_found + 1))
    fi
  done
  echo ""
  
  # Check 3: File permissions
  echo "🔍 Check 3: File Permissions"
  executable_files=(
    "$ROOT_DIR/opencode-dual-agent.sh"
    "$ROOT_DIR/guardian_system/ops.sh"
    "$ROOT_DIR/guardian_system/bootstrap.sh"
    "$OPS_SYNC_SCRIPT"
  )
  
  for file in "${executable_files[@]}"; do
    if [[ -f "$file" ]]; then
      if [[ -x "$file" ]]; then
        echo "  ✅ $(basename "$file") is executable"
      else
        echo "  ⚠️  $(basename "$file") is not executable (fix: chmod +x $file)"
        issues_found=$((issues_found + 1))
      fi
    fi
  done
  echo ""
  
  # Check 4: JSON validity
  echo "🔍 Check 4: JSON Configuration Files"
  json_files=("$MODELS_JSON" "$ROOT_DIR/opencode.json")
  for file in "${json_files[@]}"; do
    if [[ -f "$file" ]]; then
      if python3 -m json.tool "$file" > /dev/null 2>&1; then
        echo "  ✅ $(basename "$file") is valid JSON"
      else
        echo "  ❌ $(basename "$file") has JSON syntax errors"
        issues_found=$((issues_found + 1))
      fi
    fi
  done
  echo ""
  
  # Check 5: Model consistency
  echo "🔍 Check 5: Model Configuration Consistency"
  if [[ -f "$ROOT_DIR/.opencode/tests/test_framework.py" ]]; then
    if python3 "$ROOT_DIR/.opencode/tests/test_framework.py" > /dev/null 2>&1; then
      echo "  ✅ Model configurations are consistent"
    else
      echo "  ❌ Model configuration inconsistencies detected"
      python3 "$ROOT_DIR/.opencode/tests/test_framework.py" | grep "❌" | sed 's/^/     /'
      issues_found=$((issues_found + 1))
    fi
  else
    echo "  ⚠️  Cannot check model consistency (test framework missing)"
  fi
  echo ""
  
  # Summary
  if [[ $issues_found -eq 0 ]]; then
    echo "🎉 No issues found. Framework is healthy!"
  else
    echo "💥 Found $issues_found issue(s) that need attention"
    echo ""
    echo "💡 Common fixes:"
    echo "   • Make scripts executable: chmod +x *.sh"
    echo "   • Fix JSON syntax: python3 -m json.tool file.json"
    echo "   • Sync models: ./guardian_system/ops.sh models show"
  fi
}

backup_config() {
  local backup_name="${1:-backup-$(date +%Y%m%d-%H%M%S)}"
  local backup_dir="$ROOT_DIR/.opencode/backups/$backup_name"
  
  echo "💾 Creating backup: $backup_name"
  
  mkdir -p "$backup_dir"
  
  # Backup configuration files
  cp "$MODELS_JSON" "$backup_dir/" 2>/dev/null || echo "  ⚠️  models.json not found"
  cp "$ROOT_DIR/opencode.json" "$backup_dir/" 2>/dev/null || echo "  ⚠️  opencode.json not found"
  cp "$ROOT_DIR/.opencode-credentials.json" "$backup_dir/" 2>/dev/null || echo "  ⚠️  .opencode-credentials.json not found"
  
  # Backup agent prompts
  if [[ -d "$ROOT_DIR/.opencode/agent" ]]; then
    cp -r "$ROOT_DIR/.opencode/agent" "$backup_dir/" || echo "  ⚠️  Could not backup agent prompts"
  fi
  
  # Create backup metadata
  cat > "$backup_dir/backup-info.json" <<EOF
{
  "name": "$backup_name",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "created_by": "$(whoami)",
  "hostname": "$(hostname)",
  "framework_version": "1.0.0"
}
EOF
  
  echo "✅ Backup created: $backup_dir"
  echo ""
  echo "To restore: ./guardian_system/ops.sh restore $backup_name"
}

restore_config() {
  local backup_name="$1"
  
  if [[ -z "$backup_name" ]]; then
    echo "❌ Backup name required"
    echo "Available backups:"
    ls -1 "$ROOT_DIR/.opencode/backups/" 2>/dev/null || echo "  (no backups found)"
    exit 1
  fi
  
  local backup_dir="$ROOT_DIR/.opencode/backups/$backup_name"
  
  if [[ ! -d "$backup_dir" ]]; then
    echo "❌ Backup not found: $backup_name"
    echo "Available backups:"
    ls -1 "$ROOT_DIR/.opencode/backups/" 2>/dev/null || echo "  (no backups found)"
    exit 1
  fi
  
  echo "🔄 Restoring from backup: $backup_name"
  
  # Restore configuration files
  if [[ -f "$backup_dir/models.json" ]]; then
    cp "$backup_dir/models.json" "$MODELS_JSON"
    echo "  ✅ Restored models.json"
  fi
  
  if [[ -f "$backup_dir/opencode.json" ]]; then
    cp "$backup_dir/opencode.json" "$ROOT_DIR/"
    echo "  ✅ Restored opencode.json"
  fi
  
  if [[ -f "$backup_dir/.opencode-credentials.json" ]]; then
    cp "$backup_dir/.opencode-credentials.json" "$ROOT_DIR/"
    echo "  ✅ Restored .opencode-credentials.json"
  fi
  
  # Restore agent prompts
  if [[ -d "$backup_dir/agent" ]]; then
    rm -rf "$ROOT_DIR/.opencode/agent"
    cp -r "$backup_dir/agent" "$ROOT_DIR/.opencode/"
    echo "  ✅ Restored agent prompts"
  fi
  
  echo ""
  echo "✅ Restore complete"
  echo "📝 Run './guardian_system/ops.sh status' to verify"
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

case "$1" in
  models)
    shift
    subcmd="${1:-}"
    case "$subcmd" in
      list)
        shift
        models_list "$@"
        ;;
      show)
        shift
        models_show "$@"
        ;;
      set)
        shift
        models_set "$@"
        ;;
      *)
        usage
        exit 1
        ;;
    esac
    ;;
  credentials)
    shift
    case "${1:-}" in
      status)
        shift
        credentials_status
        ;;
      sync)
        shift
        credentials_sync
        ;;
      *)
        usage
        exit 1
        ;;
    esac
    ;;
  status)
    framework_status
    ;;
  doctor)
    doctor
    ;;
  backup)
    shift
    backup_config "$@"
    ;;
  restore)
    shift
    restore_config "$@"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage
    exit 1
    ;;
esac
