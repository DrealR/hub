# RFC: Transform This Repo into an Autonomous Digital Companion

Status: Proposal
Author: @DrealR
Created: 2025-09-12
Target Release: phased (90 days)

## Summary
Evolve this repository from a CLI‑centric toolkit into a multi‑surface, autonomous digital companion with a delightful UI, first‑class MCP integrations, and safe autonomy. The system should plan, execute, and verify complex tasks across the web and developer tools while preserving user control via confirmations, sandboxing, and clear audit trails.

## Motivation
- Showcase the project’s agentic capabilities beyond the terminal.
- Unlock high‑value automations (browser tasks, GitHub maintainer flows, docs/PM, calendar, mail).
- Provide a UI that is friendly for non‑terminal users while keeping the CLI powerful for advanced workflows.

## Goals
- Add a curated "MCP Pack" (browser, GitHub, docs/PM, workspace, messaging).
- Ship Desktop and Web UIs that visualize plans, tool calls, and results.
- Introduce a small orchestrator (planner → critic → executor) with resumable tasks.
- Persist memory and long‑running jobs; enable voice and realtime interactions.

## Non‑Goals
- Building a closed ecosystem. We prefer open MCP servers and pluggable transports.
- Removing the terminal UX. The CLI remains a first‑class interface.

## Architecture Overview
- Core remains TypeScript/ESM. Add packages and a small event bus abstraction for UI surfaces.
- New packages:
  - `packages/agent-graph/` – planning/execution graph; plan steps, tool batching, verifiers.
  - `packages/app-desktop/` – Tauri shell (IPC/WebSocket to core/a2a server).
  - `packages/web/` – Next.js web UI; connects to `packages/a2a-server`.
  - `packages/memory-store/` – embeddings + recall (file store by default; vector DB pluggable).
  - `servers/*` – thin wrappers for selected MCP servers when local hosting is needed.
- Existing `packages/a2a-server` exposes Express endpoints for tasks and streaming; we extend it with:
  - WebSocket bridge for UI streams.
  - OAuth helper endpoints for HTTP/SSE MCP servers.

## MCP Pack (initial)
- Playwright Browser MCP (element‑aware navigation; screenshots; safe‑confirm).
- GitHub MCP (issues/PRs/triage/reviews; read‑only by default).
- Notion MCP (docs/project briefs; OAuth flow).
- Google Workspace MCP (Gmail/Calendar triage and scheduling).
- Slack MCP (status and notifications for runs).

All new servers default to `trust: false`; every sensitive action requires confirmation. Snapshots (DOM/screenshot/diff) appear in UI before approve/deny.

## Autonomy Engine
- Planner produces a task graph; Critic verifies steps (heuristics + self‑checks); Executor calls tools with batching and retry.
- Temporal (optional) for long‑running workflows with Signals (pause, escalate) and Queries (status).

## UI Concepts
- Timeline: streaming model tokens, tool requests, approvals, and outputs.
- Inspector: view tool schemas, params, and responses; re‑run with edits.
- Voice mode: push‑to‑talk; TTS playback; mic consent gate.

## Security & Privacy
- Default sandbox profile: restrictive; opt‑in to escalate per task.
- Policy engine: per‑server and per‑tool allow/deny lists; UI to manage trust.
- Secrets: never stored in repo; use OS keychain or env providers.

## Rollout Plan (90 days)
1. Weeks 1–3: MCP pack integration; unified OAuth; improved CLI confirmations.
2. Weeks 4–6: Desktop/Web shells; timeline/inspector; voice prototype.
3. Weeks 7–9: Orchestrator + Temporal; two showcase experiences (Concierge Browser, Maintainer Mode).
4. Weeks 10–12: Memory store; polish; docs and self‑host recipes; stable release.

## Open Questions
- Which vector store to default to for local memory? (file‑based first, pluggable second)
- Which actions warrant server‑side policy vs. per‑task user approvals?
- What is the minimum viable offline experience for the desktop app?

