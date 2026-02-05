---
description: Lightweight planning mode - analyze before implementing
argument-hint: <task to plan>
allowed-tools: Read, Glob, Grep, Task, TodoWrite
model: sonnet
---

# Planning Mode

**Task:** $ARGUMENTS

---

## Plan Mode Protocol (IndyDevDan Method)

This is a **read-only analysis phase**. NO code changes until plan is approved.

### What Plan Mode Does:
- Analyzes codebase structure
- Identifies files to modify
- Understands existing patterns
- Creates implementation roadmap
- **Does NOT modify files**

---

## Phase 1: Problem Analysis

### 1.1 Understand the Request
- What exactly is being asked?
- What is the expected outcome?
- What are the success criteria?

### 1.2 Gather Context
!git ls-files | head -30

Read relevant files to understand:
- Current architecture
- Existing patterns
- Dependencies

### 1.3 Identify Constraints
- Technical limitations
- Time/scope constraints
- Breaking change risks

---

## Phase 2: Investigation

### 2.1 Search Codebase
Find related code:
- Similar implementations
- Affected components
- Test coverage

### 2.2 Form Hypotheses
List possible approaches:
1. Approach A: ...
2. Approach B: ...
3. Approach C: ...

### 2.3 Evaluate Trade-offs
| Approach | Pros | Cons | Effort |
|----------|------|------|--------|
| A | ... | ... | Low/Med/High |
| B | ... | ... | Low/Med/High |

---

## Phase 3: Solution Design

### 3.1 Chosen Approach
**Selected:** [Approach X]
**Reasoning:** Why this is best

### 3.2 Task Breakdown
```
$ARGUMENTS
├── Task 1: ...
│   └── Files: ...
├── Task 2: ...
│   └── Files: ...
└── Task 3: ...
    └── Files: ...
```

### 3.3 Validation Strategy
- How will success be measured?
- What tests are needed?
- What verification steps?

---

## Phase 4: Approval Checkpoint

**Before implementing, present this plan and ask:**

> "Here's my plan for: $ARGUMENTS
>
> [Summary of approach]
>
> Tasks:
> 1. ...
> 2. ...
>
> Ready to proceed? (yes/modify/cancel)"

---

## Output Format

```
┌─────────────────────────────────────────┐
│         PLAN: $ARGUMENTS                │
├─────────────────────────────────────────┤
│ Approach: [chosen approach]             │
│ Tasks: N                                │
│ Files to modify: N                      │
│ Estimated complexity: Low/Med/High      │
├─────────────────────────────────────────┤
│ Status: Awaiting Approval               │
└─────────────────────────────────────────┘
```

---

**Now plan: $ARGUMENTS**
