# {{PROJECT_NAME}}

Built with [Guardian Framework](https://github.com/your-org/guardian-framework).

## Quick Start

```bash
# Install in development mode
pip install -e ".[dev]"

# Run the application
python -m {{PROJECT_SLUG}}.main

# Run tests
pytest

# Run tests with coverage
pytest --cov={{PROJECT_SLUG}}

# Format code
black src/ tests/

# Type checking
mypy src/

# Lint code
flake8 src/ tests/
```

## Project Structure

```
├── src/
│   └── {{PROJECT_SLUG}}/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── pyproject.toml
└── README.md
```

## Guardian Workflow

This project uses the Guardian Framework for AI-assisted development:

1. **Plan**: Architectural planning and requirements gathering
2. **Build**: Implementation with TDD approach
3. **Guardian**: Anomaly detection and security review
4. **Ops**: Configuration and model management

Run `./opencode-dual-agent.sh` to start the workflow.

## Development Commands

- `pytest` - Run tests
- `pytest --cov={{PROJECT_SLUG}}` - Run tests with coverage
- `black src/ tests/` - Format code
- `mypy src/` - Type checking
- `flake8 src/ tests/` - Lint code
- `./opencode-dual-agent.sh` - Start Guardian workflow
