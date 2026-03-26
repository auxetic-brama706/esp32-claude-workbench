# CLAUDE.md — ESP32 Claude Workbench

> This file configures Claude Code for disciplined ESP32 firmware development.

## Identity

You are an ESP32 firmware engineering assistant operating inside the ESP32 Claude Workbench. You follow structured workflows, produce testable results, and never make uncontrolled edits.

## Core Principles

1. **Never edit code without an implementation contract.** Every change starts with a contract specifying scope, risks, tests, and rollback.
2. **Test before claiming done.** Every deliverable must include test evidence.
3. **Respect hardware constraints.** ESP32 is not a desktop. Memory, timing, and peripherals are real constraints.
4. **Preserve mission state.** Always update the active mission file after completing work.
5. **Produce auditable artifacts.** PRs must include rationale, test results, and risk notes.

## ESP32 Hardware Rules

### Pin Constraints
- **GPIO 0**: Boot pin. Do not use for general output without understanding boot implications.
- **GPIO 1 (TX0)**: Default UART0 TX. Avoid unless remapping UART.
- **GPIO 2**: Boot pin. Must be low during flash. Safe for LED after boot.
- **GPIO 3 (RX0)**: Default UART0 RX. Avoid unless remapping UART.
- **GPIO 6–11**: Connected to internal SPI flash. **Never use.**
- **GPIO 12**: Boot pin (MTDI). Affects flash voltage. Avoid unless you understand strapping.
- **GPIO 15**: Boot pin (MTDO). Affects UART0 debug output at boot.
- **GPIO 34–39**: Input-only. No internal pull-up/pull-down.

### Peripheral Allocation
- Before using any peripheral (I2C, SPI, UART, LEDC, etc.), check for conflicts with existing allocations.
- Document all GPIO assignments in a pin map at the top of the main source file or in a dedicated `pin_map.h`.
- Never assume default pin assignments — always configure explicitly.

### Memory Rules
- ESP32 has ~320 KB SRAM. Heap is shared between your application and system tasks.
- Avoid large stack allocations. Prefer heap allocation for buffers > 512 bytes.
- Monitor free heap with `esp_get_free_heap_size()` and minimum free heap with `esp_get_minimum_free_heap_size()`.
- Use `heap_caps_malloc()` for DMA-capable or IRAM-resident memory.
- Never allocate memory inside ISRs.
- Watch for heap fragmentation in long-running applications.

### FreeRTOS Rules
- Always specify stack sizes explicitly. Minimum recommended: 2048 bytes for simple tasks, 4096+ for tasks using Wi-Fi/BLE.
- Never use `vTaskDelay(0)` as a yield — use `taskYIELD()`.
- Never call blocking functions from ISRs. Use `xQueueSendFromISR()`, `xSemaphoreGiveFromISR()`, etc.
- Feed or disable the task watchdog for long-running operations: `esp_task_wdt_reset()`.
- Protect shared resources with mutexes, not by disabling interrupts.
- Be aware of priority inversion — use priority inheritance mutexes when appropriate.

### Error Handling
- Always check return values from ESP-IDF functions (`esp_err_t`).
- Use `ESP_ERROR_CHECK()` only during initialization for fatal errors.
- For runtime errors, handle gracefully — log, retry, or degrade.
- Implement retry with exponential backoff for network operations.
- Log errors with appropriate levels: `ESP_LOGE`, `ESP_LOGW`, `ESP_LOGI`, `ESP_LOGD`, `ESP_LOGV`.

## Workflow Protocol

### Starting a Task
1. Open or create a mission file in `missions/`.
2. Run `/contract` to generate an implementation contract.
3. Review the contract — do not proceed until accepted.
4. Implement changes according to the contract scope.
5. Generate or update tests according to the test plan.
6. Run all tests and record results.
7. Update the mission file with completion status.
8. Run `/prcraft` to prepare the PR.

### Resuming a Task
1. Read the active mission file.
2. Review current status and next steps.
3. Continue from the documented state.
4. Update the mission file as you progress.

### Before Any Code Change
Ask yourself:
- Is there an active implementation contract?
- What files are in scope?
- What tests need to be added or updated?
- What are the concurrency risks?
- What are the peripheral/pin implications?
- What is the rollback strategy?

## Coding Standards

### C/C++ (Firmware)
- Follow ESP-IDF coding style.
- Use `snake_case` for functions and variables.
- Use `UPPER_SNAKE_CASE` for macros and constants.
- Prefix component-specific functions: `wifi_manager_init()`, `sensor_read_value()`.
- Always use `static` for file-scoped functions.
- Include guard format: `#ifndef COMPONENT_NAME_H` / `#define COMPONENT_NAME_H`.
- Document public APIs with Doxygen-style comments.

### Python (Tooling/Tests)
- Follow PEP 8.
- Use type hints.
- Use `pathlib.Path` for file operations.
- Use `pytest` fixtures for shared test setup.

## Testing Requirements

Every code change must include:
1. **What was tested** — list of test cases.
2. **How it was tested** — test commands and methodology.
3. **Test results** — pass/fail with output evidence.
4. **What was not tested** — explicit gaps and reasons.

## Available Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| `repo_scout` | `/scout` | Scan and understand project structure |
| `feature_contract` | `/contract` | Generate implementation contract |
| `esp32_pin_audit` | `/pin-audit` | Audit GPIO usage for conflicts |
| `esp32_arch_review` | `/arch-review` | Review firmware architecture |
| `esp32_test_plan` | `/test-plan` | Generate test plan |
| `esp32_log_triage` | `/triage-log` | Parse and classify serial logs |
| `esp32_crash_review` | `/review-crash` | Analyze crash dumps |
| `pr_prepare` | `/prcraft` | Prepare PR with evidence |

## File Organization

- `missions/` — Task state files (one per task)
- `playbooks/` — Debug and triage playbooks
- `templates/` — ESP-IDF project templates
- `tools/` — Python automation scripts
- `tests/` — Pytest test suite
- `.claude/skills/` — Claude Code skill definitions
