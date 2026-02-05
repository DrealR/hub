# Test-Driven Development Cycle

Run a TDD cycle for: $ARGUMENTS

---

## TDD Workflow: Red → Green → Refactor

### Phase 1: RED (Write Failing Test)

**Before writing any implementation code:**

1. **Understand the requirement**
   - What behavior are we implementing?
   - What are the inputs and expected outputs?
   - What edge cases exist?

2. **Write the test first**
   ```
   // Example structure:
   describe('<feature>', () => {
     it('should <expected behavior>', () => {
       // Arrange - set up test data
       // Act - call the function/method
       // Assert - verify the result
     });
   });
   ```

3. **Run the test - it MUST fail**
   - If it passes, the test is wrong or the feature already exists
   - The failure message should be meaningful

### Phase 2: GREEN (Make It Pass)

**Write the minimum code to make the test pass:**

1. **Implement only what's needed**
   - Don't over-engineer
   - Don't add extra features
   - Focus on passing the specific test

2. **Run the test - it MUST pass**
   - If it fails, fix the implementation
   - Don't modify the test (unless it was wrong)

3. **Verify no regressions**
   - Run the full test suite
   - All existing tests should still pass

### Phase 3: REFACTOR (Improve the Code)

**Now improve the code while keeping tests green:**

1. **Code quality improvements**
   - Remove duplication
   - Improve naming
   - Simplify logic
   - Extract methods/functions

2. **Run tests after each change**
   - Tests must stay green
   - If they fail, undo the refactor

3. **Consider edge cases**
   - Add more tests if needed
   - Each new test follows the same cycle

## TDD Commands

### Red Phase
```bash
# Run tests expecting failure
npm test -- --testNamePattern="<test name>"
# or
pytest -k "<test name>" -x
```

### Green Phase
```bash
# Run single test
npm test -- --testNamePattern="<test name>"
```

### Refactor Phase
```bash
# Run full suite
npm test
# or
pytest
```

## Output Format

```
┌─────────────────────────────────────────┐
│           TDD CYCLE STATUS              │
├─────────────────────────────────────────┤
│ Feature: $ARGUMENTS                     │
├─────────────────────────────────────────┤
│ Phase: RED                              │
│ Test: should handle empty input         │
│ Status: ✗ FAILING (as expected)         │
├─────────────────────────────────────────┤
│ Next: Implement minimum code to pass    │
└─────────────────────────────────────────┘
```

## Best Practices

- **One test at a time** - Don't write multiple failing tests
- **Small increments** - Each cycle should be quick (minutes, not hours)
- **Meaningful assertions** - Test behavior, not implementation
- **Clear test names** - Describe what should happen

---

**Now start a TDD cycle for: $ARGUMENTS**
