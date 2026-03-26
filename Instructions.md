# ESP32 Claude Workbench

**Tagline:** Deterministic AI workflow for ESP32 firmware development.

## Vision

We are not building another prompt collection.

We are building a real GitHub repository that helps firmware developers use Claude Code in a disciplined, testable, repeatable way for ESP32 development. The goal is to reduce wasted time, reduce regressions, improve debugging, and give developers a workflow they can trust.

This repository should become the default starting point for anyone who wants to use Claude Code seriously in embedded development.

## Core Idea

Most AI coding setups fail in firmware because they are:
- Too chat-based.
- Not stateful enough.
- Weak on testing.
- Weak on hardware constraints.
- Weak on debugging workflows.
- Weak on CI structure.
- Good at generating code, bad at proving the code is safe.

This repository solves that by combining:
- Claude Code workflow rules.
- Structured markdown state files.
- ESP32-specific engineering playbooks.
- Build and test automation.
- Pytest-based validation strategy.
- CI-ready quality gates.
- Reusable project templates.

## Real Developer Problems To Solve

### 1. AI generates code but does not understand embedded constraints
Typical pain:
- Wrong pin assumptions.
- Invalid peripheral combinations.
- Unsafe blocking calls.
- Broken FreeRTOS interactions.
- Heap fragmentation risks.
- Watchdog problems.
- Boot pin misuse.
- Poor error handling.

What we provide:
- ESP32-specific design rules in `CLAUDE.md`.
- Pin audit workflow.
- Peripheral compatibility checklists.
- RTOS safety review commands.
- Memory and watchdog review playbooks.

### 2. Developers lose context across long tasks
Typical pain:
- The session becomes huge.
- The model forgets constraints.
- A new session cannot resume the work safely.
- Partial work has no reliable state.

What we provide:
- Persistent markdown mission files.
- Structured task state.
- File-scoped implementation plans.
- Resume workflow.
- Explicit acceptance criteria and risk logs.

### 3. Firmware testing is fragmented and often skipped
Typical pain:
- Code compiles but does not really work.
- Developers rely too much on manual serial inspection.
- Testing is weak in firmware projects.
- CI is often compile-only.

What we provide:
- First-class testing architecture from the start.
- Host-side unit tests where possible.
- ESP-IDF unit-test integration.
- `pytest` and `pytest-embedded` support for target testing.
- Serial output assertions.
- JUnit reports in CI.
- Clear separation between no-hardware and hardware-in-the-loop tests.

### 4. Debugging embedded failures is repetitive and undocumented
Typical pain:
- Guru Meditation errors waste hours.
- Developers re-debug the same boot loop or peripheral issue.
- Logs are noisy and poorly interpreted.
- There is no standard fault triage process.

What we provide:
- Debugging playbooks.
- Log triage patterns.
- Failure classification commands.
- Crash analysis templates.
- Repeatable bug-investigation workflow.

### 5. AI-assisted firmware changes are hard to trust in teams
Typical pain:
- Hard to review AI-generated changes.
- Missing rationale.
- Poor test evidence.
- Unclear risk surface.

What we provide:
- PR preparation workflow.
- Required implementation contract.
- Test evidence checklist.
- Risk notes.
- Rollback notes.
- Architecture impact summary.

## Positioning

This repository is not:
- Another ESP32 examples repo.
- Another list of prompts.
- Another AI wrapper.
- Another generic embedded toolkit.

This repository is:
- A structured Claude Code workflow for ESP32 firmware.
- A reliability layer for AI-assisted embedded development.
- A testing-first embedded AI workbench.
- A practical system for turning vague requests into validated firmware work.

## Initial Audience

Primary users:
- ESP-IDF developers.
- Firmware engineers exploring AI-assisted workflows.
- Embedded developers who want repeatable testing and review.
- Developers who want to use Claude Code without losing control of their codebase.

Secondary users:
- PlatformIO users later.
- Other microcontroller developers later.
- Teams building connected devices and prototypes.

## Why ESP32 First

ESP32 is a strong entry point because:
- It has a very large developer ecosystem.
- It is widely used in IoT and connected devices.
- It has enough complexity to make AI workflows valuable.
- It supports meaningful demos: Wi-Fi, BLE, sensors, serial logs, OTA, RTOS tasks.
- It is broad enough to attract many developers, but specific enough to make the repository focused.

Even without owning hardware, we can still build the core system because the first value is not flashing a board. The first value is making firmware work more structured, testable, and reviewable.

## Strategic Principle

**Do not start from hardware. Start from failure modes.**

The repository should be designed around the real failure modes of firmware developers:
- Build breaks.
- Incorrect architecture changes.
- Pin conflicts.
- Memory misuse.
- Race conditions.
- Peripheral integration failures.
- Missing tests.
- Hard-to-review AI edits.
- Context loss across sessions.

If we solve these, the repository becomes useful.

## Main Repository Components

### 1. Workflow Engine
Purpose:
- Turn Claude Code into a structured development protocol.

Files:
- `CLAUDE.md`
- `.claude/skills/...`
- `missions/...`
- command templates
- implementation contracts

### 2. Testing System
Purpose:
- Make testing a first-class citizen.

Layers:
- Static analysis and linting.
- Build validation.
- Host-side logic tests.
- ESP-IDF unit tests.
- Pytest-based target tests.
- CI reporting.

### 3. Debug Playbooks
Purpose:
- Standardize firmware troubleshooting.

Examples:
- boot-loop triage
- Guru Meditation triage
- watchdog reset analysis
- heap/stack issue review
- I2C bring-up
- SPI bring-up
- UART debugging
- Wi-Fi connection failure investigation
- BLE initialization failure

### 4. Project Templates
Purpose:
- Give developers something usable immediately.

Examples:
- Wi-Fi sensor node
- BLE peripheral
- MQTT telemetry node
- Web dashboard firmware
- low-power logger

### 5. CI and Review System
Purpose:
- Make AI-generated firmware changes auditable.

Outputs:
- build matrix
- test reports
- lint reports
- risk checklist
- generated PR body template
- traceable mission file

## Real Feature Set To Build

### Must-Have Features

#### Mission files
Each task gets a markdown file such as:

`missions/2026-03-esp32-wifi-reconnect.md`

Structure:
- Goal
- Board/target
- Constraints
- Files in scope
- Design notes
- Acceptance criteria
- Test plan
- Known risks
- Current status
- Next step

Why this matters:
- It preserves state across sessions.
- It reduces context loss.
- It makes AI-assisted work reviewable.
- It creates visible project memory.

#### Implementation contract
Before code changes, Claude should generate:
- summary of requested change
- non-goals
- affected files
- APIs touched
- concurrency/peripheral risks
- tests to add
- rollback strategy

This prevents random uncontrolled edits.

#### Pin audit
A workflow that checks:
- reserved pins
- bootstrapping pins
- peripheral conflicts
- declared GPIO usage
- comments/docs drift

This can later become partially automated.

#### Firmware review mode
A stricter review path focused on:
- RTOS safety
- error handling
- timeout behavior
- retries and backoff
- stack/heap impact
- ISR misuse
- logging quality
- persistent storage safety

#### Release-readiness checklist
Before merge or release:
- build passes
- tests pass
- log noise reviewed
- partition assumptions documented
- OTA compatibility checked
- NVS schema notes captured
- rollback notes written

## Recommended Commands / Skills

We should prefer a modern skills-based layout, while still exposing memorable command-style workflows.

### Core workflow skills
- `repo_scout`
- `feature_contract`
- `task_shard`
- `esp32_pin_audit`
- `esp32_arch_review`
- `esp32_driver_implement`
- `esp32_test_plan`
- `esp32_log_triage`
- `esp32_crash_review`
- `pr_prepare`

### User-facing command ideas
- `/scout`
- `/contract`
- `/shard`
- `/pin-audit`
- `/arch-review`
- `/implement-driver`
- `/test-plan`
- `/triage-log`
- `/review-crash`
- `/prcraft`
- `/resume`

## Testing Strategy

Testing is one of the strongest differentiators of this repository.

### Testing Philosophy

We should support two realities:

#### Reality A: No hardware available
This is completely acceptable for early development.

We still provide value through:
- compile checks
- linting
- static analysis
- architecture reviews
- host-side tests for pure logic
- parser tests
- config validation
- code generation tests
- markdown/state validation

#### Reality B: Hardware available later
We extend the system with:
- target unit tests
- serial-log assertions
- flash/monitor automation
- peripheral smoke tests
- integration tests using `pytest-embedded`

### Testing Layers

#### Layer 1: Repository logic tests
Test the repository tooling itself:
- mission file generation
- markdown schema validation
- command template correctness
- file classification
- report generation

Use:
- `pytest`

#### Layer 2: Firmware logic tests without target
Test pure C logic where possible:
- parsers
- utility functions
- state machines
- protocol encoding/decoding
- retry/backoff logic via mocks

Use:
- `pytest` for orchestration
- native/unit-test support where possible
- mock-based host tests

#### Layer 3: ESP-IDF unit tests
Use official ESP-IDF unit-testing approaches for firmware components.

Test:
- components under `test/`
- isolated behavior
- edge cases
- internal APIs

#### Layer 4: Target integration tests
Use `pytest` with `pytest-embedded` for:
- flashing firmware
- serial log assertions
- boot success checks
- interactive command/response validation
- environment-aware test runs

#### Layer 5: CI result publishing
Produce:
- JUnit XML
- logs
- artifacts
- test summaries
- failure triage bundles

## Why Pytest Is The Right Center

Pytest is a strong choice because:
- It is widely known.
- ESP-IDF already documents pytest-based target testing.
- `pytest-embedded` exists specifically for embedded workflows.
- It supports markers, parametrization, fixtures, reports, and CI integration.
- It can unify repository tests and target tests under one familiar runner.

This is ideal for making the repo professional instead of ad hoc.

## Proposed Testing Stack

### Core
- `pytest`
- `pytest-xdist`
- `pytest-cov`
- `pytest-json-report`

### Embedded-specific
- `pytest-embedded`

### Output and CI
- JUnit XML reports
- saved serial logs
- artifact upload in GitHub Actions

### Optional later
- property-based testing for parsers/state machines
- fuzz testing for protocol handlers
- static analyzers
- coverage dashboards

## Best “No Hardware Yet” MVP

We should build an MVP that proves value before owning any board.

### MVP Goal
A developer should be able to clone the repo and immediately get:
- a structured Claude workflow
- mission files
- implementation contracts
- test planning
- static QA
- firmware review checklists
- CI-friendly outputs

### MVP Scope
- ESP-IDF-first structure
- no live flashing required
- strong docs
- mission-driven workflow
- test skeletons
- example project
- GitHub Actions for validation
- clean README with demos

### MVP Deliverables
1. `README.md`
2. `CLAUDE.md`
3. `.claude/skills/`
4. `missions/templates/`
5. `playbooks/`
6. `templates/esp-idf-basic/`
7. `tests/`
8. `.github/workflows/ci.yml`
9. sample reports
10. contribution guide

## Sample Pain-Driven Playbooks To Include

### Playbook: Build failure triage
Helps Claude classify:
- include path problems
- sdkconfig mismatch
- target mismatch
- component registration errors
- linker errors
- missing Kconfig options

### Playbook: Guru Meditation review
Helps Claude inspect:
- exception type
- likely null dereference
- stack overflow suspicion
- ISR misuse
- memory corruption clues
- next diagnostic steps

### Playbook: Wi-Fi failure investigation
Helps Claude check:
- init sequence
- event loop setup
- credentials source
- retry logic
- timeout handling
- log signatures

### Playbook: I2C bring-up
Helps Claude review:
- SDA/SCL choice
- pull-up assumptions
- frequency settings
- address handling
- timeout behavior
- bus recovery path

### Playbook: Watchdog reset review
Helps Claude inspect:
- blocking code
- task starvation
- missing yields
- long critical sections
- ISR abuse

## Strong Differentiators

To earn stars, we need differentiators that are obvious and useful.

### Differentiator 1: Persistent markdown state
This is the repository memory system.

### Differentiator 2: Firmware-native review
Not generic code review. Real embedded review.

### Differentiator 3: Testing-first AI workflow
Not “Claude wrote code.”  
Instead: “Claude proposed changes, generated tests, and produced review artifacts.”

### Differentiator 4: Useful even without hardware
This increases adoption dramatically.

### Differentiator 5: Designed for trust
The repo helps humans inspect and verify AI-generated work.

## Initial Directory Structure

```text
esp32-claude-workbench/
├─ README.md
├─ LICENSE
├─ CLAUDE.md
├─ CONTRIBUTING.md
├─ pyproject.toml
├─ .gitignore
├─ .claude/
│  └─ skills/
│     ├─ repo_scout/
│     │  └─ SKILL.md
│     ├─ feature_contract/
│     │  └─ SKILL.md
│     ├─ esp32_pin_audit/
│     │  └─ SKILL.md
│     ├─ esp32_arch_review/
│     │  └─ SKILL.md
│     ├─ esp32_test_plan/
│     │  └─ SKILL.md
│     ├─ esp32_log_triage/
│     │  └─ SKILL.md
│     ├─ esp32_crash_review/
│     │  └─ SKILL.md
│     └─ pr_prepare/
│        └─ SKILL.md
├─ missions/
│  ├─ templates/
│  │  ├─ mission_template.md
│  │  ├─ implementation_contract.md
│  │  └─ test_plan_template.md
│  └─ examples/
├─ playbooks/
│  ├─ build_failure.md
│  ├─ guru_meditation.md
│  ├─ wifi_debug.md
│  ├─ i2c_bringup.md
│  ├─ watchdog_reset.md
│  └─ memory_review.md
├─ templates/
│  └─ esp-idf-basic/
├─ tools/
│  ├─ validate_mission.py
│  ├─ generate_contract.py
│  └─ summarize_logs.py
├─ tests/
│  ├─ test_mission_templates.py
│  ├─ test_contract_generation.py
│  ├─ test_log_parsing.py
│  └─ test_playbook_integrity.py
└─ .github/
   └─ workflows/
      ├─ ci.yml
      └─ claude.yml
```

## Launch Strategy

### Phase 1
Ship the foundation:
- clean README
- strong repo concept
- mission templates
- 5 to 8 skills
- testing skeleton
- one example project
- CI pipeline

### Phase 2
Add practical depth:
- log triage helpers
- pin audit improvements
- PR generation workflow
- more tests
- more examples

### Phase 3
Add real target testing:
- hardware test support
- `pytest-embedded` examples
- serial assertions
- flash/monitor workflow
- hardware-in-the-loop guidance

## README Promise

The README must communicate this clearly:

> ESP32 Claude Workbench helps firmware developers use Claude Code safely and effectively with structured workflows, persistent task state, testing-first development, and embedded-specific review/playbooks.

The README should show:
- the pain
- the workflow
- the files
- the commands
- the outputs
- the testing strategy
- a concrete example issue turned into a mission and PR

## What Success Looks Like

A starred and useful repository should make people say:

- “This is the first AI firmware repo that feels serious.”
- “I can use this even before connecting hardware.”
- “This gives me a repeatable workflow, not random prompting.”
- “This helps me test and review AI-generated embedded changes.”
- “This is actually useful for my real ESP32 work.”

## Non-Negotiable Principles

- Solve real developer pain.
- Prefer structure over magic.
- Prefer testing over claims.
- Prefer auditable artifacts over chat output.
- Prefer reproducible workflows over clever prompts.
- Be useful without hardware.
- Make adoption easy.
- Make the repository visually clean and professional.

## Immediate Next Steps

1. Finalize repository name.
2. Create the root README.
3. Draft `CLAUDE.md`.
4. Create the first 5 skills.
5. Create mission and contract templates.
6. Add Python tooling and `pytest` test skeleton.
7. Add CI workflow.
8. Add one realistic example flow.
9. Add screenshots/GIFs later.
10. Publish early and iterate from developer feedback.