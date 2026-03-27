# ESP32 DevKit V1

**Microcontroller:** ESP32-WROOM-32
**Core:** Xtensa Dual-Core 32-bit LX6

## Overview

The standard 30-pin or 38-pin development board for ESP32. Most tutorials and examples default to this pinout.

## Typical Pinout

- **Built-in LED:** GPIO 2 (Active HIGH)
- **Built-in Button:** GPIO 0 (BOOT button, Active LOW, pull-up required if used in application)
- **Default I2C:** SDA = 21, SCL = 22
- **Default HSPI:** MISO = 12, MOSI = 13, SCK = 14, CS = 15
- **Default VSPI:** MISO = 19, MOSI = 23, SCK = 18, CS = 5
- **UART (TX/RX):** TX = 1, RX = 3 (used for flashing/console, avoid in application code unless necessary)

## Limitations

- Pins 34, 35, 36 (VP), 39 (VN) are **INPUT ONLY**. They cannot drive LEDs or logic outputs.
- ADC2 cannot be used when Wi-Fi is active (Pins: 4, 0, 2, 15, 13, 12, 14, 27, 25, 26).
- Strapping pins (0, 2, 5, 12, 15) must be carefully planned if used at boot time.
