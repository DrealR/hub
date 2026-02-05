---
description: Run ALL quality checks in parallel (lint, types, tests, build)
argument-hint: [directory] [--skip-tests]
allowed-tools: Bash(*), Read, Glob, Task
---

# Quality Gate Check

**Target:** $ARGUMENTS

---

## Pre-Check: Detect Project Type

!ls package.json Cargo.toml go.mod pyproject.toml requirements.txt 2>/dev/null | head -5

Identify:
- Package manager (npm/yarn/pnpm/cargo/go/pip)
- Available scripts
- Test framework

---

## Parallel Quality Checks

Execute ALL checks simultaneously using Task tool:

### 1. Lint Check
```bash
# Node.js
npm run lint || npx eslint . || npx biome check .

# Python
ruff check . || pylint **/*.py

# Rust
cargo clippy

# Go
golangci-lint run
```

### 2. Type Check
```bash
# TypeScript
npx tsc --noEmit

# Python
mypy . || pyright

# Rust
cargo check
```

### 3. Test Suite
```bash
# Node.js
npm test || npx jest || npx vitest

# Python
pytest

# Rust
cargo test

# Go
go test ./...
```

### 4. Build Verification
```bash
# Node.js
npm run build

# Rust
cargo build --release

# Go
go build ./...
```

---

## Skip Options

If `$ARGUMENTS` contains `--skip-tests`:
- Skip test suite (for faster feedback)
- Still run lint, types, build

---

## Output Format

```
┌─────────────────────────────────────────┐
│           QUALITY GATE RESULTS          │
├─────────────┬───────────┬───────────────┤
│ Check       │ Status    │ Details       │
├─────────────┼───────────┼───────────────┤
│ Lint        │ ✓ PASS    │ 0 issues      │
│ Types       │ ✓ PASS    │ 0 errors      │
│ Tests       │ ✓ PASS    │ 42/42 passing │
│ Build       │ ✓ PASS    │ 3.2s          │
└─────────────┴───────────┴───────────────┘

Overall: ✓ ALL CHECKS PASSED
```

---

## On Failure

If ANY check fails:
1. Show specific error messages
2. Identify root cause
3. Suggest fixes
4. Ask: "Should I auto-fix these issues?"

---

**Now run quality checks on: $ARGUMENTS**
