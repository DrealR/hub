---
description: Create a detailed specification for a feature (Plan → Spec → Build)
argument-hint: <feature-name> "<description>"
allowed-tools: Read, Glob, Grep, Task, TodoWrite
model: sonnet
---

# Spec-Driven Development

**Feature:** $1
**Description:** $2

---

## IndyDevDan's Plan → Spec → Build Workflow

This command creates a specification document that will guide implementation.

### Phase 1: REQUIREMENTS GATHERING

First, analyze the codebase to understand context:

!git ls-files | head -30

**Questions to answer:**
1. What problem does this solve?
2. Who is the user?
3. What are the acceptance criteria?
4. What constraints exist?

### Phase 2: WRITE SPECIFICATION

Create: `specs/$1.md`

```markdown
# Feature Specification: $1

## Overview
$2

## Requirements

### Functional Requirements
1. FR-1: [Description]
2. FR-2: [Description]
3. FR-3: [Description]

### Non-Functional Requirements
1. NFR-1: Performance - [criteria]
2. NFR-2: Security - [criteria]
3. NFR-3: Accessibility - [criteria]

## Design

### Architecture
[Describe how this fits into the existing architecture]

### Data Model
[Any new data structures or schema changes]

### API Design
[New endpoints or interface changes]

### Component Structure
```
$1/
├── index.ts
├── types.ts
├── components/
└── utils/
```

## Implementation Tasks

### Backend
- [ ] Task 1
- [ ] Task 2

### Frontend
- [ ] Task 3
- [ ] Task 4

### Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests

## Success Criteria

- [ ] Criterion 1 is met
- [ ] Criterion 2 is met
- [ ] All tests pass
- [ ] No performance regression

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | Low/Med/High | Low/Med/High | How to handle |

## Timeline

Phase 1: [Tasks] - Est. X hours
Phase 2: [Tasks] - Est. Y hours
Phase 3: [Tasks] - Est. Z hours
```

### Phase 3: APPROVAL CHECKPOINT

**Before proceeding to implementation:**

Present the spec and ask:
> "Here is the specification for $1. Review it and let me know if you want to:
> 1. Approve and begin implementation
> 2. Modify the spec
> 3. Add more requirements
> 4. Cancel"

### Phase 4: GENERATE TASK COMMANDS

After approval, create individual task commands:

```
.claude/commands/tasks/$1-task-1.md
.claude/commands/tasks/$1-task-2.md
...
```

Each task command references the spec and implements one piece.

---

## Usage Examples

```bash
# Create spec for user authentication
/project:spec auth "Add OAuth2 login with Google and GitHub"

# Create spec for new feature
/project:spec export-csv "Export user data to CSV format"

# Create spec for refactor
/project:spec refactor-api "Migrate REST endpoints to GraphQL"
```

---

**Now create specification for: $1 - $2**

If $2 is empty, ask the user to describe the feature.
