---
name: feature_contract
description: Generate a structured implementation contract before making any code changes to an ESP32 project.
---

# Feature Contract

Generate an implementation contract that must be reviewed and approved before any code changes begin.

## When to Use

- Before implementing any feature or bug fix.
- Before refactoring existing code.
- Before making any architecture changes.
- Always. No exceptions.

## Steps

### 1. Gather Requirements

Ask or determine:
- What is the requested change?
- What is the expected behavior after the change?
- What board/target is this for?
- Are there hardware constraints?

### 2. Define Scope

Document:
- **Summary**: One-paragraph description of the change.
- **Non-goals**: What this change explicitly does NOT do.
- **Affected files**: List every file that will be created, modified, or deleted.
- **APIs touched**: Public functions or interfaces that will change.

### 3. Assess Risks

Evaluate:
- **Concurrency risks**: Shared state, race conditions, task interactions.
- **Peripheral risks**: Pin conflicts, bus contention, timing issues.
- **Memory risks**: Heap impact, stack requirements, DMA buffers.
- **Boot risks**: Changes that affect boot sequence or strapping pins.
- **Backward compatibility**: Breaking changes to APIs or protocols.

### 4. Define Test Plan

Specify:
- **New tests to add**: Unit tests, integration tests, or validation scripts.
- **Existing tests to update**: Tests affected by the change.
- **Manual verification**: Steps for hardware testing if applicable.
- **Test evidence required**: What output proves the change works.

### 5. Define Rollback Strategy

Document:
- How to revert the change.
- What state needs to be restored.
- Any data migration or NVS implications.

### 6. Generate Contract Document

Write the contract to the active mission file or as a standalone document using the template at `missions/templates/implementation_contract.md`.

## Contract Template

```markdown
# Implementation Contract

## Change Summary
[One-paragraph description]

## Non-Goals
- [What this does NOT include]

## Affected Files
| File | Action | Description |
|------|--------|-------------|
| path/to/file.c | MODIFY | [What changes] |
| path/to/new.h | CREATE | [Purpose] |

## APIs Touched
- `function_name()` — [How it changes]

## Risk Assessment
### Concurrency: [LOW/MED/HIGH]
[Details]

### Peripheral: [LOW/MED/HIGH]
[Details]

### Memory: [LOW/MED/HIGH]
[Details]

## Test Plan
- [ ] [Test case description]

## Rollback Strategy
[Steps to revert]

## Acceptance Criteria
- [ ] [Criterion]
```

## Rules

1. **Never skip the contract.** Even small changes need a contract.
2. **Get approval before coding.** The contract must be accepted first.
3. **Update the contract if scope changes.** Scope creep must be documented.
4. **Reference the contract in the PR.** Link it for reviewers.
