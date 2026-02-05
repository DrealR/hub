# Guardian Framework Integration

This project is configured for Guardian Framework development workflow.

## Getting Started

1. Ensure Guardian Framework is set up in the parent directory
2. Run `./opencode-dual-agent.sh` to start the workflow
3. Use the Plan agent for architectural decisions
4. Use the Build agent for implementation
5. Use the Guardian agent for review and anomaly detection

## Best Practices

- Write tests before implementation (TDD)
- Use pytest for testing with coverage reporting
- Document all anomalies in `.opencode/anomaly-ledger.json`
- Use type hints and run mypy for type checking
- Format code with black before committing
- Review changes with Guardian agent before merging

## Development Workflow

1. Start with Guardian: `./opencode-dual-agent.sh`
2. Switch to Plan agent for requirements
3. Plan agent delegates to Build for implementation
4. Build agent writes tests first, then implementation
5. Guardian agent reviews for anomalies
6. Iterate until all tests pass and Guardian approves
