---
name: pr_prepare
description: Prepare a pull request with structured description, test evidence, risk assessment, and review checklist.
---

# PR Prepare

Generate a complete, reviewable pull request with all required evidence and documentation.

## When to Use

- After completing implementation and testing.
- Before submitting code for review.
- When updating a mission to "complete" status.

## Steps

### 1. Collect Implementation Artifacts

Gather from the mission file and implementation contract:
- Change summary and motivation.
- List of affected files.
- Non-goals (what was intentionally excluded).
- Risk assessment from the contract.

### 2. Compile Test Evidence

Document all test results:
- Test commands run and their output.
- Pass/fail counts.
- Coverage report (if available).
- Any skipped tests with reason (e.g., requires hardware).
- Serial log excerpts for target tests.

### 3. Generate PR Description

```markdown
## Summary

[One-paragraph description of the change and why it was needed]

## Changes

### Files Modified
| File | Change Type | Description |
|------|------------|-------------|
| `path/to/file` | Modified | [Brief description] |

### Architecture Impact
- [How this affects the overall system]
- [New dependencies introduced]

## Testing

### Tests Run
```
[paste test command and output]
```

### Test Summary
- ✅ [N] passed
- ❌ [N] failed
- ⏭️ [N] skipped (hardware-required)

### Coverage
- [X]% statement coverage on changed files

## Risk Assessment

| Risk | Level | Mitigation |
|------|-------|-----------|
| [Risk description] | LOW/MED/HIGH | [How it's handled] |

## Rollback Plan

[Steps to safely revert this change if needed]

## Checklist

- [ ] Implementation contract reviewed and accepted
- [ ] All acceptance criteria met
- [ ] Tests added for new functionality
- [ ] No regressions in existing tests
- [ ] Pin audit passed (if GPIO changes)
- [ ] Architecture review passed (if structural changes)
- [ ] Documentation updated
- [ ] Mission file updated with completion status
```

### 4. Link to Mission File

Reference the mission file in the PR so reviewers can see the full context:
- Original mission with goals and constraints.
- Implementation contract with scope and risks.
- Test plan with detailed cases.

### 5. Review Readiness Check

Before submitting, verify:
- [ ] All CI checks would pass.
- [ ] No uncommitted changes.
- [ ] Commit messages are descriptive.
- [ ] PR description is complete.
- [ ] No debugging code left in.
- [ ] No `TODO` or `FIXME` without issue references.

## Rules

1. **Never submit a PR without test evidence.** Even if tests are manual, document the results.
2. **Include risk assessment.** Reviewers need to know what could go wrong.
3. **Link to the mission.** Provide full traceability.
4. **Keep the PR focused.** If scope grew beyond the contract, split into multiple PRs.
