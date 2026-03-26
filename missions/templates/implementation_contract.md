# Implementation Contract

> Fill this out BEFORE writing any code. Get it reviewed and accepted first.

## Change Summary

[One paragraph describing what will change and why.]

## Non-Goals

- [What this change explicitly does NOT do]
- [Scope boundaries to prevent creep]

## Affected Files

| File | Action | Description |
|------|--------|-------------|
| `path/to/file.c` | MODIFY | [What changes and why] |
| `path/to/new.h` | CREATE | [Purpose of new file] |

## APIs Touched

| Function / Interface | Change | Breaking? |
|---------------------|--------|-----------|
| `function_name()` | [How it changes] | YES / NO |

## Risk Assessment

### Concurrency Risk: LOW / MEDIUM / HIGH
[Details: shared state, task interactions, race conditions]

### Peripheral Risk: LOW / MEDIUM / HIGH
[Details: pin conflicts, bus contention, timing]

### Memory Risk: LOW / MEDIUM / HIGH
[Details: heap impact, stack changes, buffer sizes]

### Boot Risk: LOW / MEDIUM / HIGH
[Details: strapping pins, init order, partition changes]

### Backward Compatibility: LOW / MEDIUM / HIGH
[Details: API changes, protocol changes, NVS schema]

## Test Plan

- [ ] [Specific test case with expected result]
- [ ] [Another test case]
- [ ] Existing tests updated for API changes.
- [ ] Coverage target: [X%] on changed code.

## Rollback Strategy

[How to revert this change:]
1. [Step 1]
2. [Step 2]

[State or data implications of rollback:]
- [NVS / filesystem / OTA implications]

## Acceptance Criteria

- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] All tests pass.
- [ ] PR prepared with evidence.

## Approval

- [ ] Contract reviewed
- [ ] Contract accepted — proceed with implementation
