#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
VERSION_FILE="$ROOT/VERSION"
current=$(cat "$VERSION_FILE")

# Bump minor: X.Y.Z -> X.(Y+1).0
major=$(echo "$current" | cut -d. -f1)
minor=$(echo "$current" | cut -d. -f2)
patch=$(echo "$current" | cut -d. -f3)

new_minor=$((minor + 1))
new_version="$major.$new_minor.0"

echo "$new_version" > "$VERSION_FILE"

# Update README badge
README_FILE="$ROOT/README.md"
sed -i '' "s/Current version: [0-9]*\.[0-9]*\.[0-9]*/Current version: $new_version/" "$README_FILE"

echo "$current -> $new_version"
