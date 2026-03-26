"""Scan ESP32 C/H source files to extract GPIO pin assignments and detect conflicts.

This tool scans firmware source code for GPIO pin definitions and usage,
builds a pin allocation table, and flags:
- Reserved/forbidden pin usage (GPIO 6-11, strapping pins)
- Double-assigned pins (two peripherals on the same GPIO)
- Input-only pins used as outputs (GPIO 34-39)
- ADC2 usage in Wi-Fi projects
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PinAssignment:
    """A detected GPIO pin assignment in source code."""

    gpio: int
    purpose: str
    file: str
    line: int
    raw: str


@dataclass
class PinIssue:
    """A detected issue with pin usage."""

    severity: str  # ERROR, WARNING, INFO
    gpio: int
    message: str
    file: str
    line: int


# ESP32 reserved/restricted pins
FORBIDDEN_PINS = {6, 7, 8, 9, 10, 11}  # Internal SPI flash
STRAPPING_PINS = {0, 2, 12, 15}  # Boot strapping
UART0_PINS = {1, 3}  # Default UART0
INPUT_ONLY_PINS = {34, 35, 36, 37, 38, 39}  # No output, no pull-up/down

# ADC2 channel pins (unusable with Wi-Fi active)
ADC2_PINS = {0, 2, 4, 12, 13, 14, 15, 25, 26, 27}

# Patterns to detect GPIO usage
PATTERNS = [
    # #define PIN_NAME GPIO_NUM_XX or #define PIN_NAME XX
    re.compile(r"#define\s+(\w+)\s+GPIO_NUM_(\d+)", re.MULTILINE),
    re.compile(
        r"#define\s+(\w+(?:_PIN|_GPIO|_SDA|_SCL|_MOSI|_MISO|_CS|_CLK|_RST|_DC|_LED|_BTN|_INT))\s+(\d+)",
        re.MULTILINE,
    ),
    # gpio_config_t with pin_bit_mask
    re.compile(r"\.pin_bit_mask\s*=\s*\(\s*1ULL\s*<<\s*(\d+)\s*\)", re.MULTILINE),
    # gpio_set_direction(GPIO_NUM_XX, ...)
    re.compile(r"gpio_set_direction\s*\(\s*GPIO_NUM_(\d+)", re.MULTILINE),
    # gpio_set_level(GPIO_NUM_XX, ...)
    re.compile(r"gpio_set_level\s*\(\s*GPIO_NUM_(\d+)", re.MULTILINE),
    # i2c_config .sda_io_num = XX
    re.compile(r"\.(sda_io_num|scl_io_num)\s*=\s*(\d+)", re.MULTILINE),
    # spi_bus_config_t fields
    re.compile(r"\.(mosi_io_num|miso_io_num|sclk_io_num)\s*=\s*(\d+)", re.MULTILINE),
    # UART tx_io_num / rx_io_num
    re.compile(r"\.(tx_io_num|rx_io_num|rts_io_num|cts_io_num)\s*=\s*(\d+)", re.MULTILINE),
    # LEDC output_io_num
    re.compile(r"\.output_io_num\s*=\s*(\d+)", re.MULTILINE),
]

# Wi-Fi usage indicators
WIFI_INDICATORS = [
    re.compile(r"#include\s*[\"<]esp_wifi\.h[\">]"),
    re.compile(r"esp_wifi_init"),
    re.compile(r"WIFI_MODE_STA|WIFI_MODE_AP|WIFI_MODE_APSTA"),
]


def scan_file(filepath: Path) -> list[PinAssignment]:
    """Scan a single C/H file for GPIO pin assignments.

    Args:
        filepath: Path to the source file.

    Returns:
        List of detected PinAssignment objects.
    """
    assignments: list[PinAssignment] = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return assignments

    lines = content.splitlines()

    for pattern in PATTERNS:
        for match in pattern.finditer(content):
            # Find line number
            pos = match.start()
            line_num = content[:pos].count("\n") + 1

            groups = match.groups()

            if len(groups) == 2:
                purpose = groups[0]
                try:
                    gpio = int(groups[1])
                except ValueError:
                    continue
            elif len(groups) == 1:
                try:
                    gpio = int(groups[0])
                except ValueError:
                    continue
                purpose = "gpio_usage"
            else:
                continue

            # Clamp to valid range
            if gpio < 0 or gpio > 39:
                continue

            raw_line = lines[line_num - 1].strip() if line_num <= len(lines) else ""

            assignments.append(
                PinAssignment(
                    gpio=gpio,
                    purpose=purpose,
                    file=str(filepath),
                    line=line_num,
                    raw=raw_line,
                )
            )

    return assignments


def detect_wifi_usage(directory: Path) -> bool:
    """Check if the project uses Wi-Fi.

    Args:
        directory: Project root directory.

    Returns:
        True if Wi-Fi usage is detected.
    """
    for filepath in directory.rglob("*.[ch]"):
        if "build" in filepath.parts or ".venv" in filepath.parts:
            continue
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in WIFI_INDICATORS:
            if pattern.search(content):
                return True
    return False


def analyze_pins(assignments: list[PinAssignment], uses_wifi: bool = False) -> list[PinIssue]:
    """Analyze pin assignments for issues.

    Args:
        assignments: List of detected pin assignments.
        uses_wifi: Whether the project uses Wi-Fi.

    Returns:
        List of PinIssue objects.
    """
    issues: list[PinIssue] = []
    pin_users: dict[int, list[PinAssignment]] = defaultdict(list)

    for a in assignments:
        pin_users[a.gpio].append(a)

    for gpio, users in pin_users.items():
        first = users[0]

        # Check forbidden pins
        if gpio in FORBIDDEN_PINS:
            issues.append(
                PinIssue(
                    severity="ERROR",
                    gpio=gpio,
                    message=f"GPIO {gpio} is connected to internal SPI flash — NEVER use this pin",
                    file=first.file,
                    line=first.line,
                )
            )

        # Check strapping pins
        if gpio in STRAPPING_PINS:
            issues.append(
                PinIssue(
                    severity="WARNING",
                    gpio=gpio,
                    message=f"GPIO {gpio} is a boot strapping pin — may affect boot if externally driven",
                    file=first.file,
                    line=first.line,
                )
            )

        # Check UART0 pins
        if gpio in UART0_PINS:
            issues.append(
                PinIssue(
                    severity="WARNING",
                    gpio=gpio,
                    message=f"GPIO {gpio} is default UART0 {'TX' if gpio == 1 else 'RX'} — using it will disable serial output",
                    file=first.file,
                    line=first.line,
                )
            )

        # Check input-only pins used for output-sounding purposes
        if gpio in INPUT_ONLY_PINS:
            output_keywords = {
                "LED",
                "MOSI",
                "SDA",
                "SCL",
                "TX",
                "CS",
                "RST",
                "DC",
                "CLK",
                "output",
            }
            for user in users:
                if any(kw.lower() in user.purpose.lower() for kw in output_keywords):
                    issues.append(
                        PinIssue(
                            severity="ERROR",
                            gpio=gpio,
                            message=f"GPIO {gpio} is input-only but assigned to output function '{user.purpose}'",
                            file=user.file,
                            line=user.line,
                        )
                    )

        # Check ADC2 with Wi-Fi
        if uses_wifi and gpio in ADC2_PINS:
            for user in users:
                if "adc" in user.purpose.lower():
                    issues.append(
                        PinIssue(
                            severity="ERROR",
                            gpio=gpio,
                            message=f"GPIO {gpio} is ADC2 — cannot be used while Wi-Fi is active",
                            file=user.file,
                            line=user.line,
                        )
                    )

        # Check double assignment
        if len(users) > 1:
            # Deduplicate by purpose
            unique_purposes = {u.purpose for u in users}
            if len(unique_purposes) > 1:
                purpose_list = ", ".join(sorted(unique_purposes))
                issues.append(
                    PinIssue(
                        severity="ERROR",
                        gpio=gpio,
                        message=f"GPIO {gpio} is assigned to multiple functions: {purpose_list}",
                        file=first.file,
                        line=first.line,
                    )
                )

    return sorted(issues, key=lambda i: (0 if i.severity == "ERROR" else 1, i.gpio))


def format_report(
    assignments: list[PinAssignment],
    issues: list[PinIssue],
    uses_wifi: bool,
) -> str:
    """Format pin scan results as a markdown report.

    Args:
        assignments: All detected pin assignments.
        issues: All detected issues.
        uses_wifi: Whether Wi-Fi is used.

    Returns:
        Formatted markdown string.
    """
    lines: list[str] = []
    lines.append("# Pin Scan Report")
    lines.append("")

    # Summary
    error_count = sum(1 for i in issues if i.severity == "ERROR")
    warning_count = sum(1 for i in issues if i.severity == "WARNING")
    lines.append("## Summary")
    lines.append(f"- **Pins detected**: {len(set(a.gpio for a in assignments))}")
    lines.append(f"- **Assignments**: {len(assignments)}")
    lines.append(f"- **Errors**: {error_count}")
    lines.append(f"- **Warnings**: {warning_count}")
    lines.append(f"- **Wi-Fi detected**: {'Yes' if uses_wifi else 'No'}")
    lines.append("")

    # Pin allocation table
    pin_map: dict[int, list[PinAssignment]] = defaultdict(list)
    for a in assignments:
        pin_map[a.gpio].append(a)

    if pin_map:
        lines.append("## Pin Allocation Table")
        lines.append("")
        lines.append("| GPIO | Purpose | File | Line |")
        lines.append("|------|---------|------|------|")
        for gpio in sorted(pin_map):
            for a in pin_map[gpio]:
                short_file = Path(a.file).name
                lines.append(f"| {gpio} | `{a.purpose}` | {short_file} | {a.line} |")
        lines.append("")

    # Issues
    if issues:
        lines.append("## Issues")
        lines.append("")
        for issue in issues:
            icon = "❌" if issue.severity == "ERROR" else "⚠️"
            short_file = Path(issue.file).name
            lines.append(f"- {icon} **{issue.severity}** GPIO {issue.gpio}: {issue.message}")
            lines.append(f"  - File: `{short_file}:{issue.line}`")
        lines.append("")
    else:
        lines.append("## ✅ No Issues Found")
        lines.append("")

    return "\n".join(lines)


def scan_directory(directory: Path) -> tuple[list[PinAssignment], list[PinIssue], bool]:
    """Scan all C/H files in a directory tree.

    Args:
        directory: Root directory to scan.

    Returns:
        Tuple of (assignments, issues, uses_wifi).
    """
    all_assignments: list[PinAssignment] = []

    for filepath in directory.rglob("*.[ch]"):
        # Skip build directories
        if "build" in filepath.parts or ".venv" in filepath.parts:
            continue
        all_assignments.extend(scan_file(filepath))

    uses_wifi = detect_wifi_usage(directory)
    issues = analyze_pins(all_assignments, uses_wifi)

    return all_assignments, issues, uses_wifi


def main() -> None:
    """CLI entry point for pin scanner."""
    if len(sys.argv) < 2:
        print("Usage: scan-pins <project-directory>")
        print("       scan-pins ./main/")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"ERROR: Not a directory: {directory}")
        sys.exit(1)

    assignments, issues, uses_wifi = scan_directory(directory)
    print(format_report(assignments, issues, uses_wifi))

    error_count = sum(1 for i in issues if i.severity == "ERROR")
    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
