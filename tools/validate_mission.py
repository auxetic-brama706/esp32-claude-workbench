"""Validate mission markdown files for required sections and structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Required top-level sections in a mission file
REQUIRED_SECTIONS: list[str] = [
    "Goal",
    "Board / Target",
    "Constraints",
    "Files in Scope",
    "Acceptance Criteria",
    "Test Plan",
    "Known Risks",
    "Current Status",
    "Next Step",
]

# Optional but recommended sections
RECOMMENDED_SECTIONS: list[str] = [
    "Design Notes",
    "History",
]


def extract_sections(content: str) -> list[str]:
    """Extract all H2 (##) section titles from markdown content.

    Args:
        content: Raw markdown text.

    Returns:
        List of section titles (without the ## prefix).
    """
    sections: list[str] = []
    for line in content.splitlines():
        match = re.match(r"^##\s+(.+)$", line.strip())
        if match:
            sections.append(match.group(1).strip())
    return sections


def validate_mission(content: str) -> dict[str, list[str]]:
    """Validate a mission file's content for required sections.

    Args:
        content: Raw markdown text of the mission file.

    Returns:
        Dict with 'missing_required', 'missing_recommended', and 'found' lists.
    """
    found_sections = extract_sections(content)
    found_lower = [s.lower() for s in found_sections]

    missing_required: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section.lower() not in found_lower:
            missing_required.append(section)

    missing_recommended: list[str] = []
    for section in RECOMMENDED_SECTIONS:
        if section.lower() not in found_lower:
            missing_recommended.append(section)

    return {
        "found": found_sections,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
    }


def validate_file(filepath: Path) -> bool:
    """Validate a mission file at the given path.

    Args:
        filepath: Path to the mission markdown file.

    Returns:
        True if all required sections are present, False otherwise.
    """
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        return False

    content = filepath.read_text(encoding="utf-8")
    result = validate_mission(content)

    print(f"\nValidating: {filepath.name}")
    print(f"  Found sections: {len(result['found'])}")

    if result["missing_required"]:
        print(f"  ❌ Missing required sections:")
        for section in result["missing_required"]:
            print(f"     - {section}")
    else:
        print(f"  ✅ All required sections present")

    if result["missing_recommended"]:
        print(f"  ⚠️  Missing recommended sections:")
        for section in result["missing_recommended"]:
            print(f"     - {section}")

    return len(result["missing_required"]) == 0


def main() -> None:
    """CLI entry point for validate-mission command."""
    if len(sys.argv) < 2:
        print("Usage: validate-mission <mission-file.md> [...]")
        print("       validate-mission missions/*.md")
        sys.exit(1)

    all_valid = True
    for arg in sys.argv[1:]:
        filepath = Path(arg)
        if not validate_file(filepath):
            all_valid = False

    if not all_valid:
        sys.exit(1)
    else:
        print("\n✅ All mission files valid.")


if __name__ == "__main__":
    main()
