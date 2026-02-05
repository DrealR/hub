# Session Handover

Prepare comprehensive handover documentation: $ARGUMENTS

---

## Handover Document Generation

Create a complete handover document for continuity between sessions or developers.

### Step 1: Gather Context

```bash
# Current state
git status
git branch --show-current
git log --oneline -10

# Any stashed work
git stash list

# Recent activity
git log --since="24 hours ago" --oneline
```

### Step 2: Document Structure

Generate `HANDOVER.md` or append to session:

```markdown
# Handover: $ARGUMENTS
**Date:** <timestamp>
**Author:** Claude Code Session
**Branch:** <current branch>

## Current State

### What's Working
- Feature/component 1: Status
- Feature/component 2: Status

### What's In Progress
- Task 1: X% complete
  - Done: ...
  - Remaining: ...
- Task 2: X% complete

### What's Blocked
- Issue 1: Blocked by X
- Issue 2: Waiting on Y

## Recent Changes

### Commits (last 24h)
<list of commits>

### Files Modified
<list of key files changed>

## Architecture Notes

### Key Decisions Made
1. Decision 1: Rationale
2. Decision 2: Rationale

### Technical Debt Introduced
1. Item 1: Priority/Plan
2. Item 2: Priority/Plan

## Next Steps

### Immediate (should do first)
1. [ ] Task 1
2. [ ] Task 2

### Short-term (this sprint)
1. [ ] Task 3
2. [ ] Task 4

### Future Considerations
1. Consideration 1
2. Consideration 2

## Environment Setup

### Prerequisites
- Requirement 1
- Requirement 2

### Commands to Run
```bash
# Get up to speed
git pull
npm install  # or equivalent
npm run dev  # or equivalent
```

## Known Issues

### Current Bugs
1. Bug 1: Description, workaround
2. Bug 2: Description, workaround

### Flaky Tests
1. Test 1: Sometimes fails because...

## Contacts & Resources

### Key Files to Review
- `file1.ts` - Main logic for X
- `file2.ts` - Important for Y

### Related Documentation
- Link 1
- Link 2
```

### Step 3: Verify Completeness

Checklist:
- [ ] All in-progress work documented
- [ ] Blockers clearly stated
- [ ] Next steps actionable
- [ ] No tribal knowledge lost

## Output

```
┌─────────────────────────────────────────┐
│         HANDOVER PREPARED               │
├─────────────────────────────────────────┤
│ Document: HANDOVER.md                   │
│ Branch: <branch>                        │
│ Date: <timestamp>                       │
├─────────────────────────────────────────┤
│ Sections:                               │
│ ✓ Current State                         │
│ ✓ Recent Changes                        │
│ ✓ Architecture Notes                    │
│ ✓ Next Steps                            │
│ ✓ Known Issues                          │
├─────────────────────────────────────────┤
│ Ready for handoff!                      │
└─────────────────────────────────────────┘
```

---

**Now prepare handover documentation for: $ARGUMENTS**
