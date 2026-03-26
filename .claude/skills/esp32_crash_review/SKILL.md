---
name: esp32_crash_review
description: Analyze ESP32 Guru Meditation errors and crash dumps to identify root cause and recommend fixes.
---

# ESP32 Crash Review

Analyze crash reports, Guru Meditation errors, and panic dumps to determine root cause.

## When to Use

- After observing a Guru Meditation error.
- When a device is stuck in a crash-reboot loop.
- When analyzing crash dumps from field devices.

## Steps

### 1. Identify the Exception Type

| Exception | Cause |
|-----------|-------|
| `LoadProhibited` | Read from invalid memory (often NULL pointer) |
| `StoreProhibited` | Write to invalid memory |
| `InstrFetchProhibited` | Tried to execute code from invalid address |
| `IllegalInstruction` | Stack corruption, code corruption, or invalid function pointer |
| `IntegerDivideByZero` | Division by zero |
| `Unaligned` | Unaligned memory access |

### 2. Extract Key Information

From the panic output, collect:

```
Guru Meditation Error: Core [0/1] panic'ed ([ExceptionType]).
Exception was unhandled.
Core [N] register dump:
PC      : 0x........  PS      : 0x........
A0      : 0x........  A1      : 0x........  ...
EXCVADDR: 0x........    ← The address that caused the fault
```

**PC** (Program Counter) → Where the crash happened.
**EXCVADDR** (Exception Address) → What address was accessed illegally.
**A1** → Stack pointer at time of crash.

### 3. Decode the Backtrace

```bash
# Using addr2line
xtensa-esp32-elf-addr2line -pfiaC -e build/project.elf ADDR1 ADDR2 ADDR3

# Using idf.py
idf.py monitor  # Automatically decodes backtraces

# Using ESP-IDF monitor with ELF
python -m esp_idf_monitor --port /dev/ttyUSB0 --baud 115200 build/project.elf
```

### 4. Analyze Common Patterns

#### NULL Pointer Dereference
- **EXCVADDR**: `0x00000000` or small value (< `0x100`)
- **Cause**: Using an uninitialized pointer or a handle that failed to initialize.
- **Fix**: Add NULL checks before dereferencing.

#### Stack Overflow
- **Signs**: `IllegalInstruction` or `LoadProhibited` with A1 near the end of stack space.
- **Cause**: Task stack too small, deep recursion, large local variables.
- **Fix**: Increase task stack size, reduce local buffer sizes, check recursion depth.

#### ISR Violation
- **Signs**: Crash inside a FreeRTOS API that is not `*FromISR`.
- **Cause**: Calling blocking functions from an interrupt handler.
- **Fix**: Use ISR-safe API variants only.

#### Memory Corruption
- **Signs**: `IllegalInstruction` at a random address, corrupted register values.
- **Cause**: Buffer overflow, use-after-free, heap corruption.
- **Fix**: Enable heap poisoning (`CONFIG_HEAP_POISONING_COMPREHENSIVE`), use AddressSanitizer.

#### Watchdog Reset (not Guru Meditation but related)
- **Signs**: `TG0WDT_SYS_RESET` or `TG1WDT_SYS_RESET` in reset reason.
- **Cause**: Task not yielding, blocking the idle task or system tasks.
- **Fix**: Add yields, reduce critical section length, feed watchdog.

### 5. Recommend Diagnostic Steps

Based on the analysis, suggest:
1. **Immediate fix** — if root cause is clear.
2. **Diagnostic configuration** — enable features that help narrow down:
   - `CONFIG_HEAP_POISONING_COMPREHENSIVE=y`
   - `CONFIG_HEAP_TASK_TRACKING=y`
   - `CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK=y`
   - `CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT=y`
   - `CONFIG_COMPILER_STACK_CHECK=y`
3. **Reproduction steps** — minimal steps to trigger the crash again.

### 6. Generate Crash Report

```markdown
# Crash Analysis Report

## Exception
- **Type**: [ExceptionType]
- **Core**: [0/1]
- **PC**: [address] → [decoded function]
- **EXCVADDR**: [address]

## Backtrace
| # | Address | Function | File:Line |
|---|---------|----------|-----------|
| 0 | 0x... | function_name | file.c:123 |

## Root Cause
[Analysis of most likely cause]

## Classification
[NULL pointer / Stack overflow / ISR violation / Memory corruption / Other]

## Recommended Fix
[Specific code change or configuration]

## Prevention
[How to prevent this class of bug in the future]
```
