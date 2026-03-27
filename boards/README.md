# ESP32 Boards Mapping

This directory contains hardware templates for popular ESP32 development boards. These templates are used by Claude to understand the exact pinout and capabilities of your specific board configuration, ensuring generated code natively respects hardware limitations.

## How to use

When starting a project, specify which board template you are using in your initial prompt to Claude.

For example: "I am using the ESP32 DevKit V1 board. Please reference its pinout when writing code."

## Adding a new board

To add a new board template, create a markdown file following the schema seen in existing files (e.g., `esp32_devkit_v1.md`), specifying:
1. LED pin(s).
2. Button pin(s), indicating active high/low.
3. Special hardware constraints or non-exposed pins.
4. Peripherals like I2C (SDA/SCL default pins) and SPI.
