# Smart Git Push

Intelligently commit and push changes: $ARGUMENTS

---

## Composable Command

**This command automatically includes:** `check` (quality gate)

---

## Push Workflow

### Step 1: Quality Gate (via check)

Before any commit, run all checks:
- [ ] Lint passes
- [ ] Type check passes
- [ ] Tests pass
- [ ] Build succeeds

**If checks fail:** Stop and report issues. Ask to fix or override.

### Step 2: Analyze Changes

```bash
git status
git diff --stat
git diff HEAD
```

Determine:
- One logical change or multiple?
- Split into multiple commits?
- What commit style does this repo use?

### Step 3: Check Recent Commit Style

```bash
git log --oneline -10
```

Match the existing style:
- Conventional commits? (`feat:`, `fix:`, etc.)
- Emoji prefixes?
- Issue references?

### Step 4: Security Check (quick)

Verify no secrets staged:
- [ ] No `.env` files
- [ ] No API keys in code
- [ ] No credentials or tokens

### Step 5: Generate Commit Message

```
<type>(<scope>): <short description>

<body explaining WHY>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Step 6: Commit & Push

```bash
git add <files>
git commit -m "<message>"
git push
```

### Step 7: Monitor CI

After push:
- Check if CI/CD triggers
- Report initial status
- Note any immediate failures

---

## Safety Rules

**NEVER:**
- Force push to main/master
- Commit secrets
- Skip hooks without permission
- Amend pushed commits

**ALWAYS:**
- Review diff first
- Run checks before commit
- Use meaningful messages

---

## Linked Commands

This command uses:
- `check` - Quality gate (automatic)

Works well after:
- `/project:fix-issue` - Push the fix
- `/project:feature-dev` - Ship the feature
- `/project:tdd` - Push tested code

Or use the flow:
- `/project:flow ship` - Full ship workflow with security scan

---

## Output

```
┌─────────────────────────────────────────┐
│            PUSH WORKFLOW                │
├─────────────────────────────────────────┤
│ QUALITY GATE (via /check)               │
│ ├── Lint: ✓                             │
│ ├── Types: ✓                            │
│ ├── Tests: ✓ (42 passed)                │
│ └── Build: ✓                            │
├─────────────────────────────────────────┤
│ CHANGES                                 │
│ ├── Files: 3                            │
│ ├── Insertions: +42                     │
│ └── Deletions: -12                      │
├─────────────────────────────────────────┤
│ COMMIT                                  │
│ ├── Type: feat                          │
│ ├── Scope: auth                         │
│ └── Hash: abc1234                       │
├─────────────────────────────────────────┤
│ PUSHED → origin/feature-branch          │
│ CI: ⏳ Running...                       │
└─────────────────────────────────────────┘
```

---

**Now analyze changes and push: $ARGUMENTS**
