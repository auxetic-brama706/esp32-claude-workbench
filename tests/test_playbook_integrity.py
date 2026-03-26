"""Tests for playbook file integrity and structure."""

from pathlib import Path

import pytest

# Path to the project root
ROOT = Path(__file__).parent.parent

# Expected playbook files
EXPECTED_PLAYBOOKS = [
    "build_failure.md",
    "guru_meditation.md",
    "wifi_debug.md",
    "i2c_bringup.md",
    "watchdog_reset.md",
    "memory_review.md",
    "ota_update.md",
    "ble_debug.md",
    "spi_bringup.md",
]

# Required sections in every playbook
REQUIRED_PLAYBOOK_SECTIONS = [
    "Trigger",
    "Symptoms",
    "Triage Steps",
    "Resolution Checklist",
    "Prevention",
]


def extract_h2_sections(content: str) -> list[str]:
    """Extract H2 section titles from markdown."""
    import re
    return [
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+)$", content, re.MULTILINE)
    ]


class TestPlaybookFilesExist:
    """Test that all expected playbook files exist."""

    @pytest.mark.parametrize("filename", EXPECTED_PLAYBOOKS)
    def test_playbook_exists(self, filename: str):
        playbook_path = ROOT / "playbooks" / filename
        assert playbook_path.exists(), f"Playbook not found: {playbook_path}"

    @pytest.mark.parametrize("filename", EXPECTED_PLAYBOOKS)
    def test_playbook_is_not_empty(self, filename: str):
        playbook_path = ROOT / "playbooks" / filename
        content = playbook_path.read_text(encoding="utf-8")
        assert len(content.strip()) > 100, f"Playbook {filename} appears to be empty or too short"


class TestPlaybookStructure:
    """Test that playbooks have required structure."""

    @pytest.mark.parametrize("filename", EXPECTED_PLAYBOOKS)
    def test_playbook_has_title(self, filename: str):
        playbook_path = ROOT / "playbooks" / filename
        content = playbook_path.read_text(encoding="utf-8")
        assert content.strip().startswith("# "), f"Playbook {filename} should start with an H1 title"

    @pytest.mark.parametrize("filename", EXPECTED_PLAYBOOKS)
    def test_playbook_has_required_sections(self, filename: str):
        playbook_path = ROOT / "playbooks" / filename
        content = playbook_path.read_text(encoding="utf-8")
        found_sections = extract_h2_sections(content)
        found_lower = [s.lower() for s in found_sections]

        for required in REQUIRED_PLAYBOOK_SECTIONS:
            assert required.lower() in found_lower, (
                f"Playbook {filename} missing required section: '{required}'. "
                f"Found sections: {found_sections}"
            )


class TestPlaybookContent:
    """Test playbook content quality."""

    @pytest.mark.parametrize("filename", EXPECTED_PLAYBOOKS)
    def test_playbook_has_checklist(self, filename: str):
        """Playbooks should have at least one checklist item."""
        playbook_path = ROOT / "playbooks" / filename
        content = playbook_path.read_text(encoding="utf-8")
        assert "- [ ]" in content, (
            f"Playbook {filename} should contain at least one checklist item"
        )

    @pytest.mark.parametrize("filename", EXPECTED_PLAYBOOKS)
    def test_playbook_minimum_length(self, filename: str):
        """Playbooks should have substantial content."""
        playbook_path = ROOT / "playbooks" / filename
        content = playbook_path.read_text(encoding="utf-8")
        lines = [line for line in content.splitlines() if line.strip()]
        assert len(lines) >= 20, (
            f"Playbook {filename} has only {len(lines)} non-empty lines, expected >= 20"
        )
