---
name: dev-workflow
description: Complete development workflow skill with Plan-Spec-Build methodology. Use for feature development, bug fixes, code review, session tracking, quality checks, and deployment. Activates when user mentions building features, fixing bugs, reviewing code, starting sessions, or deploying.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite, WebSearch, WebFetch
---

# Development Workflow Skill

A comprehensive agentic development workflow based on IndyDevDan's methodologies.

## Core Philosophy

**"Four out of five times I recommend Plan → Spec → Build, specifically for mid to large-sized features. Aim big, hand off more work to your agent."** — IndyDevDan

## Cognitive Enhancement Protocol

Before ANY action, apply this 9-step reasoning:

1. **Logical Dependencies** - What must happen first?
2. **Risk Assessment** - What could go wrong?
3. **Abductive Reasoning** - What's the root cause?
4. **Outcome Evaluation** - Learn from previous attempts
5. **Information Gathering** - Know vs assume
6. **Precision** - Be specific
7. **Completeness** - Consider all options
8. **Persistence** - Don't give up early
9. **Inhibition** - Think before acting

## Available Workflows

### 1. Plan → Spec → Build (Recommended)

For features, use this 3-phase approach:

**Phase 1: PLAN (Read-Only)**
- Analyze codebase with `git ls-files`
- Read relevant files
- Identify patterns and constraints
- NO modifications

**Phase 2: SPEC (Write Specification)**
Create `specs/<feature-name>.md`:
```markdown
# Feature: <name>

## Requirements
1. Requirement 1
2. Requirement 2

## Design
- Architecture approach
- Data flow
- Components

## Tasks
- [ ] Task 1
- [ ] Task 2

## Success Criteria
- Criterion 1
- Criterion 2
```

**Phase 3: BUILD (Execute)**
Implement following the spec exactly.

### 2. Quick Fix Workflow

For bugs, use TDD:
1. Write failing test
2. Implement fix
3. Verify test passes
4. Run quality checks

### 3. Session Management

Track work sessions:
- `/project:session-start <name>` - Begin
- `/project:session-end` - End with summary

### 4. Quality Gate

Before shipping:
- Lint check
- Type check
- Test suite
- Build verification

## Slash Commands Reference

See `workflows/` directory for detailed command implementations:

- `architect` - Full analysis + research + planning
- `spec` - Create detailed specification
- `plan` - Lightweight planning mode
- `research` - Deep technical research
- `check` - Quality gate
- `push` - Smart git workflow
- `flow` - Master orchestrator

## Extended Thinking Triggers

For deep analysis, use:
- "think" - Standard
- "think hard" - Deeper
- "think harder" - Extensive
- "ultrathink" - Maximum depth

## Best Practices

1. **Start with Plan Mode** (Shift+Tab x2) for complex tasks
2. **Create specs** for features before building
3. **Use TDD** for bug fixes
4. **Track sessions** for continuity
5. **Run quality checks** before shipping

## Integration

This skill works with:
- Git workflows
- GitHub issues/PRs
- CI/CD pipelines
- Testing frameworks
