# ollama-sync

Keeps your OpenCode model list in sync with what Ollama actually has installed.

Runs `ollama list`, parses the output, and writes the model names to the
`ollama` provider section in `opencode.json`. That's it.

You need Ollama running and write access to `opencode.json`.

## Comparison with opencode-model-scout

`opencode-model-scout` is a community plugin that auto-discovers models and
enriches them with metadata at startup — no config file changes needed. If
you're already running it with `"probe": "ollama"`, this skill is redundant.
Use this skill only if you prefer an explicit model list in your config or
aren't using the plugin.
