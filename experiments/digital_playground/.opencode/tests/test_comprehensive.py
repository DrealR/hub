#!/usr/bin/env python3
"""
Comprehensive test suite for Guardian Framework.
Tests configuration, anomaly tracking, scaffolding, and workflow integration.
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path


class GuardianFrameworkTests:
    """Test suite for Guardian Framework."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results = []
        self.test_count = 0
        self.pass_count = 0
    
    def run_test(self, name: str, test_func):
        """Run a test and record results."""
        self.test_count += 1
        print(f"\n📋 {name}...")
        
        try:
            result = test_func()
            if result:
                self.pass_count += 1
                print(f"  ✅ PASS")
                self.results.append((name, True, None))
            else:
                print(f"  ❌ FAIL")
                self.results.append((name, False, "Test returned False"))
        except Exception as e:
            print(f"  ❌ FAIL: {e}")
            self.results.append((name, False, str(e)))
    
    def test_required_files(self):
        """Verify all required framework files exist."""
        required_files = [
            ".opencode/models.json",
            ".opencode/agent/plan.md",
            ".opencode/agent/build.md",
            ".opencode/agent/guardian.md",
            ".opencode/agent/ops.md",
            ".opencode/agent/vision.md",
            ".opencode/tests/test_framework.py",
            ".opencode/anomaly-ledger.json",
            ".opencode/anomaly-ledger-schema.json",
            "opencode.json",
            "opencode-dual-agent.sh",
            "guardian_system/ops.sh",
            "guardian_system/bootstrap.sh",
            "guardian_system/scaffold.py",
            ".opencode/tool/ops-sync-config.sh",
            "GUARDIAN_WORKFLOW.md"
        ]
        
        missing = []
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing.append(file_path)
        
        if missing:
            print(f"  Missing files: {', '.join(missing)}")
            return False
        
        return True
    
    def test_model_configuration(self):
        """Verify model configuration is consistent across all files."""
        # Load models.json
        models_file = self.project_root / ".opencode" / "models.json"
        models_data = json.loads(models_file.read_text())
        current_models = models_data.get("current_models", {})
        
        if not current_models:
            print("  No current_models in models.json")
            return False
        
        # Check each agent
        agent_dir = self.project_root / ".opencode" / "agent"
        issues = []
        
        for agent_name, expected_model in current_models.items():
            # Check agent prompt
            prompt_file = agent_dir / f"{agent_name}.md"
            if not prompt_file.exists():
                issues.append(f"Missing prompt for {agent_name}")
                continue
            
            content = prompt_file.read_text()
            
            # Extract model from frontmatter
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
            
            if actual_model != expected_model:
                issues.append(f"{agent_name}: expected '{expected_model}', got '{actual_model}'")
            
            # Check opencode.json
            opencode_file = self.project_root / "opencode.json"
            if opencode_file.exists():
                opencode_data = json.loads(opencode_file.read_text())
                agent_config = opencode_data.get("agent", {}).get(agent_name, {})
                config_model = agent_config.get("model")
                
                if config_model != expected_model:
                    issues.append(f"{agent_name} in opencode.json: expected '{expected_model}', got '{config_model}'")
        
        if issues:
            for issue in issues:
                print(f"  {issue}")
            return False
        
        return True
    
    def test_anomaly_ledger_schema(self):
        """Verify anomaly ledger matches schema."""
        ledger_file = self.project_root / ".opencode" / "anomaly-ledger.json"
        schema_file = self.project_root / ".opencode" / "anomaly-ledger-schema.json"
        
        if not ledger_file.exists() or not schema_file.exists():
            print("  Missing anomaly ledger files")
            return False
        
        try:
            ledger = json.loads(ledger_file.read_text())
            schema = json.loads(schema_file.read_text())
            
            # Basic validation
            required_fields = ["system_state", "last_updated", "anomalies"]
            for field in required_fields:
                if field not in ledger:
                    print(f"  Missing required field: {field}")
                    return False
            
            # Check system_state is valid
            if ledger["system_state"] not in ["STABLE", "UNSTABLE"]:
                print(f"  Invalid system_state: {ledger['system_state']}")
                return False
            
            # Check anomalies is array
            if not isinstance(ledger["anomalies"], list):
                print("  anomalies must be an array")
                return False
            
            # Validate each anomaly has required fields
            for anomaly in ledger["anomalies"]:
                required_anomaly_fields = ["id", "title", "status", "detected_at"]
                for field in required_anomaly_fields:
                    if field not in anomaly:
                        print(f"  Anomaly missing required field: {field}")
                        return False
            
            # Check metrics if present
            if "metrics" in ledger:
                metrics = ledger["metrics"]
                required_metrics = ["total_anomalies", "active_anomalies", "resolved_anomalies"]
                for field in required_metrics:
                    if field not in metrics:
                        print(f"  Metrics missing required field: {field}")
                        return False
                    if not isinstance(metrics[field], int):
                        print(f"  Metrics field must be integer: {field}")
                        return False
            
            return True
        except Exception as e:
            print(f"  Error validating anomaly ledger: {e}")
            return False
    
    def test_scaffolding_functionality(self):
        """Test project scaffolding functionality."""
        scaffold_script = self.project_root / "guardian_system" / "scaffold.py"
        
        if not scaffold_script.exists():
            print("  Scaffold script not found")
            return False
        
        # Test listing templates
        import subprocess
        try:
            result = subprocess.run(
                ["python3", str(scaffold_script), "list"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode != 0:
                print(f"  Scaffold list failed: {result.stderr}")
                return False
            
            if "Available templates" not in result.stdout:
                print("  Unexpected scaffold list output")
                return False
            
            # Test creating a project
            with tempfile.TemporaryDirectory() as tmpdir:
                test_project = Path(tmpdir) / "test-scaffold"
                result = subprocess.run(
                    ["python3", str(scaffold_script), "create", "minimal", "Test Project", "--target-dir", str(test_project)],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root
                )
                
                if result.returncode != 0:
                    print(f"  Scaffold create failed: {result.stderr}")
                    return False
                
                # Check created files
                expected_files = ["README.md", ".gitignore", "GUARDIAN.md"]
                for file_name in expected_files:
                    if not (test_project / file_name).exists():
                        print(f"  Missing scaffolded file: {file_name}")
                        return False
                
                # Check content substitution
                readme = (test_project / "README.md").read_text()
                if "Test Project" not in readme:
                    print("  Template variable substitution failed")
                    return False
            
            return True
        except Exception as e:
            print(f"  Error testing scaffolding: {e}")
            return False
    
    def test_agent_prompts_content(self):
        """Verify agent prompts have expected content."""
        agent_dir = self.project_root / ".opencode" / "agent"
        
        # Check Plan agent
        plan_prompt = (agent_dir / "plan.md").read_text()
        if "Architect" not in plan_prompt:
            print("  Plan prompt missing 'Architect' reference")
            return False
        
        # Check Build agent
        build_prompt = (agent_dir / "build.md").read_text()
        if "Builder" not in build_prompt:
            print("  Build prompt missing 'Builder' reference")
            return False
        
        # Check Guardian agent
        guardian_prompt = (agent_dir / "guardian.md").read_text()
        if "Guardian" not in guardian_prompt:
            print("  Guardian prompt missing 'Guardian' reference")
            return False
        
        # Check Ops agent
        ops_prompt = (agent_dir / "ops.md").read_text()
        if "Ops" not in ops_prompt:
            print("  Ops prompt missing 'Ops' reference")
            return False
        
        # Check Vision agent
        vision_prompt = (agent_dir / "vision.md").read_text()
        if "multimodal" not in vision_prompt.lower():
            print("  Vision prompt missing 'multimodal' reference")
            return False
        
        return True
    
    def test_workflow_documentation(self):
        """Verify workflow documentation is present and accurate."""
        workflow_file = self.project_root / "GUARDIAN_WORKFLOW.md"
        
        if not workflow_file.exists():
            print("  GUARDIAN_WORKFLOW.md not found")
            return False
        
        content = workflow_file.read_text()
        
        required_sections = [
            "Agent Lineup",
            "Quick Start",
            "Managing Models",
            "Workflow Loop",
            "Reusing in Other Projects"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"  Missing sections: {', '.join(missing_sections)}")
            return False
        
        return True
    
    def test_bootstrap_script(self):
        """Test bootstrap script functionality."""
        bootstrap_script = self.project_root / "guardian_system" / "bootstrap.sh"
        
        if not bootstrap_script.exists():
            print("  Bootstrap script not found")
            return False
        
        # Check script is executable
        if not bootstrap_script.stat().st_mode & 0o111:
            print("  Bootstrap script not executable")
            return False
        
        # Check script content
        content = bootstrap_script.read_text()
        required_elements = ["copy_file", "opencode", "GUARDIAN_WORKFLOW.md"]
        
        for element in required_elements:
            if element not in content:
                print(f"  Bootstrap script missing: {element}")
                return False
        
        return True
    
    def run_all_tests(self):
        """Run all test suites."""
        print("🧪 Running Comprehensive Guardian Framework Tests")
        print("=" * 70)
        
        tests = [
            ("Required Files", self.test_required_files),
            ("Model Configuration", self.test_model_configuration),
            ("Anomaly Ledger Schema", self.test_anomaly_ledger_schema),
            ("Scaffolding Functionality", self.test_scaffolding_functionality),
            ("Agent Prompts Content", self.test_agent_prompts_content),
            ("Workflow Documentation", self.test_workflow_documentation),
            ("Bootstrap Script", self.test_bootstrap_script),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 70)
        
        for test_name, passed, error in self.results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status}: {test_name}")
            if error and not passed:
                print(f"       Error: {error}")
        
        print(f"\n📈 Results: {self.pass_count}/{self.test_count} tests passed")
        
        if self.pass_count == self.test_count:
            print("\n🎉 All tests passed! Guardian Framework is STABLE.")
            return 0
        else:
            failed = self.test_count - self.pass_count
            print(f"\n💥 {failed} test(s) failed. Framework needs attention.")
            return 1


def main():
    """Main entry point."""
    project_root = Path(".")
    
    if not (project_root / ".opencode").exists():
        print("❌ Error: Not in a Guardian Framework project directory")
        print("   This test must be run from the root of a Guardian Framework project.")
        return 1
    
    tester = GuardianFrameworkTests(project_root)
    return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
