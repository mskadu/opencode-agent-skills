#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/mskadu/opencode-agent-skills.git"
INSTALL_DIR="${HOME}/.config/opencode/skill-repos/opencode-agent-skills"
SKILLS_TARGET="${HOME}/.config/opencode/skills"

echo "Installing opencode-agent-skills..."

# Clone if not already present
if [ ! -d "$INSTALL_DIR" ]; then
  mkdir -p "$(dirname "$INSTALL_DIR")"
  git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
else
  echo "Updating existing installation..."
  git -C "$INSTALL_DIR" pull --depth 1
fi

# Symlink each skill
mkdir -p "$SKILLS_TARGET"
for skill_dir in "$INSTALL_DIR"/skills/*/; do
  skill_name="$(basename "$skill_dir")"
  link_path="$SKILLS_TARGET/$skill_name"
  if [ -L "$link_path" ] || [ -d "$link_path" ]; then
    rm -rf "$link_path"
  fi
  ln -sf "$skill_dir" "$link_path"
  echo "  Linked: $skill_name"
done

echo "Done. Skills are available in ~/.config/opencode/skills/"
