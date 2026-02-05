---
description: Master orchestrator - chains commands together for complete workflows
argument-hint: <workflow> [args] (start|ship|end|feature|fix|review|deploy|spec)
allowed-tools: Bash(git:*), Read, Glob, Grep, Task, TodoWrite, WebSearch
---

# Flow - Master Command Orchestrator

**Workflow:** $1
**Arguments:** $2

---

## Available Workflows

### 1. `start` - Begin Work Session
```
/project:flow start <session-name>
```
**Chains:** `context-prime` → `session-start`

### 2. `ship` - Complete Ship Workflow
```
/project:flow ship [commit-hint]
```
**Chains:** `check` → `security-scan` → `push`

### 3. `end` - End Work Session
```
/project:flow end
```
**Chains:** `session-end` → `handover`

### 4. `feature` - Full Feature Development
```
/project:flow feature <name>
```
**Chains:** `spec` → `feature-dev` → `check` → `pr-review`

### 5. `fix` - Complete Bug Fix
```
/project:flow fix <issue#>
```
**Chains:** `fix-issue` → `tdd` → `check` → `push`

### 6. `review` - Full Code Review
```
/project:flow review <PR#>
```
**Chains:** `security-scan` → `pr-review`

### 7. `deploy` - Safe Deployment
```
/project:flow deploy <env>
```
**Chains:** `check` → `security-scan` → `deploy-checklist`

### 8. `spec` - Spec-Driven Development (IndyDevDan Method)
```
/project:flow spec <feature-name>
```
**Chains:** `research` → `spec` → `feature-dev`

---

## Workflow Execution Protocol

When you invoke a flow:

1. **Announce** the sub-commands that will run
2. **Execute** each in sequence
3. **Pass context** between commands
4. **Report** status after each step
5. **Stop** on failure (ask to continue or abort)

---

## Cognitive Enhancement (Applied to ALL Flows)

Before executing, verify:

### Pre-Flight Checklist
- [ ] Understand what each sub-command does
- [ ] Identify dependencies between steps
- [ ] Know what success looks like
- [ ] Have rollback plan if needed

### During Execution
- [ ] Track progress with TodoWrite
- [ ] Report status between steps
- [ ] Stop and ask if uncertain

### Post-Execution
- [ ] Verify all steps completed
- [ ] Report final status
- [ ] Suggest next actions

---

## Output Format

```
┌─────────────────────────────────────────┐
│         FLOW: $1                        │
├─────────────────────────────────────────┤
│ Step 1/N: <command>                     │
│ └── Status: ✓ Complete                  │
├─────────────────────────────────────────┤
│ Step 2/N: <command>                     │
│ └── Status: ⏳ In Progress              │
├─────────────────────────────────────────┤
│ FLOW STATUS: Running...                 │
└─────────────────────────────────────────┘
```

---

**Now execute: /project:flow $1 $2**
