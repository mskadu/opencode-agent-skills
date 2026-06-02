#!/usr/bin/env bash
set -euo pipefail

SOURCE="${1:?Usage: $0 <path-to-all-my-skills>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$ROOT/SKILL_MANIFEST"
SKILLS_DIR="$ROOT/skills"

if [ ! -d "$SOURCE/opencode-skills" ]; then
  echo "Error: $SOURCE does not look like all-my-skills (missing opencode-skills/)"
  exit 1
fi

mkdir -p "$SKILLS_DIR"

while IFS= read -r skill; do
  [ -z "$skill" ] && continue
  echo "Syncing: $skill"

  target_dir="$SKILLS_DIR/$skill"
  mkdir -p "$target_dir"

  # Copy SKILL.md with license injected
  src="$SOURCE/opencode-skills/$skill/SKILL.md"
  if [ ! -f "$src" ]; then
    echo "  WARNING: $src not found, skipping"
    continue
  fi

  python3 -c "
import sys, re

path = '$src'
content = open(path).read()

if not content.startswith('---'):
    print('  ERROR: no frontmatter in $src', file=sys.stderr)
    sys.exit(1)

parts = content.split('---', 2)
frontmatter = parts[1]

if 'license:' not in frontmatter:
    # Insert license after the first line (---) or after name/description
    lines = frontmatter.split('\n')
    # Find a good insertion point: after description or after name if no description
    insert_after = -1
    for i, line in enumerate(lines):
        if line.startswith('description:') or line.startswith('description '):
            insert_after = i
            break
    if insert_after < 0:
        for i, line in enumerate(lines):
            if line.startswith('name:') or line.startswith('name '):
                insert_after = i
                break
    if insert_after < 0:
        insert_after = 0
    lines.insert(insert_after + 1, 'license: MIT')
    frontmatter = '\n'.join(lines)

parts[1] = frontmatter
out_path = '$target_dir/SKILL.md'
open(out_path, 'w').write('---'.join(parts))
print('  SKILL.md synced (license injected)')
"

  # Copy README.md if it exists
  src_readme="$SOURCE/opencode-skills/$skill/README.md"
  if [ -f "$src_readme" ]; then
    cp "$src_readme" "$target_dir/README.md"
    echo "  README.md synced"
  fi

done < "$MANIFEST"

# Bump version
bash "$ROOT/scripts/bump-version.sh"

# Update CHANGELOG
today=$(date +%Y-%m-%d)
new_version=$(cat "$ROOT/VERSION")
changelog="$ROOT/CHANGELOG.md"

cat > /tmp/changelog_new.md << EOF
# Changelog

## $new_version — $today

### Added

- Synced skills from source.

\`\`\`
$(cat "$MANIFEST")
\`\`\`

$(cat "$changelog" | tail -n +3)
EOF
mv /tmp/changelog_new.md "$changelog"

echo "Sync complete. Version bumped to $(cat "$ROOT/VERSION")."
