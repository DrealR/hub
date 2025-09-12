# Assistant Preferences (Optional)

This repo supports a user‑tunable “assistant” profile that controls tone, structure, planning, and confirmations. It does not break existing behavior if absent.

## Quick Setup

```bash
# Merge preferences into ~/.gemini/settings.json (idempotent)
tools/cdx/scripts/setup-agent-preferences.sh

# Dry run to preview changes
tools/cdx/scripts/setup-agent-preferences.sh --dry-run
```

## What it adds

```json
{
  "assistant": {
    "__profileVersion": "v1",
    "verbosity": "balanced",
    "preambles": true,
    "plan": "auto",
    "progressInterval": "auto",
    "structure": { "headers": true, "bullets": true, "codeMonospace": true },
    "confirmations": "default"
  }
}
```

- `verbosity`: concise | balanced | detailed
- `preambles`: include 1‑sentence “what I’ll do next” before tool calls
- `plan`: auto | always | never (controls plan display for multi‑step tasks)
- `progressInterval`: auto | none | N (every N major steps)
- `structure`: hint UI/text rendering choices
- `confirmations`: default | auto_edit | yolo (maps to CLI approval modes)

## Related
- Prompts: `prompts/agent-operating-manual.md`
- RFC: `docs/rfcs/0002-agent-communication-contract.md`

