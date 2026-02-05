#!/usr/bin/env python3
"""
Test suite for Guardian Framework configuration integrity.
Verifies model synchronization, agent prompt structure, and workflow consistency.
"""

import json
import sys
from pathlib import Path


def test_model_sync_integrity():
    """Verify all agent prompts have correct model references matching models.json"""
    project_root = Path(".")
    
    # Load current models from models.json
    models_file = project_root / ".opencode" / "models.json"
    if not models_file.exists():
        print(f"❌ models.json not found at {models_file}")
        return False
    
    try:
        models_data = json.loads(models_file.read_text())
        current_models = models_data.get("current_models", {})
    except Exception as e:
        print(f"❌ Failed to parse models.json: {e}")
        return False
    
    if not current_models:
        print("❌ No current_models defined in models.json")
        return False
    
    # Check each agent prompt file
    agent_dir = project_root / ".opencode" / "agent"
    if not agent_dir.exists():
        print(f"❌ Agent directory not found at {agent_dir}")
        return False
    
    issues = []
    
    for agent_name, expected_model in current_models.items():
        prompt_file = agent_dir / f"{agent_name}.md"
        if not prompt_file.exists():
            issues.append(f"Missing prompt file: {prompt_file}")
            continue
            
        content = prompt_file.read_text()
        
        # Extract model from frontmatter
        if "model:" not in content:
            issues.append(f"No model declaration in {prompt_file}")
            continue
        
        # Extract model value
        actual_model = None
        in_frontmatter = False
        for line in content.split('\n'):
            if line.strip() == '---':
                if in_frontmatter:
                    break
                in_frontmatter = True
                continue
                
            if in_frontmatter and line.startswith('model:'):
                actual_model = line.split('model:', 1)[1].strip()
                break
        
        if not actual_model:
            issues.append(f"Could not extract model from {prompt_file}")
            continue
            
        if actual_model != expected_model:
            issues.append(f"Model mismatch in {prompt_file.name}: expected '{expected_model}', found '{actual_model}'")
    
    if issues:
        print("❌ CONFIG SYNC TESTS FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All model sync tests passed")
        return True


def test_opencode_json_sync():
    """Verify opencode.json matches models.json"""
    project_root = Path(".")
    
    models_file = project_root / ".opencode" / "models.json"
    opencode_file = project_root / "opencode.json"
    
    if not models_file.exists():
        print(f"❌ models.json not found at {models_file}")
        return False
    
    if not opencode_file.exists():
        print(f"❌ opencode.json not found at {opencode_file}")
        return False
    
    try:
        models_data = json.loads(models_file.read_text())
        current_models = models_data.get("current_models", {})
        
        opencode_data = json.loads(opencode_file.read_text())
        agent_config = opencode_data.get("agent", {})
    except Exception as e:
        print(f"❌ Failed to parse config files: {e}")
        return False
    
    issues = []
    
    for agent_name, expected_model in current_models.items():
        if agent_name not in agent_config:
            issues.append(f"Agent '{agent_name}' missing from opencode.json")
            continue
            
        actual_model = agent_config[agent_name].get("model")
        if actual_model != expected_model:
            issues.append(f"Model mismatch for {agent_name} in opencode.json: expected '{expected_model}', found '{actual_model}'")
    
    if issues:
        print("❌ OPENCODE.JSON SYNC TESTS FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ opencode.json sync tests passed")
        return True


def test_agent_prompt_structure():
    """Verify agent prompts have required frontmatter structure"""
    agent_dir = Path(".") / ".opencode" / "agent"
    
    if not agent_dir.exists():
        print(f"❌ Agent directory not found at {agent_dir}")
        return False
    
    required_fields = ["description", "mode", "model"]
    issues = []
    
    for prompt_file in agent_dir.glob("*.md"):
        content = prompt_file.read_text()
        
        # Check frontmatter exists
        if not content.startswith("---"):
            issues.append(f"{prompt_file.name} missing frontmatter")
            continue
        
        # Check required fields
        for field in required_fields:
            if f"{field}:" not in content.split("---")[1]:
                issues.append(f"{prompt_file.name} missing '{field}' in frontmatter")
    
    if issues:
        print("❌ AGENT PROMPT STRUCTURE TESTS FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All agent prompt structure tests passed")
        return True


def test_required_files_exist():
    """Verify all required framework files exist"""
    project_root = Path(".")
    
    required_files = [
        ".opencode/models.json",
        ".opencode/agent/plan.md",
        ".opencode/agent/build.md",
        ".opencode/agent/guardian.md",
        ".opencode/agent/ops.md",
        ".opencode/agent/vision.md",
        "opencode.json",
        "opencode-dual-agent.sh",
        "guardian_system/ops.sh",
        "guardian_system/bootstrap.sh",
        ".opencode/tool/ops-sync-config.sh",
        "GUARDIAN_WORKFLOW.md"
    ]
    
    missing = []
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing.append(file_path)
    
    if missing:
        print("❌ REQUIRED FILES TEST FAILED:")
        for file_path in missing:
            print(f"  - Missing: {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True


def main():
    """Run all tests"""
    print("🧪 Running Guardian Framework Configuration Tests")
    print("=" * 60)
    
    tests = [
        ("Required Files", test_required_files_exist),
        ("Model Sync Integrity", test_model_sync_integrity),
        ("opencode.json Sync", test_opencode_json_sync),
        ("Agent Prompt Structure", test_agent_prompt_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Framework is STABLE.")
        return 0
    else:
        print(f"\n💥 {sum(1 for _, r in results if not r)} test(s) failed. Framework is UNSTABLE.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
