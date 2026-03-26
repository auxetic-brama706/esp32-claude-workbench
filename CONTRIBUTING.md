# Contributing to ESP32 Claude Workbench

Thank you for your interest in contributing! This guide will help you get started.

## What You Can Contribute

### New Skills
Add a new Claude Code skill under `.claude/skills/`:
1. Create a directory: `.claude/skills/your_skill_name/`
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) and step-by-step instructions.
3. Follow the pattern of existing skills.
4. Add a corresponding test in `tests/` if applicable.

### New Playbooks
Add a debugging playbook under `playbooks/`:
1. Follow the existing playbook structure (Trigger, Symptoms, Triage Steps, Resolution, Prevention).
2. Keep it ESP32-specific.
3. Include real log signatures and error patterns.

### New Project Templates
Add a reusable ESP-IDF template under `templates/`:
1. Include a minimal working project with `CMakeLists.txt`, `main/`, and `sdkconfig.defaults`.
2. Add a `README.md` explaining the template's purpose.
3. Follow ESP-IDF best practices.

### Tooling Improvements
Improve or add Python tools under `tools/`:
1. Follow PEP 8 and use type hints.
2. Add corresponding tests in `tests/`.
3. Ensure the tool works without ESP32 hardware.

### Bug Fixes and Documentation
Always welcome! Please include test evidence when applicable.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-org/esp32-claude-workbench.git
cd esp32-claude-workbench

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install for development
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Pull Request Process

1. Fork the repository and create a feature branch.
2. Make your changes following the coding standards in `CLAUDE.md`.
3. Add or update tests as needed.
4. Run the full test suite: `pytest tests/ -v`
5. Update documentation if applicable.
6. Submit a PR with:
   - Clear description of the change.
   - Test evidence (command output or screenshots).
   - Any risk notes for embedded-specific changes.

## Code Style

- **Python**: PEP 8, type hints, `pathlib.Path` for files.
- **C/C++**: ESP-IDF coding style, `snake_case`, static for file-scoped functions.
- **Markdown**: ATX-style headers, consistent formatting, no trailing whitespace.

## Testing

All contributions must include tests where applicable:
- Repository tooling → `pytest` tests in `tests/`.
- New templates → validation tests for structure.
- New playbooks → integrity tests for required sections.

Run the full suite before submitting:
```bash
pytest tests/ -v --tb=short
```

## Questions?

Open an issue with the `question` label if you need help or clarification.
