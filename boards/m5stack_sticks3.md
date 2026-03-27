# M5Stack StickC Plus2 / StickS3 (ESP32-S3 Variant)

**Microcontroller:** ESP32-S3
**Core:** Xtensa Dual-Core 32-bit LX7

## Overview

A highly integrated development board with a built-in LCD, IMU, microphone, and buttons. 

## Typical Pinout

- **Built-in LED:** GPIO 19 (Check specific revision; sometimes active LOW)
- **Built-in Buttons:** 
  - Button A (Front): GPIO 37
  - Button B (Side): GPIO 39
- **I2C (Internal):** SDA = 21, SCL = 22 (Used for IMU, RTC, Power Management)
- **I2C (External Grove):** SDA = 32, SCL = 33
- **TFT Display (SPI):** MOSI = 15, SCLK = 13, CS = 5, DC = 14, RST = On-board AXP power chip
- **Microphone (I2S):** DAT = 14, BCLK = 0 (SPM1423)

## Limitations

- The internal I2C bus is critical for the AXP192/AXP2101 power management chip. You must initialize it properly or the device will turn off.
- Many pins are dedicated to internal features and shouldn't be overridden in application logic.
- The S3 module operates differently from the standard ESP32 in terms of USB routing (Native USB vs CDC). Pay attention when defining serial outputs.
