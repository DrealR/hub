# Plan → Spec → Build Prompt Template

Use this for mid to large-sized features.

## Phase 1: PLAN

```
I need to build: [FEATURE]

First, let me analyze the codebase without making changes:

1. Check project structure: git ls-files | head -50
2. Read relevant files
3. Understand existing patterns
4. Identify constraints

DO NOT modify any files yet.

Questions to answer:
- What existing code is similar?
- What patterns should I follow?
- What are the dependencies?
- What could break?
```

## Phase 2: SPEC

```
Based on my analysis, here's the specification:

## Feature: [NAME]

### Requirements
1. [Functional requirement 1]
2. [Functional requirement 2]
3. [Non-functional: performance/security/etc]

### Design
- Architecture: [How it fits]
- Data model: [New structures]
- API: [New endpoints]
- Components: [New UI pieces]

### Tasks (in order)
1. [ ] [Task 1] - Files: [files]
2. [ ] [Task 2] - Files: [files]
3. [ ] [Task 3] - Files: [files]

### Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] All tests pass

### Risks
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [How to handle] |

Do you approve this spec? (yes/modify/cancel)
```

## Phase 3: BUILD

```
Spec approved. Now implementing:

Following the spec exactly:
1. [Task 1] - Creating [files]
2. [Task 2] - Implementing [logic]
3. [Task 3] - Adding [tests]

Tracking progress with TodoWrite.

After each task:
- Verify it works
- Check for regressions
- Update progress
```

## Completion Checklist

```
Implementation complete. Verifying:

- [ ] All spec requirements met
- [ ] All tasks completed
- [ ] Tests pass
- [ ] Lint clean
- [ ] Build succeeds
- [ ] No regressions

Ready for: /project:push or /project:pr-review
```
