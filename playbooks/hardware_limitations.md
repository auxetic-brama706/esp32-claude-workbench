# Playbook: ESP32 Hardware Limitations

## Trigger

When starting a new ESP32 project, selecting pins for peripherals, or diagnosing issues related to physical I/O.

## Symptoms

- Code works but physical hardware behaves erratically (e.g., cannot flash, randomly enters bootloader mode).
- ADC reads fail when Wi-Fi is active.
- Pins cannot act as outputs.
- Debugging features (like JTAG) are unavailable or conflicting with other peripherals.

## Triage Steps & Limitations

### 1. Input-Only Pins (Pins 34-39)
- **Pins:** GPIO 34, 35, 36 (VP), 39 (VN).
- **Limitation:** These pins do not have internal pull-up or pull-down resistors and **cannot be configured as outputs**. They are input-only.
- **Action:** Only use for input signals (e.g., buttons with external pull resistors, ADC inputs).

### 2. Strapping Pins
- **Pins:** GPIO 0, 2, 5, 12, 15.
- **Limitation:** The logic level on these pins at boot time determines the boot mode (e.g., flashing mode vs. normal execution).
- **Action:** 
  - Avoid connecting components that might pull these pins to unintended logic levels during boot.
  - GPIO 0: Must be HIGH for normal boot.
  - GPIO 2: Must be left floating or tied LOW during boot.
  - GPIO 12: Determines flash voltage (MTDI). Careful using this pin as it may cause boot failures.

### 3. ADC2 / Wi-Fi Conflict
- **Pins:** GPIO 4, 0, 2, 15, 13, 12, 14, 27, 25, 26 (ADC2 channel pins).
- **Limitation:** The ADC2 peripheral is shared with the Wi-Fi driver. If Wi-Fi is turned on, reading from ADC2 will fail.
- **Action:** Use ADC1 (Pins 36, 37, 38, 39, 32, 33, 34, 35) for analog readings when Wi-Fi is required.

### 4. JTAG Debugging Pins
- **Pins:** GPIO 12, 13, 14, 15.
- **Limitation:** These overlap with the JTAG interface. If you are using hardware debugging via JTAG, these pins are reserved.
- **Action:** Leave them disconnected from other peripherals if JTAG debugging is active.

## Resolution Checklist

- [ ] All output requirements are kept away from pins 34-39.
- [ ] Strapping pins are kept floating or in their safe boot states.
- [ ] Analog sensors avoid ADC2 if Wi-Fi is used.
- [ ] JTAG pins are unused by application code when hardware debugging is required.
