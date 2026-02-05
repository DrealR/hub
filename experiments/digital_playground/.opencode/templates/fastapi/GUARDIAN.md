# Guardian Framework Integration

This FastAPI project uses Guardian Framework for AI-assisted development.

## Getting Started

1. Run `./opencode-dual-agent.sh` to start the workflow
2. Use Plan agent for API design and Pydantic schemas
3. Use Build agent for implementation with TDD
4. Use Guardian agent for security review
5. Use Vision agent for API docs review

## Best Practices

- Design Pydantic models first
- Write tests for each endpoint
- Use dependency injection
- Document endpoints with docstrings
- Use type hints throughout
- Validate input with Pydantic
- Document anomalies