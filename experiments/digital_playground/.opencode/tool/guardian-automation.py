#!/usr/bin/env python3
"""
Guardian Automation System for Anomaly Detection.
Proactively scans for configuration issues, security vulnerabilities, and code quality problems.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GuardianAutomation:
    """Automated anomaly detection and reporting system."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.anomaly_ledger = project_root / ".opencode" / "anomaly-ledger.json"
        self.config_dir = project_root / ".opencode"
    
    def load_ledger(self) -> Dict:
        """Load the anomaly ledger."""
        if not self.anomaly_ledger.exists():
            return {
                "system_state": "STABLE",
                "last_updated": datetime.now().isoformat(),
                "anomalies": [],
                "metrics": {
                    "total_anomalies": 0,
                    "active_anomalies": 0,
                    "resolved_anomalies": 0,
                    "false_positives": 0
                }
            }
        
        try:
            return json.loads(self.anomaly_ledger.read_text())
        except Exception as e:
            print(f"❌ Error loading anomaly ledger: {e}")
            return {
                "system_state": "UNSTABLE",
                "last_updated": datetime.now().isoformat(),
                "anomalies": [],
                "metrics": {
                    "total_anomalies": 0,
                    "active_anomalies": 0,
                    "resolved_anomalies": 0,
                    "false_positives": 0
                }
            }
    
    def save_ledger(self, ledger: Dict):
        """Save the anomaly ledger."""
        ledger["last_updated"] = datetime.now().isoformat()
        self.anomaly_ledger.write_text(json.dumps(ledger, indent=2) + "\n")
    
    def add_anomaly(self, title: str, description: str, severity: str, 
                   reproduction_steps: Optional[List[str]] = None, 
                   linked_files: Optional[List[str]] = None,
                   tags: Optional[List[str]] = None) -> str:
        """Add a new anomaly to the ledger."""
        ledger = self.load_ledger()
        
        anomaly_id = f"anomaly-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        anomaly = {
            "id": anomaly_id,
            "title": title,
            "description": description,
            "severity": severity,
            "status": "detected",
            "detected_at": datetime.now().isoformat(),
            "owner": "guardian-automation",
            "reproduction_steps": reproduction_steps if reproduction_steps is not None else [],
            "linked_files": linked_files if linked_files is not None else [],
            "tags": tags if tags is not None else ["automation"],
            "remediation_notes": ""
        }
        
        ledger["anomalies"].append(anomaly)
        ledger["metrics"]["total_anomalies"] += 1
        ledger["metrics"]["active_anomalies"] += 1
        ledger["system_state"] = "UNSTABLE"
        
        self.save_ledger(ledger)
        return anomaly_id
    
    def resolve_anomaly(self, anomaly_id: str, notes: str = ""):
        """Mark an anomaly as resolved."""
        ledger = self.load_ledger()
        
        for anomaly in ledger["anomalies"]:
            if anomaly["id"] == anomaly_id and anomaly["status"] != "resolved":
                anomaly["status"] = "resolved"
                anomaly["resolved_at"] = datetime.now().isoformat()
                anomaly["remediation_notes"] = notes
                ledger["metrics"]["active_anomalies"] -= 1
                ledger["metrics"]["resolved_anomalies"] += 1
                break
        
        # Update system state
        active_count = ledger["metrics"]["active_anomalies"]
        ledger["system_state"] = "STABLE" if active_count == 0 else "UNSTABLE"
        
        self.save_ledger(ledger)
    
    def scan_configuration_drift(self) -> List[Dict]:
        """Scan for configuration drift between model files."""
        anomalies = []
        
        # Load configurations
        models_file = self.config_dir / "models.json"
        opencode_file = self.project_root / "opencode.json"
        
        if not models_file.exists():
            anomalies.append({
                "title": "Missing models.json configuration",
                "description": "The models.json file is missing from .opencode/",
                "severity": "high",
                "linked_files": [str(models_file)],
                "tags": ["configuration", "missing-file"]
            })
            return anomalies
        
        if not opencode_file.exists():
            anomalies.append({
                "title": "Missing opencode.json configuration",
                "description": "The opencode.json file is missing from project root",
                "severity": "high",
                "linked_files": [str(opencode_file)],
                "tags": ["configuration", "missing-file"]
            })
            return anomalies
        
        try:
            models_data = json.loads(models_file.read_text())
            opencode_data = json.loads(opencode_file.read_text())
            
            current_models = models_data.get("current_models", {})
            agent_config = opencode_data.get("agent", {})
            
            # Check for mismatches
            for agent_name, expected_model in current_models.items():
                if agent_name not in agent_config:
                    anomalies.append({
                        "title": f"Missing agent configuration: {agent_name}",
                        "description": f"Agent '{agent_name}' is in models.json but not in opencode.json",
                        "severity": "medium",
                        "linked_files": [str(models_file), str(opencode_file)],
                        "tags": ["configuration", "missing-agent", agent_name]
                    })
                else:
                    actual_model = agent_config[agent_name].get("model")
                    if actual_model != expected_model:
                        anomalies.append({
                            "title": f"Model mismatch for {agent_name}",
                            "description": f"Expected '{expected_model}', found '{actual_model}'",
                            "severity": "medium",
                            "linked_files": [str(models_file), str(opencode_file)],
                            "tags": ["configuration", "model-mismatch", agent_name]
                        })
            
            # Check agent prompt files
            agent_dir = self.config_dir / "agent"
            for agent_name in current_models.keys():
                prompt_file = agent_dir / f"{agent_name}.md"
                if not prompt_file.exists():
                    anomalies.append({
                        "title": f"Missing agent prompt: {agent_name}.md",
                        "description": f"Agent prompt file not found: {prompt_file}",
                        "severity": "medium",
                        "linked_files": [str(prompt_file)],
                        "tags": ["configuration", "missing-prompt", agent_name]
                    })
        
        except Exception as e:
            anomalies.append({
                "title": "Configuration parsing error",
                "description": f"Failed to parse configuration files: {e}",
                "severity": "high",
                "linked_files": [str(models_file), str(opencode_file)],
                "tags": ["configuration", "parsing-error"]
            })
        
        return anomalies
    
    def scan_security_issues(self) -> List[Dict]:
        """Scan for common security issues."""
        anomalies = []
        
        # Check for exposed API keys in files
        sensitive_patterns = [
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI-style API key"),
            (r'xox[baprs]-[a-zA-Z0-9]{10,}', "Slack token"),
            (r'-----BEGIN [A-Z ]+-----', "Private key"),
            (r'gh[ps]_[a-zA-Z0-9]{36}', "GitHub token"),
            (r'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*', "JWT token"),
        ]
        
        # Files to check (avoid node_modules, etc.)
        check_extensions = {'.js', '.ts', '.py', '.md', '.json', '.sh', '.yaml', '.yml', '.env'}
        skip_dirs = {'node_modules', '.git', '__pycache__', 'venv', 'env', 'dist', 'build'}
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                # Skip directories
                if any(skip_dir in str(file_path) for skip_dir in skip_dirs):
                    continue
                
                # Check extension
                if file_path.suffix not in check_extensions:
                    continue
                
                try:
                    content = file_path.read_text(errors='ignore')
                    
                    for pattern, description in sensitive_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            # Check if it's in a safe context (example, placeholder)
                            context_safe = any(placeholder in content.lower() 
                                             for placeholder in ['example', 'placeholder', 'your-', 'fake', 'test'])
                            
                            if not context_safe:
                                anomalies.append({
                                    "title": f"Potential {description} exposed",
                                    "description": f"Found {len(matches)} {description}(s) in {file_path.name}",
                                    "severity": "critical",
                                    "linked_files": [str(file_path)],
                                    "tags": ["security", "exposed-secret", file_path.suffix[1:]]
                                })
                
                except Exception:
                    # Skip files we can't read
                    continue
        
        return anomalies
    
    def scan_code_quality(self) -> List[Dict]:
        """Scan for code quality issues."""
        anomalies = []
        
        # Check for large files
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and file_path.suffix in {'.js', '.ts', '.py', '.md'}:
                try:
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    if size_mb > 5:  # 5MB
                        anomalies.append({
                            "title": f"Large file detected: {file_path.name}",
                            "description": f"File is {size_mb:.2f}MB, consider splitting",
                            "severity": "low",
                            "linked_files": [str(file_path)],
                            "tags": ["quality", "large-file", file_path.suffix[1:]]
                        })
                except Exception:
                    continue
        
        # Check for missing tests
        src_files = []
        test_files = []
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                if '/src/' in str(file_path) or '/lib/' in str(file_path):
                    if file_path.suffix in {'.js', '.ts', '.py'}:
                        src_files.append(file_path)
                elif '/test/' in str(file_path) or '/tests/' in str(file_path):
                    if file_path.suffix in {'.js', '.ts', '.py'}:
                        test_files.append(file_path)
        
        if src_files and not test_files:
            anomalies.append({
                "title": "No test files found",
                "description": f"Found {len(src_files)} source files but no tests",
                "severity": "medium",
                "linked_files": [str(f) for f in src_files[:5]],  # List first 5
                "tags": ["quality", "missing-tests"]
            })
        
        return anomalies
    
    def scan_test_failures(self) -> List[Dict]:
        """Run tests and check for failures."""
        anomalies = []
        
        # Look for test files
        test_files = list(self.project_root.rglob("test*.py"))
        
        if test_files:
            # Try to run tests
            try:
                result = subprocess.run(
                    ["python3", "-m", "pytest", "-v", "--tb=short"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                    timeout=60  # 1 minute timeout
                )
                
                if result.returncode != 0:
                    # Parse failures
                    failure_lines = []
                    for line in result.stdout.split('\n'):
                        if 'FAILED' in line or 'ERROR' in line:
                            failure_lines.append(line)
                    
                    anomalies.append({
                        "title": "Test failures detected",
                        "description": f"{len(failure_lines)} test(s) failed. Run pytest for details.",
                        "severity": "high",
                        "reproduction_steps": [
                            "cd " + str(self.project_root),
                            "python3 -m pytest -v"
                        ],
                        "tags": ["testing", "test-failure"]
                    })
            
            except subprocess.TimeoutExpired:
                anomalies.append({
                    "title": "Test timeout",
                    "description": "Tests took too long to run (timeout after 60s)",
                    "severity": "medium",
                    "tags": ["testing", "timeout"]
                })
            except Exception as e:
                # Tests might not be set up properly
                pass
        
        return anomalies
    
    def run_full_scan(self) -> Tuple[int, int]:
        """
        Run a complete anomaly detection scan.
        Returns (new_anomalies, total_anomalies)
        """
        print("🔍 Guardian Automation: Running full anomaly scan...")
        
        all_scanners = [
            ("Configuration Drift", self.scan_configuration_drift),
            ("Security Issues", self.scan_security_issues),
            ("Code Quality", self.scan_code_quality),
            ("Test Failures", self.scan_test_failures)
        ]
        
        new_anomaly_count = 0
        total_found = 0
        
        for scan_name, scanner_func in all_scanners:
            print(f"  📋 Scanning: {scan_name}...")
            try:
                anomalies = scanner_func()
                total_found += len(anomalies)
                
                for anomaly in anomalies:
                    # Check if this anomaly already exists
                    if not self.anomaly_exists(anomaly["title"]):
                        self.add_anomaly(
                            title=anomaly["title"],
                            description=anomaly["description"],
                            severity=anomaly["severity"],
                            reproduction_steps=anomaly.get("reproduction_steps"),
                            linked_files=anomaly.get("linked_files"),
                            tags=anomaly.get("tags", [])
                        )
                        new_anomaly_count += 1
                        print(f"    🚨 New anomaly: {anomaly['title']}")
                    else:
                        print(f"    ℹ️  Known anomaly: {anomaly['title']}")
            
            except Exception as e:
                print(f"    ❌ Scanner failed: {e}")
        
        print(f"\n📊 Scan complete: {new_anomaly_count} new anomalies, {total_found} total found")
        return new_anomaly_count, total_found
    
    def anomaly_exists(self, title: str) -> bool:
        """Check if an anomaly with this title already exists."""
        ledger = self.load_ledger()
        
        for anomaly in ledger["anomalies"]:
            if anomaly["title"] == title and anomaly["status"] != "resolved":
                return True
        
        return False
    
    def generate_report(self) -> str:
        """Generate a human-readable anomaly report."""
        ledger = self.load_ledger()
        
        report = []
        report.append("🔍 Guardian Anomaly Report")
        report.append("=" * 50)
        report.append(f"System State: {ledger['system_state']}")
        report.append(f"Last Updated: {ledger['last_updated']}")
        report.append("")
        
        metrics = ledger["metrics"]
        report.append("📊 Metrics:")
        report.append(f"  Total Anomalies: {metrics['total_anomalies']}")
        report.append(f"  Active Anomalies: {metrics['active_anomalies']}")
        report.append(f"  Resolved Anomalies: {metrics['resolved_anomalies']}")
        report.append(f"  False Positives: {metrics['false_positives']}")
        report.append("")
        
        active_anomalies = [a for a in ledger["anomalies"] if a["status"] != "resolved"]
        
        if active_anomalies:
            report.append("🚨 Active Anomalies:")
            report.append("")
            
            # Group by severity
            by_severity = {"critical": [], "high": [], "medium": [], "low": []}
            for anomaly in active_anomalies:
                severity = anomaly.get("severity", "medium")
                by_severity[severity].append(anomaly)
            
            for severity in ["critical", "high", "medium", "low"]:
                if by_severity[severity]:
                    report.append(f"  {severity.upper()}:")
                    for anomaly in by_severity[severity]:
                        report.append(f"    • {anomaly['title']}")
                        if anomaly.get("description"):
                            desc = anomaly["description"][:80] + "..." if len(anomaly["description"]) > 80 else anomaly["description"]
                            report.append(f"      {desc}")
                    report.append("")
        else:
            report.append("✅ No active anomalies. System is STABLE.")
        
        return "\n".join(report)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: guardian-automation.py <command>")
        print("Commands:")
        print("  scan              - Run full anomaly scan")
        print("  report            - Generate anomaly report")
        print("  resolve <id>      - Resolve an anomaly")
        print("  config-drift      - Check configuration drift only")
        print("  security          - Check security issues only")
        print("  quality           - Check code quality only")
        sys.exit(1)
    
    command = sys.argv[1]
    project_root = Path(".")
    guardian = GuardianAutomation(project_root)
    
    if command == "scan":
        new_anomalies, total_found = guardian.run_full_scan()
        print("\n" + guardian.generate_report())
        sys.exit(0 if new_anomalies == 0 else 1)
    
    elif command == "report":
        print(guardian.generate_report())
    
    elif command == "resolve":
        if len(sys.argv) < 3:
            print("❌ Anomaly ID required")
            sys.exit(1)
        
        anomaly_id = sys.argv[2]
        notes = sys.argv[3] if len(sys.argv) > 3 else "Resolved via automation"
        guardian.resolve_anomaly(anomaly_id, notes)
        print(f"✅ Anomaly {anomaly_id} resolved")
    
    elif command == "config-drift":
        anomalies = guardian.scan_configuration_drift()
        for anomaly in anomalies:
            guardian.add_anomaly(**anomaly)
        print(f"✅ Configuration drift scan complete: {len(anomalies)} issues found")
    
    elif command == "security":
        anomalies = guardian.scan_security_issues()
        for anomaly in anomalies:
            guardian.add_anomaly(**anomaly)
        print(f"✅ Security scan complete: {len(anomalies)} issues found")
    
    elif command == "quality":
        anomalies = guardian.scan_code_quality()
        for anomaly in anomalies:
            guardian.add_anomaly(**anomaly)
        print(f"✅ Quality scan complete: {len(anomalies)} issues found")
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
