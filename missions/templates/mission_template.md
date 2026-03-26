# Mission Template

> Copy this file to `missions/YYYY-MM-description.md` and fill in each section.

## Goal

[What needs to be accomplished. Be specific and measurable.]

## Board / Target

- **Chip**: [ESP32 / ESP32-S2 / ESP32-S3 / ESP32-C3 / ESP32-C6 / ESP32-H2]
- **Board**: [DevKitC / custom / etc.]
- **ESP-IDF version**: [e.g., v5.2]

## Constraints

- [Hardware constraints — available pins, peripherals, power budget]
- [Software constraints — RTOS priorities, memory budget, latency requirements]
- [Project constraints — backward compatibility, API stability, timeline]

## Files in Scope

| File | Action | Notes |
|------|--------|-------|
| `path/to/file` | CREATE / MODIFY / DELETE | [Brief description] |

## Design Notes

[Architecture decisions, trade-offs, alternative approaches considered and rejected.]

## Acceptance Criteria

- [ ] [Specific, testable criterion]
- [ ] [Another criterion]
- [ ] All existing tests pass.
- [ ] New tests cover the change.
- [ ] Pin audit passes (if GPIO changes).

## Test Plan

> Reference `missions/templates/test_plan_template.md` for detailed structure.

- [ ] [Test case 1]
- [ ] [Test case 2]
- [ ] No-hardware tests pass.
- [ ] Hardware tests pass (if applicable, mark with `@pytest.mark.hardware`).

## Known Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| [Description] | LOW/MED/HIGH | [How to handle] |

## Current Status

- **State**: NOT STARTED / IN PROGRESS / BLOCKED / REVIEW / DONE
- **Last updated**: [date]
- **Completed items**: [list]
- **Blocking issues**: [list]

## Next Step

[The single most important next action.]

## History

| Date | Action | Notes |
|------|--------|-------|
| [date] | Created | Initial mission |
