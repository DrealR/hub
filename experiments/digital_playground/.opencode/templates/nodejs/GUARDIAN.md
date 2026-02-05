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
- Document all anomalies in `.opencode/anomaly-ledger.json`
- Use meaningful commit messages
- Review changes with Guardian agent before merging
