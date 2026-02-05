# Context Prime

Prime Claude with comprehensive project context: $ARGUMENTS

---

## Context Loading Protocol

### Step 1: Core Documentation
Read these files in order:
1. `README.md` - Project overview
2. `CLAUDE.md` - AI-specific instructions (if exists)
3. `CONTRIBUTING.md` - Contribution guidelines (if exists)
4. `ARCHITECTURE.md` or `docs/architecture.md` (if exists)

### Step 2: Project Structure
```bash
git ls-files | head -100
```

Understand:
- Directory organization
- Key source directories
- Test locations
- Configuration files

### Step 3: Dependencies & Stack
Check for and read:
- `package.json` - Node.js projects
- `Cargo.toml` - Rust projects
- `go.mod` - Go projects
- `pyproject.toml` or `requirements.txt` - Python projects
- `docker-compose.yml` - Container setup
- `.env.example` - Environment variables

### Step 4: Recent Activity
```bash
git log --oneline -20
git branch -a
```

Understand:
- Recent changes and focus areas
- Active branches
- Development patterns

### Step 5: Build & Test Commands
Identify key commands:
- How to install dependencies
- How to run the dev server
- How to run tests
- How to build for production

## Context Summary Template

After loading, provide:

```
┌─────────────────────────────────────────┐
│           PROJECT CONTEXT               │
├─────────────────────────────────────────┤
│ Name: <project name>                    │
│ Type: <web app/CLI/library/etc>         │
│ Stack: <main technologies>              │
│ Language: <primary language>            │
├─────────────────────────────────────────┤
│ Key Commands:                           │
│ • Install: <command>                    │
│ • Dev: <command>                        │
│ • Test: <command>                       │
│ • Build: <command>                      │
├─────────────────────────────────────────┤
│ Structure:                              │
│ • Source: <path>                        │
│ • Tests: <path>                         │
│ • Config: <path>                        │
├─────────────────────────────────────────┤
│ Recent Focus: <last few commits>        │
└─────────────────────────────────────────┘
```

## Usage

After priming, I'm ready to:
- Answer questions about the codebase
- Make changes following project conventions
- Run appropriate commands
- Understand the architecture

---

**Now load the project context.**
