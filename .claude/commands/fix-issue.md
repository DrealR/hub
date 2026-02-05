---
description: Fetch and fix a GitHub issue with TDD approach
argument-hint: <issue-number>
allowed-tools: Bash(gh:*), Bash(git:*), Read, Write, Edit, Glob, Grep, Task, TodoWrite
---

# Fix GitHub Issue #$1

---

## Composable Command

**Automatically includes:** `tdd` + `check`

---

## Pre-Execution Reasoning

### 1) Information Gathering
First, fetch complete issue context:

!gh issue view $1 --json title,body,labels,comments,assignees 2>/dev/null || echo "Issue not found or gh not configured"

### 2) Analysis Checklist
- [ ] What exactly is the bug/request?
- [ ] What is expected vs actual behavior?
- [ ] Are there reproduction steps?
- [ ] What's the priority/severity?

### 3) Risk Assessment
- What could break if we change this?
- Are there related areas affected?
- Is there test coverage?

---

## Implementation Protocol

### Step 1: Create Branch
```bash
git checkout -b fix/issue-$1
```

### Step 2: Reproduce (if bug)
- Write a failing test that demonstrates the issue
- Confirm the test fails as expected

### Step 3: TDD Implementation (via tdd)
1. **RED** - Failing test exists
2. **GREEN** - Minimum code to pass
3. **REFACTOR** - Clean up

### Step 4: Quality Gate (via check)
- [ ] All tests pass
- [ ] Lint clean
- [ ] Build succeeds

### Step 5: Prepare Commit
```
fix: <description from issue>

Fixes #$1

<technical explanation>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Output Format

```
┌─────────────────────────────────────────┐
│         ISSUE FIX: #$1                  │
├─────────────────────────────────────────┤
│ Title: <from GitHub>                    │
│ Type: Bug/Feature/Docs                  │
│ Labels: <labels>                        │
├─────────────────────────────────────────┤
│ Analysis: ✓ Complete                    │
│ Branch: fix/issue-$1                    │
│ TDD: ✓ Test written + passing           │
│ Quality: ✓ All checks pass              │
├─────────────────────────────────────────┤
│ Status: Ready for /project:push         │
└─────────────────────────────────────────┘
```

---

**Now fix issue #$1**
