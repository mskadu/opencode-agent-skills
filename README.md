# opencode-agent-skills

A collection of OpenCode skills I've built from real use — things I reach for
daily and have refined through trial and error. If something doesn't work for
you, or you see a gap, open an issue or send a PR.

> Current version: 0.7.0 — see [CHANGELOG](CHANGELOG.md)

## Installation

### Quickest — npx skills

```bash
# List available skills
npx skills add mskadu/opencode-agent-skills --list

# Install a specific skill to OpenCode
npx skills add mskadu/opencode-agent-skills --skill permission-manager --agent opencode

# Install all skills globally
npx skills add mskadu/opencode-agent-skills --all -g -y
```

### One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/mskadu/opencode-agent-skills/main/install.sh | bash
```

### Manual

```bash
git clone https://github.com/mskadu/opencode-agent-skills.git
cp -r opencode-agent-skills/skills/* ~/.config/opencode/skills/
```

## Skills

| Skill | Description | Risk |
|-------|-------------|------|
| [anti-sycophancy](skills/anti-sycophancy/) | Eliminate sycophantic agreement patterns in AI responses | safe |
| [permission-manager](skills/permission-manager/) | Review, configure, and audit OpenCode permission settings | critical |
| [skill-suggester](skills/skill-suggester/) | Scan prompt history for recurring patterns, propose new skills | safe |
| [smart-git-automation](skills/smart-git-automation/) | Smart change detection, auto branch naming, streamlined commit/PR | critical |

## Requirements

- [OpenCode](https://opencode.ai) CLI

## License

MIT
