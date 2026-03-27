"""
Tool for auditing ESP-IDF sdkconfig files for production readiness.
"""

import os
import re

def run_sdkconfig_check(sdkconfig_path: str) -> str:
    """Check a raw sdkconfig file (key=value format) for production readiness."""
    if not os.path.exists(sdkconfig_path):
        return f"Error: sdkconfig file '{sdkconfig_path}' not found."

    try:
        with open(sdkconfig_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return f"Error reading sdkconfig '{sdkconfig_path}': {e}"
        
    config = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            # Some lines are like "# CONFIG_XXX is not set"
            match = re.search(r'#\s*(CONFIG_[A-Z0-9_]+)\s+is not set', line)
            if match:
                config[match.group(1)] = "n"
            continue
            
        parts = line.split('=', 1)
        if len(parts) == 2:
            config[parts[0]] = parts[1].strip('"')

    report = []
    
    # Check Panic mode
    if config.get("CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT") == "y":
        report.append("[PASS] System Panic Mode is Print+Reboot.")
    elif config.get("CONFIG_ESP_SYSTEM_PANIC_SILENT_REBOOT") == "y":
        report.append("[FAIL] System Panic Mode is SILENT reboot. This is bad for production diagnostics.")
    else:
        report.append("[WARN] Panic mode not explicitly set to Print+Reboot.")

    # Bootloader Log Level
    bl_level = config.get("CONFIG_BOOTLOADER_LOG_LEVEL")
    if bl_level in ["5", "4"]: # VERBOSE=5, DEBUG=4
        report.append("[FAIL] Bootloader log level is high (Debug/Verbose), delaying boot time and risking security leaks.")
    else:
        report.append("[PASS] Bootloader log level is reasonable.")

    # Task WDT
    if config.get("CONFIG_ESP_TASK_WDT_EN") == "y" or config.get("CONFIG_ESP_TASK_WDT") == "y":
        report.append("[PASS] Task Watchdog Timer is enabled.")
    else:
        report.append("[WARN] Task Watchdog Timer is disabled. Hangs won't auto-reboot the device.")

    # Core Dump
    if config.get("CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH") == "y":
        report.append("[PASS] Core dump to flash enabled.")
    else:
        report.append("[WARN] Core dump to flash disabled. Post-mortem crash analysis will be difficult.")

    # Certificates
    if config.get("CONFIG_MBEDTLS_CERTIFICATE_BUNDLE_DEFAULT_FULL") == "y":
        report.append("[PASS] Full MBEDTLS root cert bundle enabled for HTTPS.")
    else:
        report.append("[INFO] MBEDTLS full cert bundle missing. May need custom certs for HTTPS.")

    # WiFi buffers
    wifi_rx = config.get("CONFIG_ESP_WIFI_STATIC_RX_BUFFER_NUM")
    try:
        if wifi_rx and int(wifi_rx) >= 10:
            report.append(f"[PASS] Wi-Fi static RX buffer is robust ({wifi_rx}).")
        elif wifi_rx:
            report.append(f"[WARN] Wi-Fi static RX buffer is low ({wifi_rx}). Recommended >= 10 for stability.")
    except ValueError:
        pass

    # FreeRTOS Tick Rate
    hz = config.get("CONFIG_FREERTOS_HZ")
    if hz == "1000":
        report.append("[PASS] FreeRTOS tick rate is 1000 Hz, responsive tasks.")
    else:
        report.append(f"[WARN] FreeRTOS tick rate is {hz} Hz. Recommend 1000 Hz for latency-sensitive apps.")

    # Compiler Optimization
    if config.get("CONFIG_COMPILER_OPTIMIZATION_LEVEL_DEBUG") == "y":
        report.append("[FAIL] Compiler optimization is set to DEBUG (-Og). Should be RELEASE (-O2 / -Os) for production.")
    else:
        report.append("[PASS] Compiler Optimization is not DEBUG mode.")

    return "=== SDKCONFIG AUDIT ===\n\n" + "\n".join(report)
