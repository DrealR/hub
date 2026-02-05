#!/usr/bin/env python3
"""
Project scaffolding generator for Guardian Framework.
Creates new projects with proper Guardian agent setup and best practices.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional


class ProjectScaffolder:
    """Generates project scaffolding with Guardian Framework integration."""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)
    
    def list_templates(self) -> List[str]:
        """List available project templates."""
        if not self.templates_dir.exists():
            return []
        
        templates = []
        for item in self.templates_dir.iterdir():
            if item.is_dir() and (item / "template.json").exists():
                templates.append(item.name)
        
        return sorted(templates)
    
    def create_template(self, name: str, description: str, files: Dict[str, str]):
        """Create a new project template."""
        template_dir = self.templates_dir / name
        template_dir.mkdir(exist_ok=True)
        
        # Create template metadata
        metadata = {
            "name": name,
            "description": description,
            "created_at": "2025-11-10T00:00:00Z",
            "files": list(files.keys())
        }
        
        (template_dir / "template.json").write_text(
            json.dumps(metadata, indent=2) + "\n"
        )
        
        # Create template files
        for file_path, content in files.items():
            full_path = template_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
        
        print(f"✅ Template '{name}' created successfully")
    
    def scaffold_project(self, template_name: str, target_dir: Path, project_name: str) -> bool:
        """Scaffold a new project from a template."""
        template_dir = self.templates_dir / template_name
        
        if not template_dir.exists():
            print(f"❌ Template '{template_name}' not found")
            return False
        
        metadata_file = template_dir / "template.json"
        if not metadata_file.exists():
            print(f"❌ Template metadata missing for '{template_name}'")
            return False
        
        try:
            metadata = json.loads(metadata_file.read_text())
        except Exception as e:
            print(f"❌ Failed to read template metadata: {e}")
            return False
        
        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy template files
        for file_path in metadata.get("files", []):
            src = template_dir / file_path
            dst = target_dir / file_path
            
            if not src.exists():
                print(f"⚠️  Skipping missing template file: {file_path}")
                continue
            
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Replace template variables
            content = src.read_text()
            content = content.replace("{{PROJECT_NAME}}", project_name)
            content = content.replace("{{PROJECT_SLUG}}", project_name.lower().replace(" ", "-"))
            content = content.replace("{{CURRENT_DATE}}", "2025-11-10")
            
            dst.write_text(content)
        
        print(f"✅ Project '{project_name}' scaffolded from template '{template_name}'")
        print(f"📁 Location: {target_dir}")
        return True


def create_default_templates(templates_dir: Path):
    """Create default project templates."""
    scaffolder = ProjectScaffolder(templates_dir)
    
    # Node.js Project Template
    nodejs_files = {
        "package.json": json.dumps({
            "name": "{{PROJECT_SLUG}}",
            "version": "1.0.0",
            "description": "{{PROJECT_NAME}} - Built with Guardian Framework",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js",
                "test": "jest",
                "test:watch": "jest --watch",
                "lint": "eslint src/",
                "guardian": "cd .. && ./opencode-dual-agent.sh"
            },
            "keywords": ["guardian-framework"],
            "author": "",
            "license": "MIT",
            "devDependencies": {
                "jest": "^29.0.0",
                "nodemon": "^3.0.0",
                "eslint": "^8.0.0"
            }
        }, indent=2) + "\n",
        
        "src/index.js": '''// {{PROJECT_NAME}}
// Built with Guardian Framework

function main() {
  console.log("🚀 {{PROJECT_NAME}} is running");
  console.log("Use ./opencode-dual-agent.sh to start Guardian workflow");
}

if (require.main === module) {
  main();
}

module.exports = { main };
''',
        
        "src/index.test.js": '''// Tests for {{PROJECT_NAME}}
const { main } = require('./index');

describe('{{PROJECT_NAME}}', () => {
  test('should export main function', () => {
    expect(typeof main).toBe('function');
  });
  
  test('main should not throw', () => {
    expect(() => main()).not.toThrow();
  });
});
''',
        
        "README.md": '''# {{PROJECT_NAME}}

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
''',
        
        ".gitignore": '''node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.DS_Store
*.log
coverage/
.nyc_output
''',
        
        "GUARDIAN.md": '''# Guardian Framework Integration

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
'''
    }
    
    scaffolder.create_template("nodejs", "Node.js project with Guardian Framework integration", nodejs_files)
    
    # Python Project Template
    python_files = {
        "pyproject.toml": '''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{{PROJECT_SLUG}}"
version = "1.0.0"
description = "{{PROJECT_NAME}} - Built with Guardian Framework"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
keywords = ["guardian-framework"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=22.0",
    "flake8>=5.0",
    "mypy>=1.0",
]

[project.urls]
Homepage = "https://github.com/your-org/{{PROJECT_SLUG}}"
Repository = "https://github.com/your-org/{{PROJECT_SLUG}}"

[project.scripts]
{{PROJECT_SLUG}} = "{{PROJECT_SLUG}}.main:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov={{PROJECT_SLUG}} --cov-report=term-missing"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
''',
        
        "src/{{PROJECT_SLUG}}/__init__.py": '''"""{{PROJECT_NAME}} - Built with Guardian Framework."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
''',
        
        "src/{{PROJECT_SLUG}}/main.py": '''"""Main module for {{PROJECT_NAME}}."""


def main():
    """Main entry point."""
    print("🚀 {{PROJECT_NAME}} is running")
    print("Use ./opencode-dual-agent.sh to start Guardian workflow")
    print(f"Current working directory: {__import__('os').getcwd()}")


if __name__ == "__main__":
    main()
''',
        
        "tests/test_main.py": '''"""Tests for {{PROJECT_NAME}}."""

import pytest
from {{PROJECT_SLUG}}.main import main


def test_main_function_exists():
    """Test that main function exists and is callable."""
    assert callable(main)


def test_main_runs_without_error():
    """Test that main runs without raising exceptions."""
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() raised {e} unexpectedly")


def test_module_has_version():
    """Test that module has version information."""
    import {{PROJECT_SLUG}}
    assert hasattr({{PROJECT_SLUG}}, "__version__")
    assert isinstance({{PROJECT_SLUG}}.__version__, str)
''',
        
        "README.md": '''# {{PROJECT_NAME}}

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
''',
        
        ".gitignore": '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Environment variables
.env
.env.local
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
''',
        
        "GUARDIAN.md": '''# Guardian Framework Integration

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
'''
    }
    
    scaffolder.create_template("python", "Python project with Guardian Framework integration", python_files)
    
    # React Project Template
    react_files = {
        "package.json": json.dumps({
            "name": "{{PROJECT_SLUG}}",
            "version": "1.0.0",
            "description": "{{PROJECT_NAME}} - React app built with Guardian Framework",
            "private": True,
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "test:ci": "CI=true react-scripts test --coverage --watchAll=false",
                "eject": "react-scripts eject",
                "lint": "eslint src/",
                "lint:fix": "eslint src/ --fix",
                "guardian": "cd .. && ./opencode-dual-agent.sh"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1"
            },
            "devDependencies": {
                "@testing-library/jest-dom": "^5.16.5",
                "@testing-library/react": "^13.4.0",
                "@testing-library/user-event": "^14.4.3",
                "eslint": "^8.0.0",
                "web-vitals": "^2.1.4"
            },
            "eslintConfig": {
                "extends": ["react-app", "react-app/jest"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }, indent=2) + "\n",
        
        "public/index.html": '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="{{PROJECT_NAME}} - Built with Guardian Framework" />
    <title>{{PROJECT_NAME}}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
''',
        
        "src/index.js": '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''',
        
        "src/index.css": '''body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
''',
        
        "src/App.js": '''import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>{{PROJECT_NAME}}</h1>
        <p>Built with React and Guardian Framework</p>
        <div className="guardian-info">
          <h2>Guardian Workflow</h2>
          <p>This project uses the Guardian Framework for AI-assisted development:</p>
          <ol>
            <li><strong>Plan:</strong> Architectural planning and requirements</li>
            <li><strong>Build:</strong> Implementation with TDD approach</li>
            <li><strong>Guardian:</strong> Anomaly detection and review</li>
            <li><strong>Ops:</strong> Configuration and model management</li>
          </ol>
          <button onClick={() => window.open('../../../opencode-dual-agent.sh', '_blank')}>
            Start Guardian Workflow
          </button>
        </div>
      </header>
    </div>
  );
}

export default App;
''',
        
        "src/App.css": '''.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 40px;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.App-header h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.guardian-info {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 8px;
  margin-top: 2rem;
  max-width: 600px;
  text-align: left;
}

.guardian-info h2 {
  margin-top: 0;
}

.guardian-info ol {
  text-align: left;
}

.guardian-info button {
  background: #61dafb;
  color: #282c34;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

.guardian-info button:hover {
  background: #4fa8c5;
}
''',
        
        "src/App.test.js": '''import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders project name', () => {
  render(<App />);
  const heading = screen.getByRole('heading', { name: /{{PROJECT_NAME}}/i });
  expect(heading).toBeInTheDocument();
});

test('renders guardian workflow section', () => {
  render(<App />);
  const guardianHeading = screen.getByRole('heading', { name: /Guardian Workflow/i });
  expect(guardianHeading).toBeInTheDocument();
});

test('renders start workflow button', () => {
  render(<App />);
  const button = screen.getByRole('button', { name: /Start Guardian Workflow/i });
  expect(button).toBeInTheDocument();
});
''',
        
        "README.md": '''# {{PROJECT_NAME}}

React application built with [Guardian Framework](https://github.com/your-org/guardian-framework).

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Run tests
npm test

# Run tests in CI mode with coverage
npm run test:ci

# Build for production
npm build

# Start Guardian workflow
npm run guardian
```

## Project Structure

```
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── App.css
│   ├── App.test.js
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Available Scripts

- `npm start` - Run development server on http://localhost:3000
- `npm test` - Run tests in watch mode
- `npm run test:ci` - Run tests once with coverage
- `npm build` - Build optimized production bundle
- `npm run lint` - Lint code with ESLint
- `npm run lint:fix` - Lint and auto-fix issues
- `npm run guardian` - Start Guardian workflow

## Guardian Framework Integration

This project uses the Guardian Framework for AI-assisted development:

1. **Plan** - Architectural planning and component design
2. **Build** - Implementation with TDD approach
3. **Guardian** - Code review and anomaly detection
4. **Ops** - Configuration and dependency management
5. **Vision** - UI/UX analysis and design feedback

## Testing

Tests are written using React Testing Library and Jest. Run `npm test` to start the test runner in watch mode.

## Development Workflow

1. Start Guardian: `npm run guardian` or `./opencode-dual-agent.sh`
2. Plan agent helps with component architecture
3. Build agent implements features with tests
4. Guardian agent reviews for issues
5. Iterate until all tests pass

## Learn More

- [React Documentation](https://reactjs.org/)
- [Guardian Framework Workflow](../GUARDIAN_WORKFLOW.md)
- [Create React App](https://create-react-app.dev/)
''',
        
        ".gitignore": '''# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Production
build/

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
''',
        
        "GUARDIAN.md": '''# Guardian Framework Integration

This React project is configured for Guardian Framework development workflow.

## Getting Started

1. Ensure Guardian Framework is set up in the parent directory
2. Run `./opencode-dual-agent.sh` to start the workflow
3. Use the Plan agent for component architecture and state management design
4. Use the Build agent for implementation with TDD
5. Use the Guardian agent for code review and performance analysis
6. Use the Vision agent for UI/UX feedback on designs and mockups

## React-Specific Best Practices

- Write component tests before implementation (TDD)
- Use functional components with hooks
- Keep components small and focused on single responsibilities
- Document prop types and component interfaces
- Use React Testing Library for user-centric tests
- Monitor performance with React DevTools
- Document all anomalies in `.opencode/anomaly-ledger.json`
- Review changes with Guardian agent before merging

## Common Guardian Workflows

### New Component Creation
1. Plan: Design component API and state management
2. Build: Implement component with tests
3. Guardian: Review for performance and best practices
4. Vision: Analyze UI/UX if designs are provided

### State Management Changes
1. Plan: Design state architecture and data flow
2. Build: Implement with comprehensive tests
3. Guardian: Review for complexity and performance impact

### UI/UX Updates
1. Vision: Analyze mockups and provide feedback
2. Plan: Update component architecture if needed
3. Build: Implement visual changes
4. Guardian: Review accessibility and performance
'''
    }
    
    scaffolder.create_template("react", "React application with Guardian Framework integration", react_files)
    
    # FastAPI Project Template
    fastapi_files = {
        "pyproject.toml": '''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{{PROJECT_SLUG}}"
version = "1.0.0"
description = "{{PROJECT_NAME}} - FastAPI service built with Guardian Framework"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
keywords = ["guardian-framework", "fastapi", "api"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.20.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21.0",
    "black>=22.0",
    "flake8>=5.0",
    "mypy>=1.0",
    "httpx>=0.24.0",
]

[project.urls]
Homepage = "https://github.com/your-org/{{PROJECT_SLUG}}"
Repository = "https://github.com/your-org/{{PROJECT_SLUG}}"

[project.scripts]
{{PROJECT_SLUG}} = "{{PROJECT_SLUG}}.main:main"
dev = "{{PROJECT_SLUG}}.main:dev"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov={{PROJECT_SLUG}} --cov-report=term-missing --cov-report=html"
asyncio_mode = "auto"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
''',
        
        "src/{{PROJECT_SLUG}}/__init__.py": '''"""{{PROJECT_NAME}} - FastAPI service built with Guardian Framework."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
''',
        
        "src/{{PROJECT_SLUG}}/main.py": '''"""Main application entry point."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .core.config import settings


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="{{PROJECT_DESCRIPTION}}",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        """Root endpoint with project information."""
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "message": "{{PROJECT_NAME}} is running",
            "guardian_framework": "Active",
            "docs": "/docs",
            "health": "/health"
        }
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "timestamp": "{{CURRENT_DATE}}"}
    
    return app


def main():
    """Run the application."""
    app = create_application()
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
    )


def dev():
    """Run the application in development mode."""
    app = create_application()
    uvicorn.run(
        "src.{{PROJECT_SLUG}}.main:create_application",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()
''',
        
        "src/{{PROJECT_SLUG}}/core/__init__.py": '"""Core modules."""',
        
        "src/{{PROJECT_SLUG}}/core/config.py": '''"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    PROJECT_NAME: str = "{{PROJECT_NAME}}"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "{{PROJECT_DESCRIPTION}}"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    ALLOWED_HOSTS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
''',
        
        "src/{{PROJECT_SLUG}}/api/__init__.py": '"""API modules."""',
        
        "src/{{PROJECT_SLUG}}/api/routes.py": '''"""API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def get_status():
    """Get API status."""
    return {
        "status": "operational",
        "service": "{{PROJECT_NAME}}",
        "version": "1.0.0"
    }


@router.get("/items")
async def get_items():
    """Get sample items."""
    return {
        "items": [
            {"id": 1, "name": "Sample Item 1"},
            {"id": 2, "name": "Sample Item 2"},
        ]
    }
''',
        
        "tests/__init__.py": '"""Test suite."""',
        
        "tests/test_main.py": '''"""Tests for main application."""

import pytest
from fastapi.testclient import TestClient

from {{PROJECT_SLUG}}.main import create_application


@pytest.fixture
def client():
    """Create test client."""
    app = create_application()
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "guardian_framework" in data


def test_health_endpoint(client):
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_status_endpoint(client):
    """Test API status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["service"] == "{{PROJECT_NAME}}"


def test_api_items_endpoint(client):
    """Test API items endpoint."""
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 2
''',
        
        ".env.example": '''# {{PROJECT_NAME}} Configuration
# Copy this file to .env and update values as needed

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Settings
# ALLOWED_HOSTS=["http://localhost:3000"]

# Logging
LOG_LEVEL=info
''',
        
        ".gitignore": '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Environment variables
.env
.env.local
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# FastAPI / Uvicorn
*.log
''',
        
        "README.md": '''# {{PROJECT_NAME}}

FastAPI service built with [Guardian Framework](https://github.com/your-org/guardian-framework).

## Quick Start

```bash
# Install in development mode
pip install -e ".[dev]"

# Run development server with auto-reload
python -m {{PROJECT_SLUG}}.main:dev

# Or use the dev command
python -m {{PROJECT_SLUG}}.main --dev

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

## API Endpoints

- `GET /` - Root endpoint with project information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /api/v1/status` - API status
- `GET /api/v1/items` - Sample items endpoint

## Project Structure

```
├── src/
│   └── {{PROJECT_SLUG}}/
│       ├── api/
│       │   └── routes.py
│       ├── core/
│       │   └── config.py
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── pyproject.toml
├── .env.example
└── README.md
```

## Configuration

Copy `.env.example` to `.env` and update values as needed:

```bash
cp .env.example .env
```

## Guardian Framework Integration

This project uses the Guardian Framework for AI-assisted development:

1. **Plan** - API design and architecture planning
2. **Build** - Implementation with TDD and Pydantic models
3. **Guardian** - Security review and performance analysis
4. **Ops** - Configuration and dependency management
5. **Vision** - API documentation review

## Development Workflow

1. Start Guardian: `./opencode-dual-agent.sh`
2. Plan agent helps with API design and Pydantic schemas
3. Build agent implements endpoints with tests
4. Guardian agent reviews for security and performance
5. Iterate until all tests pass

## Testing

Tests use pytest with FastAPI TestClient. Run `pytest` to execute the test suite with coverage reporting.

## Deployment

For production deployment:

```bash
# Install production dependencies
pip install .

# Run with Uvicorn
uvicorn src.{{PROJECT_SLUG}}.main:create_application --factory --host 0.0.0.0 --port 8000
```

## API Documentation

When running, access interactive documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
''',
        
        "GUARDIAN.md": '''# Guardian Framework Integration

This FastAPI project is configured for Guardian Framework development workflow.

## Getting Started

1. Ensure Guardian Framework is set up in the parent directory
2. Run `./opencode-dual-agent.sh` to start the workflow
3. Use the Plan agent for API design and architecture
4. Use the Build agent for implementation with TDD
5. Use the Guardian agent for security and performance review
6. Use the Vision agent for API documentation analysis

## FastAPI-Specific Best Practices

- Design Pydantic models first (schema-driven development)
- Write tests for each endpoint using TestClient
- Use dependency injection for database and services
- Document all endpoints with descriptive docstrings
- Use type hints throughout (enforced by mypy)
- Validate input data with Pydantic
- Document all anomalies in `.opencode/anomaly-ledger.json`
- Review changes with Guardian agent before merging

## Common Guardian Workflows

### New Endpoint Creation
1. Plan: Design request/response schemas
2. Build: Implement endpoint with tests
3. Guardian: Review for security and performance
4. Vision: Review API documentation

### Pydantic Model Changes
1. Plan: Design updated schema
2. Build: Implement model changes with migration plan
3. Guardian: Review for breaking changes

### Database Integration
1. Plan: Design data models and relationships
2. Build: Implement with SQLAlchemy or similar
3. Guardian: Review for SQL injection and N+1 issues
'''
    }
    
    scaffolder.create_template("fastapi", "FastAPI service with Guardian Framework integration", fastapi_files)
    
    # Minimal Project Template
    minimal_files = {
        "README.md": '''# {{PROJECT_NAME}}

Minimal project template for Guardian Framework.

## Quick Start

```bash
# Start Guardian workflow
./opencode-dual-agent.sh
```

## Project Structure

```
├── README.md
└── .gitignore
```

Add your project files as needed.
''',
        
        ".gitignore": '''# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
''',
        
        "GUARDIAN.md": '''# Guardian Framework Integration

This project uses the Guardian Framework for AI-assisted development.

## Getting Started

1. Run `./opencode-dual-agent.sh` to start the workflow
2. Use the Plan agent for planning
3. Use the Build agent for implementation
4. Use the Guardian agent for review

## Workflow

1. Start in Plan mode for requirements
2. Switch to Build mode for implementation
3. Guardian mode for review and anomaly detection
4. Ops mode for configuration
'''
    }
    
    scaffolder.create_template("minimal", "Minimal project template", minimal_files)
    
    print("✅ All default templates created successfully")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Guardian Framework Project Scaffolder"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List templates
    list_parser = subparsers.add_parser("list", help="List available templates")
    
    # Create project
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("template", help="Template name")
    create_parser.add_argument("project_name", help="Project name")
    create_parser.add_argument("--target-dir", help="Target directory (default: ./project-name)")
    
    # Initialize templates
    init_parser = subparsers.add_parser("init", help="Initialize default templates")
    
    args = parser.parse_args()
    
    templates_dir = Path(".opencode/templates")
    scaffolder = ProjectScaffolder(templates_dir)
    
    if args.command == "list":
        templates = scaffolder.list_templates()
        if templates:
            print("📋 Available templates:")
            for template in templates:
                print(f"  - {template}")
        else:
            print("No templates found. Run 'init' to create default templates.")
    
    elif args.command == "create":
        target_dir = Path(args.target_dir) if args.target_dir else Path(args.project_name.replace(" ", "-").lower())
        success = scaffolder.scaffold_project(args.template, target_dir, args.project_name)
        sys.exit(0 if success else 1)
    
    elif args.command == "init":
        create_default_templates(templates_dir)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
