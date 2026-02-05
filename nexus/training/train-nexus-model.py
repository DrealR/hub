#!/usr/bin/env python3
"""
NEXUS Local Model Training Pipeline
====================================
Trains local Ollama models on Reemy's codebase patterns, decisions, and crystallized wisdom.

Usage:
    python train-nexus-model.py --mode extract    # Extract training data from codebase
    python train-nexus-model.py --mode train      # Train/fine-tune local model
    python train-nexus-model.py --mode test       # Test the trained model

Philosophy:
    Local models are NOT "dumb Claude" replacements.
    They are specialized memory/reflex systems:
    - Pattern recognition (what code patterns does Reemy use?)
    - Decision memory (what approaches worked before?)
    - Crystallized wisdom (condensed insights from past work)
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configuration
CONFIG = {
    "hub_path": Path(__file__).parent.parent.parent,  # /hub
    "output_dir": Path(__file__).parent / "data",
    "model_name": "nexus-memory",
    "base_model": "llama3.2:3b",  # Fast, can run on most hardware
    "training_patterns": [
        "*.py", "*.ts", "*.tsx", "*.js", "*.jsx",
        "*.md", "*.json", "*.yaml", "*.yml"
    ],
    "exclude_dirs": [
        "node_modules", ".git", "__pycache__", "dist", "build",
        ".next", ".cache", "coverage", ".pytest_cache"
    ],
    "max_file_size": 100_000,  # 100KB max per file
    "context_window": 4096
}


def log(message: str, level: str = "INFO"):
    """Log with timestamp and NEXUS styling."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "INFO": "\033[36m",    # Cyan
        "SUCCESS": "\033[32m", # Green
        "WARN": "\033[33m",    # Yellow
        "ERROR": "\033[31m",   # Red
        "RESET": "\033[0m"
    }
    color = colors.get(level, colors["INFO"])
    reset = colors["RESET"]
    print(f"{color}[NEXUS {timestamp}] {message}{reset}")


def check_ollama() -> bool:
    """Check if Ollama is installed and running."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def extract_code_patterns(hub_path: Path) -> List[Dict[str, Any]]:
    """Extract code patterns and structures from the codebase."""
    log("Extracting code patterns from codebase...")
    patterns = []

    for pattern in CONFIG["training_patterns"]:
        for file_path in hub_path.rglob(pattern):
            # Skip excluded directories
            if any(exc in str(file_path) for exc in CONFIG["exclude_dirs"]):
                continue

            # Skip large files
            try:
                if file_path.stat().st_size > CONFIG["max_file_size"]:
                    continue
            except OSError:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                # Extract meaningful patterns
                if len(content) > 100:  # Skip tiny files
                    patterns.append({
                        "file": str(file_path.relative_to(hub_path)),
                        "type": file_path.suffix,
                        "content": content[:CONFIG["context_window"]],
                        "size": len(content)
                    })
            except Exception as e:
                log(f"Error reading {file_path}: {e}", "WARN")

    log(f"Extracted {len(patterns)} code patterns", "SUCCESS")
    return patterns


def extract_decisions(hub_path: Path) -> List[Dict[str, Any]]:
    """Extract decision records from markdown files and comments."""
    log("Extracting decision records...")
    decisions = []

    # Look for decision patterns in markdown
    for md_file in hub_path.rglob("*.md"):
        if any(exc in str(md_file) for exc in CONFIG["exclude_dirs"]):
            continue

        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")

            # Find decision blocks
            if "DECISION:" in content or "Decision:" in content:
                decisions.append({
                    "source": str(md_file.relative_to(hub_path)),
                    "type": "decision",
                    "content": content[:CONFIG["context_window"]]
                })

            # Find architecture notes
            if any(kw in content.lower() for kw in ["architecture", "design", "approach", "strategy"]):
                decisions.append({
                    "source": str(md_file.relative_to(hub_path)),
                    "type": "architecture",
                    "content": content[:CONFIG["context_window"]]
                })
        except Exception as e:
            log(f"Error reading {md_file}: {e}", "WARN")

    log(f"Extracted {len(decisions)} decision records", "SUCCESS")
    return decisions


def extract_swarm_wisdom(hub_path: Path) -> List[Dict[str, Any]]:
    """Extract crystallized wisdom from swarm agents."""
    log("Extracting swarm crystallizations...")
    wisdom = []

    # Look for crystallization data
    crystal_paths = [
        hub_path / "data" / "swarm",
        hub_path / "projects" / "holographic-agent" / "packages" / "Swarm"
    ]

    for crystal_path in crystal_paths:
        if crystal_path.exists():
            for json_file in crystal_path.rglob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if isinstance(data, dict):
                        wisdom.append({
                            "source": str(json_file.relative_to(hub_path)),
                            "type": "crystallization",
                            "data": data
                        })
                except Exception as e:
                    log(f"Error reading {json_file}: {e}", "WARN")

    log(f"Extracted {len(wisdom)} crystallizations", "SUCCESS")
    return wisdom


def generate_training_data(patterns: List, decisions: List, wisdom: List) -> List[Dict]:
    """Generate training examples in Ollama format."""
    log("Generating training data...")
    training_data = []

    # Code pattern examples
    for pattern in patterns[:500]:  # Limit to prevent massive datasets
        training_data.append({
            "prompt": f"What is a typical {pattern['type']} file structure in this codebase?",
            "response": f"Based on {pattern['file']}:\n\n{pattern['content'][:1000]}"
        })

    # Decision examples
    for decision in decisions:
        training_data.append({
            "prompt": f"What decisions were made regarding {decision['source'].split('/')[-1]}?",
            "response": decision['content'][:2000]
        })

    # Wisdom examples
    for w in wisdom:
        if isinstance(w.get('data'), dict):
            training_data.append({
                "prompt": f"What insights exist in {w['source']}?",
                "response": json.dumps(w['data'], indent=2)[:2000]
            })

    log(f"Generated {len(training_data)} training examples", "SUCCESS")
    return training_data


def create_modelfile(output_dir: Path) -> Path:
    """Create Ollama Modelfile for fine-tuning."""
    modelfile_content = f"""# NEXUS Memory Model
# Specialized for Reemy's codebase patterns and decisions

FROM {CONFIG['base_model']}

# System prompt for NEXUS memory role
SYSTEM \"\"\"You are NEXUS Memory, a specialized AI assistant trained on Reemy's codebase.
Your role is to:
1. Remember code patterns and structures from the holographic-agent ecosystem
2. Recall past decisions and their rationale
3. Provide crystallized wisdom from the swarm agents
4. Assist with pattern matching and code completion

You are NOT a general-purpose assistant. You focus specifically on:
- TypeScript/Python patterns from this codebase
- Architecture decisions (holographic principle, swarm intelligence)
- Trading strategies (QuantumLeap, RepoToken)
- AI agent patterns (Swarm, NanoBot, Neural Arena)

Always ground your responses in specific files and patterns from the codebase.
\"\"\"

# Parameters optimized for memory/recall tasks
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx {CONFIG['context_window']}
PARAMETER repeat_penalty 1.1

# Template for consistent responses
TEMPLATE \"\"\"{{{{ if .System }}}}{{{{ .System }}}}{{{{ end }}}}
User: {{{{ .Prompt }}}}
NEXUS Memory: {{{{ .Response }}}}\"\"\"
"""

    modelfile_path = output_dir / "Modelfile"
    modelfile_path.write_text(modelfile_content)
    log(f"Created Modelfile at {modelfile_path}", "SUCCESS")
    return modelfile_path


def train_model(training_data: List[Dict], output_dir: Path):
    """Train the local model using Ollama."""
    log("Starting model training...")

    # Save training data
    training_file = output_dir / "training_data.jsonl"
    with open(training_file, "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")
    log(f"Saved training data to {training_file}")

    # Create Modelfile
    modelfile_path = create_modelfile(output_dir)

    # Create the model
    log("Creating NEXUS model in Ollama...")
    try:
        result = subprocess.run(
            ["ollama", "create", CONFIG["model_name"], "-f", str(modelfile_path)],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            log("Model created successfully!", "SUCCESS")
            log(f"Run with: ollama run {CONFIG['model_name']}")
        else:
            log(f"Model creation failed: {result.stderr}", "ERROR")
    except subprocess.TimeoutExpired:
        log("Model creation timed out", "ERROR")
    except Exception as e:
        log(f"Error creating model: {e}", "ERROR")


def test_model():
    """Test the trained model with sample queries."""
    log("Testing NEXUS Memory model...")

    test_queries = [
        "What is the holographic agent architecture?",
        "How does RepoToken handle staking?",
        "What patterns are used for swarm agents?",
        "What trading strategies exist in QuantumLeap?"
    ]

    for query in test_queries:
        log(f"\nQuery: {query}")
        try:
            result = subprocess.run(
                ["ollama", "run", CONFIG["model_name"], query],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print(f"Response: {result.stdout[:500]}...")
            else:
                log(f"Query failed: {result.stderr}", "ERROR")
        except Exception as e:
            log(f"Error: {e}", "ERROR")


def main():
    parser = argparse.ArgumentParser(description="NEXUS Local Model Training Pipeline")
    parser.add_argument(
        "--mode",
        choices=["extract", "train", "test", "full"],
        default="full",
        help="Operation mode"
    )
    parser.add_argument(
        "--hub",
        type=Path,
        default=CONFIG["hub_path"],
        help="Path to hub folder"
    )
    args = parser.parse_args()

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           NEXUS LOCAL MODEL TRAINING PIPELINE             ║
    ║      Training specialized memory for your codebase        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Check Ollama
    if not check_ollama():
        log("Ollama not found or not running!", "ERROR")
        log("Install from: https://ollama.ai")
        log("Then run: ollama serve")
        sys.exit(1)

    log(f"Ollama detected, using base model: {CONFIG['base_model']}")

    # Create output directory
    output_dir = CONFIG["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    hub_path = args.hub
    log(f"Hub path: {hub_path}")

    if args.mode in ["extract", "full"]:
        # Extract training data
        patterns = extract_code_patterns(hub_path)
        decisions = extract_decisions(hub_path)
        wisdom = extract_swarm_wisdom(hub_path)

        # Generate training examples
        training_data = generate_training_data(patterns, decisions, wisdom)

        # Save extracted data
        extract_file = output_dir / "extracted_data.json"
        with open(extract_file, "w") as f:
            json.dump({
                "patterns": len(patterns),
                "decisions": len(decisions),
                "wisdom": len(wisdom),
                "training_examples": len(training_data),
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        log(f"Saved extraction summary to {extract_file}", "SUCCESS")

    if args.mode in ["train", "full"]:
        # Load or generate training data
        if args.mode == "train":
            extract_file = output_dir / "extracted_data.json"
            if not extract_file.exists():
                log("No extracted data found. Run with --mode extract first", "ERROR")
                sys.exit(1)
            patterns = extract_code_patterns(hub_path)
            decisions = extract_decisions(hub_path)
            wisdom = extract_swarm_wisdom(hub_path)
            training_data = generate_training_data(patterns, decisions, wisdom)

        train_model(training_data, output_dir)

    if args.mode == "test":
        test_model()

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  TRAINING COMPLETE                        ║
    ╠═══════════════════════════════════════════════════════════╣
    ║  Next steps:                                              ║
    ║  1. Run: ollama run nexus-memory                          ║
    ║  2. Test with codebase-specific queries                   ║
    ║  3. Integrate with NEXUS dashboard                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
