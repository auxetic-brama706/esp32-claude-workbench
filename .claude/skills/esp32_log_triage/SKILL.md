---
name: esp32_log_triage
description: Parse and classify ESP32 serial log output to identify errors, warnings, boot issues, and failure patterns.
---

# ESP32 Log Triage

Systematically analyze ESP32 serial log output to identify and classify issues.

## When to Use

- Debugging unexpected device behavior.
- Analyzing boot failures.
- Reviewing log output after a test run.
- Triaging field-reported issues from log captures.

## Steps

### 1. Identify Log Structure

ESP-IDF log format:
```
[LEVEL][TAG] (TIMESTAMP) MESSAGE
```

Levels (severity order):
- `E` — Error (critical failures)
- `W` — Warning (potential issues)
- `I` — Info (normal operation)
- `D` — Debug (detailed tracing)
- `V` — Verbose (maximum detail)

### 2. Extract Critical Events

Search for these high-priority patterns:

#### Boot Failures
```
rst:0x1 (POWERON_RESET)          → Normal power-on
rst:0x3 (SW_RESET)               → Software reset
rst:0x7 (TG0WDT_SYS_RESET)      → Task watchdog reset
rst:0x8 (TG1WDT_SYS_RESET)      → Interrupt watchdog reset
rst:0xf (BROWNOUT_RESET)         → Power supply issue
```

#### Crash Signatures
```
Guru Meditation Error             → CPU exception
LoadProhibited                    → NULL pointer or invalid memory read
StoreProhibited                   → Write to invalid memory
InstrFetchProhibited              → Jump to invalid address
IllegalInstruction                → Corrupt code or stack
abort()                           → Software abort
Stack overflow                    → Task stack too small
```

#### Memory Issues
```
MALLOC_FAILURE                    → Heap exhaustion
heap_caps_alloc failed            → Specific heap type exhausted
heap corruption detected          → Memory corruption
```

#### Network Issues
```
wifi:state:                       → Wi-Fi state transitions
esp_netif_lwip: Failed            → Network interface errors
TRANSPORT_BASE: Failed            → Connection failures
MQTT_CLIENT: Error                → MQTT protocol errors
```

### 3. Classify the Issue

Categorize the primary issue:

| Category | Indicators |
|----------|-----------|
| Boot loop | Repeated reset reasons, never reaches `app_main` |
| Crash | Guru Meditation, backtrace present |
| Memory | Allocation failures, usage growing over time |
| Watchdog | TG0WDT/TG1WDT reset reasons |
| Network | Connection failures, timeouts, drops |
| Peripheral | I2C/SPI/UART errors, timeout on bus |
| Power | Brownout resets, unstable ADC readings |

### 4. Extract Backtrace

If a crash backtrace is present:
```
Backtrace: 0x400d1234:0x3ffb5678 0x400d2345:0x3ffb6789
```

Decode with:
```bash
xtensa-esp32-elf-addr2line -pfiaC -e build/project.elf 0x400d1234 0x400d2345
```

### 5. Generate Triage Report

```markdown
# Log Triage Report

## Summary
- **Issue type**: [Boot loop / Crash / Memory / Watchdog / Network / Peripheral / Power]
- **Severity**: [CRITICAL / HIGH / MEDIUM / LOW]
- **Reset reason**: [From boot log]

## Key Events (chronological)
1. [timestamp] [event description]
2. [timestamp] [event description]

## Error Patterns
- [Pattern]: [count] occurrences — [interpretation]

## Root Cause Hypothesis
[Most likely cause based on evidence]

## Recommended Next Steps
1. [Action]
2. [Action]

## Raw Evidence
[Relevant log excerpts]
```

## Tips

- **Brownout resets** usually indicate insufficient power supply, not code bugs.
- **Watchdog resets during Wi-Fi** often mean a task is blocking the system task.
- **Guru Meditation with address 0x00000000** is almost always a NULL pointer dereference.
- **Repeated MQTT disconnects** — check keepalive interval vs. network latency.
