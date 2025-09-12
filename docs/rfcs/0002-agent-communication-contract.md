# RFC: Agent–User Communication Contract and Comfort Profile

Status: Proposal
Author: @DrealR
Created: 2025-09-12
Depends on: 0001-autonomous-digital-companion

## Summary
Define a clear interaction model that makes the agent easier to collaborate with across terminal, desktop, and web. Introduce a user‑tunable “Assistant Preferences” profile and reusable prompts that align with modern agent UIs (Claude Code, Warp Agent Mode, Gemini CLI MCP).

## Background (inspiration)
- Claude Code focuses on deep code context and conversational edits inside editors; it recently expanded IDE reach (e.g., Zed) and collaboration patterns. citeturn2search0turn2search3
- Warp’s Agent Mode emphasizes ergonomic CLI collaboration with a prompt palette, natural‑language commands, and tight shell integration. citeturn2search6turn2open7
- Gemini CLI’s MCP support shows how to safely extend agents with browser, GitHub, and SaaS tools using stdio/SSE/HTTP transports and OAuth. citeturn2open2

## Goals
- Faster alignment: consistent preambles, short plans, and explicit confirmations.
- Predictable output: stable structure for scanning in chat, terminal, and UI panes.
- Safer autonomy: confirmations by default; trust is opt‑in and revocable.

## Proposal
1) Preferences schema: allow per‑user “assistant” settings (verbosity, structure, confirmations, progress frequency). Stored in `~/.gemini/settings.json` without breaking existing consumers.
2) Operating prompts: add reusable manuals (planning loop, patch authoring, tool‑choice policy, security guardrails) in `prompts/`.
3) CLI UX: document quick toggles and provide a script to scaffold preferences idempotently (no sudo).

### Assistant Preferences (non‑breaking)
An optional `assistant` object in settings:
```
{
  "assistant": {
    "verbosity": "concise|balanced|detailed",
    "preambles": true,
    "plan": "auto|always|never",
    "progressInterval": "auto|none|N",
    "structure": { "headers": true, "bullets": true, "codeMonospace": true },
    "confirmations": "default|auto_edit|yolo"
  }
}
```
If absent, defaults apply and the CLI behaves as today.

### Output contract (short form)
- Preambles: one sentence before actions.
- Plans: 3–6 steps, single “in progress”.
- Responses: headers optional; bullets 1‑line each; commands and paths monospace.
- Progress: brief updates on long tasks.
- Safety: ask‑then‑act; confirmations on sensitive tools.

## Rollout
- Add prompts and docs; ship a no‑sudo setup script that adds `assistant` to user settings (idempotent).
- Optional future: surface these preferences in the desktop/web UI.

