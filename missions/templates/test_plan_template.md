# Test Plan Template

## Change Reference

- **Mission**: [link to mission file]
- **Contract**: [link to implementation contract]
- **Date**: [YYYY-MM-DD]

## Test Layers

### Layer 1: Repository Logic Tests

> Tests for Python tooling and templates — no ESP-IDF or hardware needed.

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | | | | ⬜ |

### Layer 2: Host-Side Logic Tests

> Tests for pure C/C++ logic compiled and run on the host — no target needed.

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | | | | ⬜ |

### Layer 3: ESP-IDF Unit Tests

> Tests using the ESP-IDF Unity framework running on the target.

| # | Test Case | Component | Expected Behavior | Status |
|---|-----------|-----------|-------------------|--------|
| 1 | | | | ⬜ |

### Layer 4: Target Integration Tests

> Tests using `pytest-embedded` that flash firmware and validate behavior.

| # | Test Case | Setup Required | Expected Behavior | Status |
|---|-----------|---------------|-------------------|--------|
| 1 | | | | ⬜ |

## Infrastructure Requirements

- [ ] [Test fixtures or mocks needed]
- [ ] [Test data or configuration files]
- [ ] [Hardware setup for target tests]

## No-Hardware Tests

[List all tests from Layers 1 and 2 that can run in CI without hardware:]
- [ ] [Test name]

## Hardware-Required Tests

[List all tests from Layers 3 and 4 that need real hardware:]
- [ ] [Test name] — marked with `@pytest.mark.hardware`

## Coverage Goals

- **Statement coverage**: [X%] on changed files
- **Branch coverage**: [X%] on changed files
- **Critical paths** that MUST be covered:
  - [Path description]

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Not started |
| 🔄 | In progress |
| ✅ | Passed |
| ❌ | Failed |
| ⏭️ | Skipped |
