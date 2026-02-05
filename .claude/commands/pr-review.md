# Multi-Perspective PR Review

Conduct a comprehensive code review: $ARGUMENTS

---

## Review Protocol

Launch parallel sub-agents for multi-perspective analysis:

### Agent 1: Architecture Review
Focus on:
- [ ] Does this change fit the existing architecture?
- [ ] Are there any design pattern violations?
- [ ] Is the code organized logically?
- [ ] Are dependencies appropriate?
- [ ] Is there unnecessary coupling?

### Agent 2: Security Review
Focus on:
- [ ] Input validation present?
- [ ] SQL injection vulnerabilities?
- [ ] XSS vulnerabilities?
- [ ] Authentication/authorization issues?
- [ ] Secrets or credentials exposed?
- [ ] OWASP Top 10 concerns?

### Agent 3: Performance Review
Focus on:
- [ ] Any O(n²) or worse algorithms?
- [ ] Unnecessary database queries (N+1)?
- [ ] Memory leaks potential?
- [ ] Missing caching opportunities?
- [ ] Large bundle size impacts?

### Agent 4: Quality Review
Focus on:
- [ ] Code readability
- [ ] Naming conventions
- [ ] Comment quality (not too many, not too few)
- [ ] Test coverage
- [ ] Error handling
- [ ] Edge cases covered

## Review Process

### Step 1: Fetch PR Details
```bash
gh pr view $ARGUMENTS --json title,body,files,commits,reviews,comments
gh pr diff $ARGUMENTS
```

### Step 2: Analyze Each File
For each changed file:
1. Understand the purpose of the change
2. Check against each review perspective
3. Note any issues or suggestions

### Step 3: Categorize Findings

**Severity Levels:**
- 🔴 **BLOCKER** - Must fix before merge
- 🟠 **MAJOR** - Should fix, may cause issues
- 🟡 **MINOR** - Nice to fix, code quality
- 🟢 **NIT** - Stylistic suggestion

## Output Format

```
┌─────────────────────────────────────────┐
│           PR REVIEW SUMMARY             │
├─────────────────────────────────────────┤
│ PR: #$ARGUMENTS                         │
│ Title: <pr title>                       │
│ Files: <count> changed                  │
├─────────────────────────────────────────┤
│ ARCHITECTURE: ✓ Approved                │
│ SECURITY: ⚠️ 1 concern                  │
│ PERFORMANCE: ✓ Approved                 │
│ QUALITY: ⚠️ 2 suggestions               │
├─────────────────────────────────────────┤
│ Overall: APPROVED WITH COMMENTS         │
└─────────────────────────────────────────┘

## Detailed Findings

### 🟠 MAJOR: SQL Injection Risk
File: src/api/users.ts:42
```ts
// Current (vulnerable)
const query = `SELECT * FROM users WHERE id = ${userId}`;

// Suggested (safe)
const query = `SELECT * FROM users WHERE id = $1`;
```

### 🟡 MINOR: Consider caching
File: src/services/data.ts:78
This function is called frequently and returns the same data.
Consider adding memoization.
```

---

**Now review PR #$ARGUMENTS or the current branch diff.**
