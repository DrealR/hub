# {{PROJECT_NAME}}

FastAPI service built with Guardian Framework.

## Quick Start

```bash
pip install -e ".[dev]"
python -m {{PROJECT_SLUG}}.main:dev  # Development server
pytest  # Run tests
```

## API Endpoints

- `GET /` - Project information
- `GET /health` - Health check
- `GET /docs` - Interactive API docs
- `GET /api/v1/status` - API status
- `GET /api/v1/items` - Sample items

## Guardian Integration

Uses Guardian Framework for AI-assisted API development.