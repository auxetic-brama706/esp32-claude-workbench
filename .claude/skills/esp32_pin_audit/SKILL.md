---
name: esp32_pin_audit
description: Audit ESP32 GPIO usage for conflicts, reserved pin violations, and documentation drift.
---

# ESP32 Pin Audit

Systematically audit GPIO pin usage across the project to detect conflicts, reserved pin misuse, and undocumented assignments.

## When to Use

- Before adding new peripheral code.
- During architecture review.
- When debugging mysterious hardware behavior.
- Before release.

## Steps

### 1. Collect All Pin Declarations

Search the project for pin definitions:

```bash
# Macro definitions
grep -rn "#define.*GPIO\|#define.*PIN\|#define.*SDA\|#define.*SCL\|#define.*MOSI\|#define.*MISO\|#define.*CS\|#define.*CLK" --include="*.h" --include="*.c"

# GPIO_NUM usage
grep -rn "GPIO_NUM_" --include="*.c" --include="*.h"

# Kconfig GPIO options
grep -rn "CONFIG_.*GPIO\|CONFIG_.*PIN" sdkconfig.defaults sdkconfig 2>/dev/null
```

### 2. Check Reserved Pins

Flag violations against these reserved pins:

| GPIO | Restriction | Reason |
|------|-------------|--------|
| 0 | Boot strapping | Must be HIGH for normal boot, LOW for download |
| 1 | UART0 TX | Default serial output |
| 2 | Boot strapping | Must be LOW during flash |
| 3 | UART0 RX | Default serial input |
| 6–11 | **FORBIDDEN** | Connected to internal SPI flash |
| 12 | Boot strapping | MTDI — affects flash voltage |
| 15 | Boot strapping | MTDO — affects debug output |
| 34–39 | Input-only | No output capability, no pull-up/pull-down |

### 3. Detect Conflicts

Build a pin allocation table and check for:
- **Double assignment**: Same GPIO used by two different peripherals.
- **Bus conflicts**: I2C and SPI sharing the same pins.
- **ADC/DAC conflicts**: ADC2 channels unusable when Wi-Fi is active.
- **Strapping conflicts**: Boot pins used without awareness.

### 4. Verify Pull-Up/Pull-Down Configuration

For I2C lines:
- External pull-ups are required. Internal pull-ups are too weak for reliable I2C.
- Flag if only internal pull-ups are configured for I2C.

For inputs with no external circuitry:
- Verify pull-up or pull-down is configured to avoid floating pins.

### 5. Check Documentation

Compare actual code pin usage against:
- Pin map comments in source files.
- README or documentation references.
- Schematic references if available.

Flag any drift between documented and actual usage.

### 6. Generate Audit Report

```markdown
# Pin Audit Report

## Pin Allocation Table
| GPIO | Function | Component | Direction | Pull | Notes |
|------|----------|-----------|-----------|------|-------|

## Violations
- [ ] [Description of violation]

## Conflicts
- [ ] [Description of conflict]

## Warnings
- [ ] [Potential issues to investigate]

## Documentation Drift
- [ ] [Documented vs. actual usage]
```

## ADC2 Wi-Fi Warning

**Critical**: ADC2 channels (GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, 27) cannot be used while Wi-Fi is active. Always flag ADC2 usage in Wi-Fi-enabled projects.
