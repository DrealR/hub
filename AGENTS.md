# Repository Guidelines

## Project Structure & Module Organization
- Monorepo managed by npm workspaces (Node ≥ 20; see `.nvmrc`).
- `packages/` – core packages: `cli/` (CLI), `a2a-server/`, `vscode-ide-companion/`, `test-utils/`.
- `integration-tests/` – end‑to‑end tests (Vitest).
- `scripts/` – build/test/dev utilities (Node).
- `docs/` – user and architecture docs.
- `third_party/` – vendored helpers (e.g., ripgrep fetcher).
- `.github/` – CI/release workflows and PR templates.

## Build, Test, and Development Commands
- Install deps: `npm install` (root installs workspaces).
- Build: `npm run build` (compile/bundle); all targets: `npm run build:all`.
- Start CLI (dev): `npm start`; debug: `npm run debug`.
- Make targets: `make build | test | lint | format | preflight | start | debug`.
- Preflight (CI parity): `npm run preflight` (format, lint, build, typecheck, tests).
- Tests (unit/workspaces): `npm test`; integration: `npm run test:e2e`.
- Lint/format: `npm run lint`, `npm run format`; typecheck: `npm run typecheck`.

## Coding Style & Naming Conventions
- Language: TypeScript (ESM). Keep modules small and focused; avoid circular deps.
- Formatting: Prettier; Linting: ESLint. CI requires zero warnings (`lint:ci`).
- Prettier rules: 2‑space indent, `printWidth=80`, `singleQuote=true`, `semi=true`, `trailingComma=all`.
- Prefer explicit exports and predictable file names; keep public APIs stable.

## Testing Guidelines
- Framework: Vitest. Unit tests colocated; E2E under `integration-tests/**/*.test.ts`.
- Script tests with coverage under `scripts/tests/` (`vitest` + V8 coverage).
- Fast checks: `npm run test`, `npm run test:ci`. Deterministic E2E: `npm run test:integration:sandbox:none`.

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:` (≤ 72‑char subject).
- Link an issue, keep PRs small/focused, include usage notes and screenshots when UI output changes.
- Ensure `npm run preflight` passes and update docs in `docs/` when flags or behavior change.

## Security & Configuration Tips
- Never commit secrets; use local env files and CI secrets. Review `.gitignore`.
- Prefer sandboxed runs (`GEMINI_SANDBOX=true`) during development and tests.

## Agent‑Specific Instructions
- Make minimal, reversible patches; preserve ESM and package boundaries.
- Avoid file renames or public API changes without prior discussion.
- When changing code, add/update tests and run `preflight` before finishing.



FAST-TOOLS PROMPT v1

Use these fast, portable CLI tools to explore and modify this repo efficiently. Prefer them over slower defaults; fall back only when missing. Never use sudo. Default to read-only operations unless explicitly asked to modify files.

Preferred tools
- ripgrep (rg): fast code search. Example: `rg -n --hidden --no-ignore -g '!**/.git/**' "pattern"`.
- fd/fdfind (fd): fast file finder. Examples: `fd -HI "name_part"`, `fd -t f -e sh bin`.
- jq: JSON processing. Examples: `jq -r '.active_profile' config.json`, `jq '.profiles | keys' config.json`.

Fallbacks
- If rg missing: `grep -RIn --exclude-dir .git "pattern" .`.
- If fd missing: `find . -type f -name '*name_part*'` (Debian/Ubuntu may use `fdfind`; run `alias fd=fdfind`).
- If jq missing: use minimal `sed/awk` only for simple extraction; avoid parsing complex JSON.

Usage guidance
- Limit output: pipe to `sed -n '1,200p'`, `head -n 200`, or add `--max-columns`/`--line-number` flags.
- Keep changes surgical. When editing files, describe intent first; then apply minimal patches.
- Quote variables safely, prefer `set -euo pipefail` in scripts, and check commands with `command -v`.
- Avoid destructive operations (`rm -rf`, `git reset --hard`). If required, request explicit confirmation or provide a safe alternative.

Install notes (manual)
- macOS (Homebrew): `brew install ripgrep fd jq`
- Debian/Ubuntu: `sudo apt-get install ripgrep fd-find jq` (then `alias fd=fdfind`)
- Fedora: `sudo dnf install ripgrep fd-find jq`
- Arch: `sudo pacman -S ripgrep fd jq`

Workflow examples
- List tracked files quickly: `rg --files --hidden --no-ignore -g '!**/.git/**'`
- Search a module and print 200 lines: `rg -n "def main\(" src | sed -n '1,200p'`
- Inspect JSON and export env: `export OPENAI_BASE_URL="$(jq -r .api_base config.json)"`

