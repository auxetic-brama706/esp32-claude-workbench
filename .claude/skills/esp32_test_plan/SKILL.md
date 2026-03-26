---
name: esp32_test_plan
description: Generate a structured test plan for ESP32 firmware changes across all testing layers.
---

# ESP32 Test Plan

Generate a comprehensive test plan covering all applicable testing layers for a firmware change.

## When to Use

- After an implementation contract is accepted.
- Before starting implementation.
- When adding test coverage to existing code.

## Steps

### 1. Classify the Change

Determine which testing layers apply:

| Layer | Applies When | Tools |
|-------|-------------|-------|
| Repository logic | Change involves Python tooling or templates | `pytest` |
| Host-side logic | Change involves pure C logic (parsers, state machines, encoders) | `pytest` + native compilation |
| ESP-IDF unit tests | Change modifies an isolated component | ESP-IDF `unity` framework |
| Target integration | Change requires real hardware validation | `pytest-embedded` |
| Static analysis | Always | `cppcheck`, compiler warnings |

### 2. Identify Test Cases

For each applicable layer, list specific test cases:

**Positive cases**: Expected behavior with valid inputs.
**Negative cases**: Behavior with invalid inputs, null pointers, edge values.
**Boundary cases**: Limits of buffers, ranges, timeouts.
**Concurrency cases**: Race conditions, shared state under load.
**Error cases**: Failure paths, recovery behavior.

### 3. Define Test Infrastructure

Specify what is needed:
- New test files to create.
- Fixtures or mocks required.
- Test data or configuration.
- Hardware requirements (if any).

### 4. Set Pass/Fail Criteria

For each test case:
- Expected result.
- Acceptable tolerance (for timing or analog tests).
- Required evidence (log output, assertion pass, measurement).

### 5. Generate Test Plan Document

Use the template at `missions/templates/test_plan_template.md`:

```markdown
# Test Plan: [Feature Name]

## Change Reference
- Contract: [link to implementation contract]
- Mission: [link to mission file]

## Test Layers

### Layer 1: Repository Logic
| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|

### Layer 2: Host-Side Logic
| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|

### Layer 3: ESP-IDF Unit Tests
| Test Case | Component | Expected Behavior | Status |
|-----------|-----------|-------------------|--------|

### Layer 4: Target Integration
| Test Case | Setup Required | Expected Behavior | Status |
|-----------|---------------|-------------------|--------|

## Infrastructure Requirements
- [ ] [Requirement]

## No-Hardware Tests
[List tests that can run without ESP32 hardware]

## Hardware-Required Tests
[List tests that need real hardware, marked with pytest `@pytest.mark.hardware`]

## Coverage Goals
- Statement coverage target: [X%]
- Branch coverage target: [X%]
- Critical paths that MUST be covered: [list]
```

## Rules

1. **Every implementation contract must have a test plan.** No exceptions.
2. **Maximize no-hardware tests.** Extract and test pure logic separately.
3. **Mark hardware tests explicitly.** Use `@pytest.mark.hardware` so CI can skip them.
4. **Include negative tests.** Happy-path-only testing is insufficient for firmware.
