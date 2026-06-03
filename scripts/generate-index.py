#!/usr/bin/env python3
"""Generate OpenCode-compatible index.json from skills/ directory.

Usage:
    python scripts/generate-index.py
    python scripts/generate-index.py --output ./pages-dist

The output directory receives:
  - index.json          Remote skill index (OpenCode discovery format)
  - .nojekyll           Disables GitHub Pages Jekyll processing
  - <skillname>/        Flattened skill files from skills/<skillname>/
  - .publish-manifest   List of generated files (for CI workflows)
"""

import sys
import json
import shutil
import argparse
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MANIFEST_FILE = REPO_ROOT / "SKILL_MANIFEST"
VERSION_FILE = REPO_ROOT / "VERSION"


def parse_frontmatter(path):
    content = path.read_text()
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    return yaml.safe_load(parts[1]) or {}, content


def list_skill_files(skill_dir):
    files = []
    for path in sorted(skill_dir.rglob("*")):
        if path.is_file():
            files.append(str(path.relative_to(skill_dir)))
    return sorted(files)


def generate(output_dir: Path):
    skills_list = []
    skill_names = []

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            print(
                f"  WARNING: {skill_dir.name}/SKILL.md not found, skipping",
                file=sys.stderr,
            )
            continue

        meta, _ = parse_frontmatter(skill_md)
        name = meta.get("name") or skill_dir.name

        files = list_skill_files(skill_dir)
        skills_list.append({"name": name, "files": files})
        skill_names.append(name)

        target = output_dir / name
        target.mkdir(parents=True, exist_ok=True)
        for f in files:
            src = skill_dir / f
            dst = target / f
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        print(f"  {name}: {len(files)} files")

    if not skills_list:
        print("No skills found.", file=sys.stderr)
        sys.exit(0)

    index = {"skills": skills_list}
    index_path = output_dir / "index.json"
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
    print(f"\nWrote index.json ({len(skills_list)} skills)")

    (output_dir / ".nojekyll").touch()

    all_paths = ["index.json", ".nojekyll"]
    all_paths.extend(f"{n}/" for n in skill_names)
    (output_dir / ".publish-manifest").write_text("\n".join(all_paths) + "\n")

    version = VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else "0.0.0"
    print(f"Version: {version}")
    print(f"Output: {output_dir}")
    print(f"Files listed in {output_dir / '.publish-manifest'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=REPO_ROOT,
        help="Output directory (default: repo root)",
    )
    args = parser.parse_args()
    generate(args.output.resolve())
