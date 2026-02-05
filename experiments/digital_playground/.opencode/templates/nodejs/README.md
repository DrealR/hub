# {{PROJECT_NAME}}

Built with [Guardian Framework](https://github.com/your-org/guardian-framework).

## Quick Start

```bash
# Install dependencies
npm install

# Run development mode
npm run dev

# Run tests
npm test

# Start Guardian workflow
npm run guardian
```

## Project Structure

```
├── src/
│   ├── index.js      # Main entry point
│   └── index.test.js # Tests
├── package.json
└── README.md
```

## Guardian Workflow

This project uses the Guardian Framework for AI-assisted development:

1. **Plan**: Architectural planning and requirements gathering
2. **Build**: Implementation with TDD approach
3. **Guardian**: Anomaly detection and security review
4. **Ops**: Configuration and model management

Run `./opencode-dual-agent.sh` to start the workflow.

## Scripts

- `npm start` - Run production server
- `npm run dev` - Run development with auto-reload
- `npm test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run lint` - Lint code
- `npm run guardian` - Start Guardian workflow
