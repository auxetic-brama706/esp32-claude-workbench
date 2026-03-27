# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-03-27

### Added
- **MCP Server backend (`mcp/mcp_server.py`)**: A local `FastMCP` implementation that exposes four development tools directory to Claude Code.
- **RAG for ESP32 Documentation (`scripts/index_esp_docs.py`)**: A local vector indexing and retrieval tool using FAISS, PyMuPDF, and SentenceTransformers to allow semantic offline search over ESP32 TRMs and Datasheets. 
- **Tool: `search_docs.py`**: Connects Claude to the local FAISS semantic index for querying hardware constraints directly.
- **Tool: `pin_audit.py`**: MCP tool designed to audit C/H files for dangerous GPIO combinations (Input-Only output mappings, ADC2 conflicts, Boot strapping rules).
- **Tool: `sdkconfig_check.py`**: MCP tool checking ESP-IDF `sdkconfig` files for required production-readiness flags like Watchdog timers, Panic behaviors, and buffer allocations.
- **Tool: `mission_generator.py`**: Automates generating state-tracked markdown documents for new firmware tasks via MCP.
- **Hardware Limitations Playbook**: `.claude/skills/hardware_check/SKILL.md` skill, `playbooks/hardware_limitations.md`, and default board layouts under `boards/`.
- Tests for MCP tools achieving >90% code coverage.
