# Output Styles

Output styles control how the assistant structures its responses: plain text, tables, YAML, ultra‑concise bullets, a short TTS summary, or a generated HTML UI.

## Quick usage

```bash
# List styles
/output-style list

# Set style (user scope by default)
/output-style set yaml

# Set for this workspace only
/output-style set html --scope workspace

# Env override (highest precedence)
export GEMINI_OUTPUT_STYLE=table
```

## Styles
- `default` — standard conversational output.
- `table` — GitHub‑flavored Markdown tables for lists/comparisons.
- `yaml` — YAML‑only responses (no backticks) with common keys when applicable.
- `ultra-concise` — 3–7 short bullets with critical commands first.
- `tts-summary` — end with a brief "TTS:" summary; may call a TTS MCP tool if available.
- `html` — generate a minimal HTML document via `write_file` in `.gemini/tmp/` and return its path.

Notes
- Styles are appended to the system prompt at chat start.
- Workspace settings override user settings; `GEMINI_OUTPUT_STYLE` overrides both.
- HTML style may propose opening the file via shell; this requires confirmation.

