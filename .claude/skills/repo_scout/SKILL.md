---
name: repo_scout
description: Scan and understand an ESP-IDF project structure, identifying components, dependencies, and architecture patterns.
---

# Repo Scout

Scan an ESP-IDF project to understand its structure, components, and patterns before making changes.

## When to Use

- Starting work on an unfamiliar project.
- Before writing an implementation contract.
- When you need to understand dependencies between components.

## Steps

### 1. Identify Project Type

Determine the build system:
- Check for `CMakeLists.txt` at root → ESP-IDF CMake project
- Check for `platformio.ini` → PlatformIO project
- Check for `Makefile` with `PROJECT_NAME` → Legacy ESP-IDF Make project

### 2. Map the Component Structure

```
find . -name "CMakeLists.txt" -not -path "./build/*" | head -20
find . -name "component.mk" -not -path "./build/*" | head -20
```

For each component directory, note:
- Component name
- Public headers (in `include/`)
- Dependencies (from `CMakeLists.txt` `REQUIRES` and `PRIV_REQUIRES`)
- Whether it has tests (check for `test/` subdirectory)

### 3. Identify Hardware Configuration

Look for:
- `sdkconfig.defaults` — default Kconfig settings
- `sdkconfig` — current build configuration
- Pin definitions — search for `GPIO_NUM_`, `#define.*PIN`, `#define.*GPIO`
- Peripheral usage — search for `i2c_`, `spi_`, `uart_`, `ledc_`, `adc_`, `wifi_`, `ble_`

### 4. Map Task Architecture

Search for FreeRTOS task creation:
```
grep -rn "xTaskCreate\|xTaskCreatePinnedToCore" --include="*.c" --include="*.h"
```

Document:
- Task names
- Stack sizes
- Priorities
- Core affinity (if pinned)

### 5. Identify External Dependencies

Check:
- `idf_component.yml` — ESP Component Registry dependencies
- `managed_components/` — downloaded components
- Git submodules — `.gitmodules`
- Direct source vendoring — `third_party/` or `lib/`

### 6. Generate Scout Report

Produce a summary with:
- **Project type**: ESP-IDF version, build system
- **Components**: list with brief purpose
- **Hardware dependencies**: pins, peripherals, communication protocols
- **Task map**: FreeRTOS tasks with parameters
- **External dependencies**: libraries and components
- **Test coverage**: which components have tests
- **Risks**: anything unusual or potentially problematic

## Output Format

Write the scout report to the active mission file or print it in a structured markdown block.
