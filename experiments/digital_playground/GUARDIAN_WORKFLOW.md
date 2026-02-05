# Guardian Build Framework

An opinionated OpenCode setup that pairs constructive and adversarial agents to harden any project through iterative build → challenge → refine loops. This is the "Architect / Oracle / Anomaly" system you described, implemented with Plan, Build, Guardian, Vision, and Ops agents.

## Agent Lineup & Default Models

| Agent | Role | Default Model | Notes |
| --- | --- | --- | --- |
| `plan` | Architect strategist & coordinator | `moonshotai/kimi-k2-thinking` | Deep reasoning for roadmap design and loop management. |
| `build` | Implementation engineer | `openrouter/polaris-alpha` | Fast, accurate code generation & tooling. |
| `guardian` | Oracle/Adversary hybrid | `openrouter/gpt-5-codex` | Raises anomalies, orchestrates red-team loops. |
| `ops` | Configuration & credential steward | `openrouter/gpt-4o-mini` | Keeps models, credentials, and environment tidy. |
| `vision` | Multimodal assistant | `openrouter/gpt-5-codex` | High-fidelity UI / diagram analysis. |

All mappings live in `.opencode/models.json` so the agents can be reassigned without touching the prompts.

## Quick Start

```bash
# Launch the Architect-first workflow
./opencode-dual-agent.sh
```

This script now:
1. Reads `.opencode/models.json` and stamps the chosen model onto every agent file.
2. Loads credentials from `.opencode-credentials.json` (if present) and exports them for OpenCode.
3. Starts OpenCode in Plan mode with the full agent carousel available via `TAB` (Plan → Build → Guardian → Ops).
4. Ensures the `guardian_system/ops.sh` helper is available for quick model or credential tweaks.

## Managing Models & Credentials via Ops

Use the Guardian Ops helper (`guardian_system/ops.sh`) instead of touching config files directly:

```bash
# Inspect the catalog by agent role
./guardian_system/ops.sh models list

# Show the current assignments
./guardian_system/ops.sh models show

# Switch the build agent to GPT-4o and guardian to GPT-5 Codex
./guardian_system/ops.sh models set build openai/gpt-4o guardian openrouter/gpt-5-codex

# Sync credentials (export keys first in your shell, then run)
export OPENROUTER_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-..."
./guardian_system/ops.sh credentials sync

# Check which providers have keys without printing the secrets
./guardian_system/ops.sh credentials status
```

Give the Ops agent commands like:
```
@ops switch the build agent to openai/gpt-4o and guardian to moonshotai/kimi-k2-thinking
```
It will call through the helper, confirm success, and log the update without exposing secrets.

## Workflow Loop

1. **Plan (Architect)**
   - Capture the mission, split work into Architect ⇄ Adversary loops, and declare expected failure checkpoints.
   - Auto-invoke `@vision` whenever imagery arrives; attach the summary.
   - Delegate building via `@build` and adversarial probes via `@guardian`.

2. **Build (Implementation)**
   - Run tests red → implement → green, logging each checkpoint.
   - Collaborate with Guardian when anomalies persist; request Ops help for environment fixes.

3. **Guardian (Oracle/Adversary)**
   - Detect anomalies, flip the system state to UNSTABLE, and spawn remediation loops.
   - Mentor anomalies without revealing the full plan; mark them resolved only when assimilated.

4. **Ops (Steward)**
   - Handles model swaps, credential sync, bootstrap tasks, and environment audits.
   - Dispatch when onboarding a new repo, rotating keys, or realigning agent models.

## Reusing in Other Projects

1. Run the bootstrap helper:
   ```bash
   guardian_system/bootstrap.sh /path/to/target/repo
   ```
   Use `--force` to overwrite existing files.
2. Inside the target repo run:
   ```bash
   cd /path/to/target/repo
   ./opencode-dual-agent.sh
   ```
   The launch script re-stamps agent prompts and model settings.
3. Use `./guardian_system/ops.sh` to inspect or change models and manage credentials.

If you prefer manual copying, mirror `.opencode`, `opencode.json`, `.opencode-workflow.json`, `opencode-dual-agent.sh`, and `GUARDIAN_WORKFLOW.md` into the new repo.

## Recommended Usage Order

1. Start in **Plan** to gather requirements and design the loop.
2. Kick off implementation with **Build** (or delegate via `@build`).
3. Let **Guardian** stress the changes; every detected anomaly becomes the checkpoint for progress.
4. When configuration needs change (models, keys, bootstrap), switch to **Ops**.
5. Use **Vision** whenever UI/diagram context appears.

## Best Practices

- Treat anomalies as allies. Only merge features once Guardian confirms STABLE state.
- Keep credentials out of the repository—export them per shell and run the Ops sync script.
- Snapshot goals at the top of each loop so the system always knows the destination.
- When running on an existing (potentially unstable) codebase, start with Guardian to catalogue current anomalies before adding new features.

Use this document as the canonical reference when porting the Guardian Framework to new workspaces.
