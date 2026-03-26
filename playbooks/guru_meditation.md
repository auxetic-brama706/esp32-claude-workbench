# Playbook: Guru Meditation Error Review

## Trigger

ESP32 outputs a "Guru Meditation Error" in the serial log and reboots.

## Symptoms

- Serial output shows `Guru Meditation Error: Core X panic'ed`.
- Device reboot loop.
- Backtrace in serial output.
- Register dump visible.

## Triage Steps

### Step 1: Capture the Full Panic Output

Ensure you have the complete output including:
```
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.
Core  0 register dump:
PC      : 0x400d1234  PS      : 0x00060030  A0      : 0x800d5678  A1      : 0x3ffb9a10
...
EXCVADDR: 0x00000000

Backtrace: 0x400d1234:0x3ffb9a10 0x400d5678:0x3ffb9a30 ...
```

### Step 2: Identify the Exception Type

| Exception | Meaning | Common Cause |
|-----------|---------|-------------|
| `LoadProhibited` | Invalid memory read | NULL pointer dereference, use-after-free |
| `StoreProhibited` | Invalid memory write | Writing to NULL, writing to flash/ROM |
| `InstrFetchProhibited` | Invalid code execution | Corrupted function pointer, stack overflow |
| `IllegalInstruction` | Invalid opcode | Stack corruption, buffer overflow |
| `IntegerDivideByZero` | Division by zero | Unchecked divisor |
| `Unaligned` | Unaligned access | Casting to wrong pointer type |

### Step 3: Check EXCVADDR

- `0x00000000` → NULL pointer dereference (most common).
- Small value (< `0x100`) → Struct member access on NULL pointer (offset is the member offset).
- Address in stack range (`0x3FFBxxxx`) → Stack corruption.
- Address in flash range (`0x400xxxxx`) → Code corruption or bad function pointer.

### Step 4: Decode the Backtrace

```bash
# Method 1: addr2line
xtensa-esp32-elf-addr2line -pfiaC -e build/project.elf 0x400d1234 0x400d5678

# Method 2: idf.py monitor (auto-decodes)
idf.py monitor

# Method 3: ESP-IDF monitor tool
python -m esp_idf_monitor --port /dev/ttyUSB0 build/project.elf
```

The decoded backtrace shows which function called which, leading to the crash site.

### Step 5: Analyze the Call Chain

Starting from the top of the backtrace (crash site):
1. What function crashed?
2. What was it trying to access?
3. Who called it? With what arguments?
4. Is there a pattern (e.g., always crashes after Wi-Fi disconnect)?

### Step 6: Check for Known Patterns

**Pattern: Crash after `free()` or `delete`** → Use-after-free. Enable heap poisoning:
```
CONFIG_HEAP_POISONING_COMPREHENSIVE=y
```

**Pattern: Crash during ISR** → ISR calling non-ISR-safe function. Check for `xSemaphoreTake`, `vTaskDelay`, `printf` in ISR context.

**Pattern: Random crashes, different locations** → Memory corruption. Enable:
```
CONFIG_HEAP_POISONING_COMPREHENSIVE=y
CONFIG_HEAP_TASK_TRACKING=y
CONFIG_COMPILER_STACK_CHECK=y
```

**Pattern: Crash on deep function call** → Stack overflow. Enable:
```
CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK=y
```

## Resolution Checklist

- [ ] Full panic output captured.
- [ ] Exception type identified.
- [ ] Backtrace decoded to source lines.
- [ ] Root cause determined.
- [ ] Fix applied and tested.
- [ ] Diagnostic config disabled before release.

## Prevention

- Always check pointers before dereference.
- Size task stacks generously.
- Use `*FromISR` variants in interrupt handlers.
- Enable stack canaries in debug builds.
- Run with heap poisoning during development.
