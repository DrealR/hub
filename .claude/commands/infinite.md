---
description: Parallel agent orchestration for iterative generation (IndyDevDan pattern)
argument-hint: <spec-file> <output-dir> <count|infinite>
allowed-tools: Read, Write, Glob, Task, TodoWrite
---

# Infinite Agentic Loop

**Spec:** $1
**Output:** $2
**Count:** $3

---

## IndyDevDan's Parallel Agent Pattern

Orchestrate multiple AI agents in parallel waves to generate unique iterations.

---

## Step 1: Parse Arguments

- **Spec file:** $1 (e.g., `specs/component.md`)
- **Output dir:** $2 (e.g., `src/components`)
- **Count:** $3
  - `1` = Single focused iteration
  - `5` = 5 parallel agents
  - `20` = 4 waves of 5 agents
  - `infinite` = Continuous until context limit

---

## Step 2: Read Specification

!cat $1 2>/dev/null || echo "Spec file not found: $1"

Extract from spec:
- Generation requirements
- Naming conventions (e.g., `component_v<N>.tsx`)
- Quality criteria
- Design dimensions to vary

---

## Step 3: Directory Reconnaissance

!ls -la $2 2>/dev/null | head -20

Understand:
- What iterations already exist
- Naming patterns used
- What gaps remain

---

## Step 4: Agent Deployment

### For count = 1:
Single agent with full attention to spec.

### For count = 5:
Launch 5 parallel sub-agents via Task tool:
```
Agent 1: Focus on [dimension A]
Agent 2: Focus on [dimension B]
Agent 3: Focus on [dimension C]
Agent 4: Focus on [dimension D]
Agent 5: Focus on [dimension E]
```

### For count = 20:
Execute in waves:
```
Wave 1: Agents 1-5 (foundation)
Wave 2: Agents 6-10 (expansion)
Wave 3: Agents 11-15 (variation)
Wave 4: Agents 16-20 (refinement)
```

### For count = infinite:
```
Wave N: Generate 5 iterations
Check context usage
If context < 80%: Continue to Wave N+1
Else: Stop and summarize
```

---

## Step 5: Sub-Agent Instructions

Each agent receives:
```markdown
## Assignment: Iteration $N

### Context
- Spec: [summary from $1]
- Existing: [list of existing iterations]
- Your unique direction: [specific variation]

### Requirements
1. Follow spec exactly
2. Be unique from other iterations
3. Meet quality criteria

### Output
- File: $2/<naming-pattern>
- Format: [from spec]
```

---

## Step 6: Quality Assurance

After each wave:
- [ ] All files created
- [ ] Spec compliance verified
- [ ] Uniqueness confirmed
- [ ] No errors

---

## Output Format

```
┌─────────────────────────────────────────┐
│         INFINITE AGENTIC LOOP           │
├─────────────────────────────────────────┤
│ Spec: $1                                │
│ Output: $2                              │
│ Mode: $3 iterations                     │
├─────────────────────────────────────────┤
│ Wave 1/N                                │
│ ├── Agent 1: ✓ Complete                 │
│ ├── Agent 2: ✓ Complete                 │
│ ├── Agent 3: ⏳ In Progress             │
│ ├── Agent 4: ⏳ Pending                 │
│ └── Agent 5: ⏳ Pending                 │
├─────────────────────────────────────────┤
│ Generated: 2/$3                         │
└─────────────────────────────────────────┘
```

---

## Example Spec File

Create in `specs/`:
```markdown
# Component Generator Spec

## Requirements
Generate unique React components

## Naming
component_v{N}.tsx

## Quality Criteria
- TypeScript strict
- Responsive
- Accessible (WCAG 2.1 AA)

## Dimensions to Vary
- Color scheme
- Layout pattern
- Animation style
- Typography
```

---

**Now execute infinite loop: $1 $2 $3**
