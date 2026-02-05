# End-to-End Feature Development

Implement a complete feature: $ARGUMENTS

---

## Composable Command

**This command automatically includes:**
- `context-prime` - Load relevant context
- `tdd` - Test-driven implementation
- `check` - Quality verification
- `pr-review` - Self-review before PR

---

## Feature Development Workflow

### Phase 1: Context & Requirements (via context-prime)

Load project context, then define:

```markdown
## Feature: $ARGUMENTS

### User Story
As a [user type]
I want to [action]
So that [benefit]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

### Phase 2: Design

Create task breakdown:
```
Feature: $ARGUMENTS
├── Backend
│   ├── Data model
│   ├── API endpoints
│   └── Business logic
├── Frontend
│   ├── Components
│   ├── State
│   └── UI/UX
└── Testing
    ├── Unit tests
    ├── Integration
    └── E2E
```

### Phase 3: Implementation (via tdd)

For each component, follow TDD:

1. **RED** - Write failing test
2. **GREEN** - Implement minimum code
3. **REFACTOR** - Clean up

Order:
1. Database/Models
2. Backend/API
3. Frontend/UI
4. Integration

### Phase 4: Quality (via check)

Run all checks:
- [ ] Lint passes
- [ ] Types pass
- [ ] Tests pass
- [ ] Build succeeds

### Phase 5: Self-Review (via pr-review)

Before creating PR:
- [ ] Architecture review
- [ ] Security review
- [ ] Performance review
- [ ] Code quality review

### Phase 6: PR Preparation

```markdown
## Summary
<description>

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

🤖 Generated with Claude Code
```

---

## Linked Commands

This command uses:
- `context-prime` - Context loading (automatic)
- `tdd` - Test-driven development (automatic)
- `check` - Quality gate (automatic)
- `pr-review` - Self-review (automatic)

Works well with:
- `/project:flow feature <name>` - Same workflow via orchestrator
- `/project:push` - After feature is ready

---

## Output

```
┌─────────────────────────────────────────┐
│         FEATURE DEVELOPMENT             │
├─────────────────────────────────────────┤
│ Feature: $ARGUMENTS                     │
├─────────────────────────────────────────┤
│ PHASE 1: Context (via /context-prime)   │
│ └── Project context loaded ✓            │
├─────────────────────────────────────────┤
│ PHASE 2: Design                         │
│ └── Task breakdown created ✓            │
├─────────────────────────────────────────┤
│ PHASE 3: Implementation (via /tdd)      │
│ ├── Backend: ✓                          │
│ ├── Frontend: ✓                         │
│ └── Tests: 12 passing                   │
├─────────────────────────────────────────┤
│ PHASE 4: Quality (via /check)           │
│ └── All checks passed ✓                 │
├─────────────────────────────────────────┤
│ PHASE 5: Review (via /pr-review)        │
│ └── Self-review complete ✓              │
├─────────────────────────────────────────┤
│ STATUS: Ready for PR                    │
└─────────────────────────────────────────┘
```

---

**Now develop feature: $ARGUMENTS**
