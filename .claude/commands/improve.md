---
description: Self-improving system analysis - test, measure, optimize
argument-hint: [focus] [--iterations N] [--sims N]
allowed-tools: Bash(*), Read, Glob, Grep, Task, Write, Edit
---

# Self-Improving System

**Focus:** $ARGUMENTS

---

## Phase 0: Detect System Type

First, identify what we're improving:

```bash
# Check for project markers
ls -la package.json pyproject.toml Cargo.toml go.mod 2>/dev/null | head -3
```

Determine:
- Project type (Node.js, Python, Rust, Go, etc.)
- Test framework available
- Build system
- Any simulation/benchmark capability

---

## Phase 1: PRE-ARCHITECT - Analyze Current State

### 1.1 Codebase Survey
```bash
# Get structure
find . -type f -name "*.py" -o -name "*.ts" -o -name "*.rs" | head -20
git log --oneline -10
```

### 1.2 Identify Improvement Targets

Based on the focus "$ARGUMENTS", identify:
- [ ] What metrics can we measure?
- [ ] What configurations can we tune?
- [ ] What alternatives can we test?

### 1.3 Define Success Criteria

For each metric, set targets:

| Metric | Current | Target | Weight |
|--------|---------|--------|--------|
| [Metric 1] | ? | ? | 30% |
| [Metric 2] | ? | ? | 30% |
| [Metric 3] | ? | ? | 40% |

---

## Phase 2: EXECUTE - Run Tests

### 2.1 Baseline Measurement
```bash
# Run current tests/benchmarks
npm test || pytest || cargo test || go test ./...
```

### 2.2 Configuration Tests

For each configuration variant:
1. Apply configuration
2. Run measurement
3. Record results

### 2.3 Parallel Execution

Use Task tool to run multiple configurations in parallel:
- Config A: [variant 1]
- Config B: [variant 2]
- Config C: [variant 3]

---

## Phase 3: POST-ARCHITECT - Analyze & Improve

### 3.1 Score Each Configuration

Calculate weighted score for each config:
```
score = (metric1 * 0.3) + (metric2 * 0.3) + (metric3 * 0.4)
```

### 3.2 Ranking Table

| Rank | Config | Score | Metric 1 | Metric 2 | Metric 3 |
|------|--------|-------|----------|----------|----------|
| 1 | [best] | X.X | ... | ... | ... |
| 2 | [2nd] | X.X | ... | ... | ... |
| 3 | [3rd] | X.X | ... | ... | ... |

### 3.3 Improvement Recommendations

Based on results:
1. **What worked:** [observations]
2. **What didn't:** [observations]
3. **Next iteration:** [proposed changes]

---

## Phase 4: APPLY - Implement Changes

### 4.1 Apply Best Configuration

If improvements found:
```bash
# Apply the winning configuration
# [specific commands based on project type]
```

### 4.2 Verify Improvement

Re-run tests to confirm:
```bash
# Verify improvement stuck
npm test || pytest || cargo test
```

### 4.3 Document Changes

Update any relevant documentation:
- Configuration files
- README notes
- Changelog entry

---

## Phase 5: LOOP - Continue or Exit

### Decision Point

```
┌─────────────────────────────────────────┐
│         IMPROVEMENT ITERATION           │
├─────────────────────────────────────────┤
│ Iteration:     N of M                   │
│ Targets Met:   X / Y                    │
│ Best Score:    XX.X / 100               │
├─────────────────────────────────────────┤
│ CONTINUE?                               │
│ ✓ Targets not yet met                   │
│ ✓ Iterations remaining                  │
│ ✓ Improvement still possible            │
└─────────────────────────────────────────┘
```

If targets not met AND iterations remaining:
- Generate new hypotheses
- Return to Phase 2

---

## Output Format

```
┌─────────────────────────────────────────┐
│         IMPROVEMENT COMPLETE            │
├─────────────┬───────────────────────────┤
│ Iterations  │ N                         │
│ Best Config │ [name]                    │
│ Final Score │ XX.X / 100                │
├─────────────┴───────────────────────────┤
│ CHANGES APPLIED:                        │
│ • [change 1]                            │
│ • [change 2]                            │
├─────────────────────────────────────────┤
│ RECOMMENDATIONS:                        │
│ • [next step 1]                         │
│ • [next step 2]                         │
└─────────────────────────────────────────┘
```

---

## Framework-Specific Notes

### Python Projects
- Use pytest for testing
- Check pyproject.toml for config options
- Consider: mypy settings, test coverage, performance

### Node.js Projects
- Use npm/yarn/pnpm test
- Check package.json scripts
- Consider: bundle size, test coverage, build time

### Rust Projects
- Use cargo test/bench
- Check Cargo.toml for features
- Consider: compile time, binary size, performance

### Simulation/Game Projects
- Run simulation batches
- Measure: diversity, realism, balance
- Consider: model configurations, parameters

---

**Now analyze and improve: $ARGUMENTS**
