"""
Tool for auditing ESP32 GPIO pin usage in C/H files.
"""

import os
import re

# Hard rules
INPUT_ONLY_PINS = {34, 35, 36, 37, 38, 39}
BOOTSTRAP_PINS = {0, 2, 5, 12, 15}
ADC2_PINS = {0, 2, 4, 12, 13, 14, 15, 25, 26, 27}
FLASH_PINS = {6, 7, 8, 9, 10, 11}

def run_pin_audit(header_path: str) -> str:
    """
    Parse a C header file (.h) or source file (.c) for GPIO definitions and usages.
    Check against ESP32 hardware rules and return a structured report.
    """
    if not os.path.exists(header_path):
        return f"Error: File '{header_path}' not found."

    try:
        with open(header_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return f"Error reading file '{header_path}': {e}"

    results = []
    has_wifi_init = False
    
    # Check for Wi-Fi init broadly first
    for line in lines:
        if "esp_wifi_init" in line or "wifi_init_config_t" in line:
            has_wifi_init = True
            break
            
    # Regex formats to match GPIO configurations and usages
    # e.g., #define MY_LED GPIO_NUM_34
    # e.g., gpio_set_direction(GPIO_NUM_34, GPIO_MODE_OUTPUT)
    
    gpio_num_pattern = re.compile(r'GPIO_NUM_(\d+)')
    io_def_pattern = re.compile(r'(\d+)')

    for idx, line in enumerate(lines, start=1):
        line_clean = line.strip()
        # Skip comments (basic handling)
        if line_clean.startswith('//'):
            continue
            
        # Find raw numbers that might be GPIOs in set_direction
        matched_gpios = set()
        
        # Check standard GPIO_NUM_XX
        for match in gpio_num_pattern.finditer(line):
            matched_gpios.add(int(match.group(1)))
            
        if "gpio_set_direction" in line:
            # simple extract
            parts = line.split(',')
            if len(parts) >= 2:
                # check if there's a raw number in the first part
                m = io_def_pattern.search(parts[0])
                if m:
                    matched_gpios.add(int(m.group(1)))
                    
        for pin in matched_gpios:
            # Check flash pins
            if pin in FLASH_PINS:
                results.append(f"[CRITICAL] Line {idx}: GPIO {pin} is connected to internal flash. Using it will likely crash the ESP32.")
                
            # Check input only pins
            if pin in INPUT_ONLY_PINS:
                if "OUTPUT" in line.upper() or "gpio_set_direction" in line and "OUTPUT" in line.upper():
                    results.append(f"[CRITICAL] Line {idx}: GPIO {pin} is INPUT ONLY, but used as OUTPUT.")
                else:
                    results.append(f"[INFO] Line {idx}: GPIO {pin} used safely (input only).")
            
            # Check bootstrap pins
            if pin in BOOTSTRAP_PINS:
                results.append(f"[WARNING] Line {idx}: GPIO {pin} is a bootstrap pin. Ensure external hardware does not pull this to the wrong state during boot.")
                
            # Check ADC2 conflict
            if pin in ADC2_PINS and has_wifi_init:
                if "adc" in line.lower() or "analog" in line.lower():
                    results.append(f"[CRITICAL] Line {idx}: GPIO {pin} (ADC2) cannot be used while Wi-Fi is enabled. Switch to ADC1.")

    if not results:
        return "=== PIN AUDIT ===\n\nResult: [INFO] No obvious GPIO conflicts or misuse detected based on static analysis."

    return "=== PIN AUDIT ===\n\n" + "\n".join(results)
