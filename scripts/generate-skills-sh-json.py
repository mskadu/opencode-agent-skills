#!/usr/bin/env python3
"""Generate skills.sh.json from SKILL_MANIFEST and skill name inference.

Output: <repo-root>/skills.sh.json

Keyword-based grouping maps skill directory names to section titles.
Skills that match no keyword land in "Other skills" (ungrouped).
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "SKILL_MANIFEST"

GROUPS = [
    {
        "title": "Safety & Quality",
        "description": "Skills for improving agent output quality and reducing harmful patterns.",
        "keywords": ["sycophancy", "quality", "bias", "safety"],
    },
    {
        "title": "Configuration & Security",
        "description": "Skills for managing agent configuration, permissions, and security.",
        "keywords": ["permission", "config", "secure", "auth"],
    },
    {
        "title": "Workflow & Automation",
        "description": "Skills that automate repetitive development workflows.",
        "keywords": ["suggest", "skill", "workflow", "automation", "sync", "git"],
    },
]


def infer_group(skill_name: str) -> int | None:
    name_lower = skill_name.lower().replace("_", "-")
    for i, group in enumerate(GROUPS):
        for kw in group["keywords"]:
            if kw in name_lower:
                return i
    return None


def generate():
    if not MANIFEST.exists():
        print("SKILL_MANIFEST not found, no skills.sh.json generated.")
        return

    skills = [s.strip() for s in MANIFEST.read_text().splitlines() if s.strip()]

    groupings_dict: dict[int, list[str]] = {i: [] for i in range(len(GROUPS))}
    ungrouped = []

    for skill in skills:
        idx = infer_group(skill)
        if idx is not None:
            groupings_dict[idx].append(skill)
        else:
            ungrouped.append(skill)

    groupings = []
    for i, group in enumerate(GROUPS):
        if groupings_dict[i]:
            groupings.append(
                {
                    "title": group["title"],
                    "description": group["description"],
                    "skills": groupings_dict[i],
                }
            )

    config = {
        "$schema": "https://skills.sh/schemas/skills.sh.schema.json",
        "notGrouped": "bottom",
        "groupings": groupings,
    }

    if not any(g["skills"] for g in groupings):
        config["groupings"] = []
        config["notGrouped"] = "bottom"

    output_path = REPO_ROOT / "skills.sh.json"
    with open(output_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    grouped_count = sum(len(g["skills"]) for g in groupings)
    print(
        f"Generated skills.sh.json: {grouped_count} grouped, {len(ungrouped)} ungrouped"
    )
    if ungrouped:
        print(f"  Ungrouped skills: {', '.join(ungrouped)}")


if __name__ == "__main__":
    generate()
