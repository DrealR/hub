# Style Workflows

Workflows let you compose several output‑style steps (e.g., YAML → HTML → TTS) into one guided prompt. They’re simple JSON files discovered in:

- User: `~/.gemini/styles/*.json`
- Workspace: `.gemini/styles/*.json`

## Example

```json
{
  "name": "genui_report",
  "description": "Research + YAML + HTML UI + TTS",
  "steps": [
    { "style": "yaml", "goal": "Research the topic; output YAML: facts, sources, risks." },
    { "style": "html", "goal": "Turn YAML into a readable HTML guide; write under .gemini/tmp/report.html." },
    { "style": "tts-summary", "goal": "End with a one-sentence TTS summary." }
  ]
}
```

## Commands

- `/workflow list` — show available workflows
- `/workflow run <name> [topic...]` — builds a composite prompt and submits it

Notes
- The assistant still has access to tools. Sensitive actions require confirmation.
- The HTML step writes a single self‑contained file under `.gemini/tmp/` and returns its path.
- TTS step ends with a `TTS:` line; if a TTS MCP tool is configured, the assistant may call it.

