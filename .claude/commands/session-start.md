# Session Start

Begin a tracked development session: $ARGUMENTS

---

## Composable Command

**This command automatically includes:** `context-prime`

---

## Session Initialization

### Step 1: Prime Context (via context-prime)

First, load project context:
- Read `README.md`, `CLAUDE.md`
- Run `git ls-files` for structure
- Check `package.json` / `Cargo.toml` / `pyproject.toml`
- Review recent commits

### Step 2: Create Session Record

Generate a session file at `.claude/sessions/`:
```
.claude/sessions/YYYY-MM-DD-HHMM-<name>.md
```

### Step 3: Capture Initial State

```bash
git branch --show-current
git status --short
git log --oneline -5
```

### Step 4: Session Document

```markdown
# Session: $ARGUMENTS
**Started:** <timestamp>
**Branch:** <current branch>

## Context Loaded
- Project: <name>
- Stack: <technologies>
- Recent focus: <last commits>

## Goals
- [ ] Goal 1
- [ ] Goal 2

## Progress Log
### <timestamp>
- Session started with context primed

## Changes Made
<updated throughout>

## Decisions Made
<updated throughout>
```

### Step 5: Set Active Session

Create `.claude/.current-session` marker.

---

## Linked Commands

After starting, you can use:
- `/project:session-update [notes]` - Add progress
- `/project:session-end` - End with summary (includes handover)

Or use the flow:
- `/project:flow end` - Complete session wrap-up

---

## Output

```
┌─────────────────────────────────────────┐
│         SESSION STARTED                 │
├─────────────────────────────────────────┤
│ Name: $ARGUMENTS                        │
│ Time: <timestamp>                       │
│ Branch: <branch>                        │
├─────────────────────────────────────────┤
│ CONTEXT LOADED:                         │
│ ├── Project: <name>                     │
│ ├── Stack: <tech>                       │
│ └── Files: <count>                      │
├─────────────────────────────────────────┤
│ Session: .claude/sessions/<file>.md     │
└─────────────────────────────────────────┘
```

---

**Now start session: $ARGUMENTS**
