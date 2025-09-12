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

