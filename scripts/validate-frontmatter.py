#!/usr/bin/env python3
"""Validate frontmatter of all SKILL.md files in the skills directory."""

import sys
import os
import re
from pathlib import Path
import yaml

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def parse_frontmatter(path):
    content = path.read_text()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])


def validate():
    errors = []
    names_seen = set()

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir.name}/SKILL.md: missing")
            continue

        meta = parse_frontmatter(skill_md)
        if meta is None:
            errors.append(
                f"{skill_dir.name}/SKILL.md: missing or invalid YAML frontmatter"
            )
            continue

        name = meta.get("name")
        if not name:
            errors.append(f"{skill_dir.name}/SKILL.md: missing 'name' in frontmatter")
        else:
            if not re.match(r"^[a-z][a-z0-9-]*$", name):
                errors.append(
                    f"{skill_dir.name}/SKILL.md: name '{name}' is not kebab-case"
                )
            if len(name) > 50:
                errors.append(
                    f"{skill_dir.name}/SKILL.md: name '{name}' exceeds 50 chars"
                )
            if name in names_seen:
                errors.append(f"Duplicate skill name: {name}")
            names_seen.add(name)

        if not meta.get("description"):
            errors.append(
                f"{skill_dir.name}/SKILL.md: missing 'description' in frontmatter"
            )

    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("All skills valid.")


if __name__ == "__main__":
    validate()
