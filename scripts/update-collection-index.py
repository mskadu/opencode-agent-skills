#!/usr/bin/env python3
"""Update a FrancoStino opencode-skills-collection index with skill entries.

Reads the collection repo's skills_index.json, adds or updates entries for
each skill, and writes back.

Usage:
    python scripts/update-collection-index.py <collection-dir> <skills-dir> [date-added]
"""

import sys
import json
from pathlib import Path
import yaml


def parse_frontmatter(path):
    content = path.read_text()
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def update_index(collection_dir, skills_dir, date_added=None):
    collection_dir = Path(collection_dir)
    skills_dir = Path(skills_dir)
    index_path = collection_dir / "skills_index.json"

    if not index_path.exists():
        print(f"Error: {index_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(index_path) as f:
        index = json.load(f)

    if not date_added:
        from datetime import date

        date_added = date.today().isoformat()

    updated = 0
    added = 0

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        name = skill_dir.name
        meta = parse_frontmatter(skill_md)

        new_entry = {
            "id": name,
            "path": f"skills/{name}",
            "category": meta.get("category", "development"),
            "name": name,
            "description": meta.get("description", ""),
            "risk": meta.get("risk", "safe"),
            "source": "community",
            "date_added": date_added,
            "plugin": {
                "targets": {
                    "codex": "supported",
                    "claude": "supported",
                },
                "setup": {
                    "type": "none",
                    "summary": "",
                    "docs": None,
                },
                "reasons": [],
            },
        }

        found = False
        for i, entry in enumerate(index):
            if entry.get("id") == name:
                index[i] = new_entry
                found = True
                updated += 1
                break

        if not found:
            index.append(new_entry)
            added += 1

    # Sort by id for consistency
    index.sort(key=lambda x: x.get("id", ""))

    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")

    print(f"Added: {added}, Updated: {updated}")
    print(f"Total entries: {len(index)}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <collection-dir> <skills-dir> [date-added]")
        sys.exit(1)

    collection_dir = sys.argv[1]
    skills_dir = sys.argv[2]
    date_added = sys.argv[3] if len(sys.argv) > 3 else None

    update_index(collection_dir, skills_dir, date_added)
