# Playbook: Build Failure Triage

## Trigger

ESP-IDF project fails to compile (`idf.py build` or `cmake --build`).

## Symptoms

- Build errors in terminal output.
- Linker errors.
- Component registration failures.
- Missing header files.

## Triage Steps

### Step 1: Identify Error Type

| Error Pattern | Category | Likely Cause |
|--------------|----------|-------------|
| `fatal error: xyz.h: No such file` | Include path | Missing component dependency or wrong include path |
| `undefined reference to` | Linker | Missing source file, missing component REQUIRES |
| `error: unknown type name` | Type | Missing include or wrong target configuration |
| `error: 'CONFIG_XYZ' undeclared` | Kconfig | Missing Kconfig option or sdkconfig mismatch |
| `CMake Error: Cannot find component` | CMake | Component not registered or wrong directory |
| `multiple definition of` | Linker | Duplicate symbol — same function defined twice |
| `error: static assertion failed` | Config | ESP-IDF version or target mismatch |

### Step 2: Check Target Configuration

```bash
# Verify target matches your board
idf.py set-target esp32  # or esp32s2, esp32s3, esp32c3, etc.

# Clean and rebuild after target change
idf.py fullclean
idf.py build
```

### Step 3: Check Component Dependencies

In each component's `CMakeLists.txt`:
```cmake
idf_component_register(
    SRCS "source.c"
    INCLUDE_DIRS "include"
    REQUIRES driver esp_wifi       # Public dependencies
    PRIV_REQUIRES esp_timer nvs_flash  # Private dependencies
)
```

Common missing dependencies:
- `driver` — for GPIO, I2C, SPI, UART, LEDC
- `esp_wifi` — for Wi-Fi features
- `esp_event` — for event loop
- `nvs_flash` — for NVS storage
- `esp_http_client` — for HTTP
- `mqtt` — for MQTT

### Step 4: Check sdkconfig

```bash
# Compare with defaults
diff sdkconfig sdkconfig.defaults

# Reset to defaults
rm sdkconfig
idf.py build
```

Common sdkconfig issues:
- Wrong partition table for the flash size.
- Feature not enabled (e.g., BLE, OTA, HTTPS).
- Wrong CPU frequency setting.
- Incompatible options for the target chip.

### Step 5: Clean Build

```bash
# Standard clean
idf.py fullclean
idf.py build

# Nuclear option — remove build directory
rm -rf build/
idf.py build
```

### Step 6: Check ESP-IDF Version

```bash
# Check version
idf.py --version

# Check for API changes in ESP-IDF release notes
# Common breaking changes between v4.x and v5.x:
# - GPIO driver API changed
# - ADC API completely reworked
# - I2C API updated
# - Wi-Fi init simplified
```

## Resolution Checklist

- [ ] Error type identified and categorized.
- [ ] Root cause found.
- [ ] Fix applied.
- [ ] Clean build succeeds.
- [ ] No new warnings introduced.

## Prevention

- Always declare component dependencies explicitly in `CMakeLists.txt`.
- Use `sdkconfig.defaults` to track all non-default configuration.
- Pin the ESP-IDF version in your project documentation.
- Run clean builds in CI.
