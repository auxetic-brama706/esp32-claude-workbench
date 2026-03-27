"""
Tool for creating structured ESP32 mission files.
"""

import os
from datetime import datetime

def generate_mission(feature_name: str, board: str, description: str) -> str:
    """Create a structured mission markdown file for a new ESP32 firmware task."""
    # Sanitize feature name to snake_case
    sanitized_name = feature_name.lower().replace(" ", "_").replace("-", "_")
    sanitized_name = "".join([c for c in sanitized_name if c.isalnum() or c == "_"])
    
    date_str_iso = datetime.now().strftime("%Y-%m-%d")
    
    filename = f"{date_str_iso}-{sanitized_name}.md"
    
    # Get the project root directory (two levels up from this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    missions_dir = os.path.join(project_root, "missions")
    file_path = os.path.join(missions_dir, filename)
    
    # Ensure missions directory exists
    if not os.path.exists(missions_dir):
        os.makedirs(missions_dir)
        
    template = f"""---
# Mission: {feature_name}
**Date:** {date_str_iso}
**Board:** {board}
**Status:** IN PROGRESS

## Goal
{description}

## Constraints
- [ ] List hardware constraints here

## Files In Scope
- [ ] List files that will be modified

## Design Notes
<!-- Architecture decisions and assumptions -->

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Test Plan
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual verification steps

## Known Risks
<!-- List potential issues -->

## Risk Log
| Date | Risk | Mitigation |
|------|------|------------|
|      |      |            |

## Status Log
| Date | Update |
|------|--------|
| {date_str_iso} | Mission created |

## Next Step
<!-- What should happen next -->
---
"""

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(template)
        return f"Mission successfully created at: {file_path}\n\n{template}"
    except Exception as e:
        return f"Error creating mission file: {e}"
