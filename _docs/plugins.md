# Claude Code Plugins — Reference Documentation

> Source: https://code.claude.com/docs/en/plugins
> Last fetched: 2026-02-21

---

## What Are Plugins?

Plugins let you extend Claude Code with custom functionality that can be **shared across projects and teams**. A plugin bundles skills, agents, hooks, and MCP servers into a single distributable package.

---

## Standalone vs. Plugin

| Approach | Skill names | Best for |
|----------|-------------|----------|
| **Standalone** (`.claude/`) | `/hello` | Personal workflows, quick experiments |
| **Plugins** (`.claude-plugin/plugin.json`) | `/plugin-name:hello` | Team sharing, marketplace distribution |

---

## Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED: Plugin manifest
├── skills/                  # Optional: Agent Skills (SKILL.md files)
│   └── skill-name/
│       └── SKILL.md
├── agents/                  # Optional: Custom agent definitions
│   └── agent-name.md
├── commands/                # Optional: Skills as Markdown files (legacy)
│   └── command-name.md
├── hooks/                   # Optional: Event handlers
│   └── hooks.json
├── .mcp.json                # Optional: MCP server configurations
├── .lsp.json                # Optional: LSP server configurations
└── settings.json            # Optional: Default settings when plugin enabled
```

> ⚠️ **Important**: Do NOT put `skills/`, `agents/`, or `hooks/` inside `.claude-plugin/`. Only `plugin.json` goes there.

---

## Plugin Manifest (plugin.json)

```json
{
  "name": "my-plugin",
  "description": "A brief description shown in the plugin manager",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  },
  "homepage": "https://github.com/user/my-plugin",
  "repository": "https://github.com/user/my-plugin",
  "license": "MIT"
}
```

| Field | Purpose |
|-------|---------|
| `name` | Unique identifier + skill namespace prefix |
| `description` | Shown in plugin manager |
| `version` | Semantic versioning (1.0.0) |
| `author` | Attribution (optional) |

---

## Creating a Plugin Step by Step

### 1. Create directory structure
```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/skills/my-skill
mkdir -p my-plugin/agents
mkdir -p my-plugin/hooks
```

### 2. Create the manifest
```json
// my-plugin/.claude-plugin/plugin.json
{
  "name": "my-plugin",
  "description": "My custom plugin",
  "version": "1.0.0"
}
```

### 3. Add a skill
```yaml
# my-plugin/skills/my-skill/SKILL.md
---
name: my-skill
description: What this skill does. Use when...
---

Instructions for Claude to follow when this skill is invoked.
```

### 4. Test locally
```bash
claude --plugin-dir ./my-plugin
# Then try: /my-plugin:my-skill
```

---

## Plugin Hooks (hooks/hooks.json)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix"
          }
        ]
      }
    ]
  }
}
```

---

## Plugin MCP Servers (.mcp.json)

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths.

---

## Default Settings (settings.json)

Activate a custom agent as the main thread when the plugin is enabled:

```json
{
  "agent": "security-reviewer"
}
```

---

## Test Multiple Plugins

```bash
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

---

## Migrating from Standalone to Plugin

| Standalone (`.claude/`) | Plugin |
|------------------------|--------|
| `.claude/commands/` files | `plugin-name/commands/` |
| `.claude/skills/` files | `plugin-name/skills/` |
| `.claude/agents/` files | `plugin-name/agents/` |
| Hooks in `settings.json` | `hooks/hooks.json` |
| Only in one project | Shareable via marketplace |

---

## Skill Naming in Plugins

- Skills are prefixed with the plugin name
- `hello/SKILL.md` in plugin `my-plugin` → invoked as `/my-plugin:hello`
- Prevents conflicts between plugins

---

## Distribution

1. Add `README.md` with installation and usage instructions
2. Use semantic versioning in `plugin.json`
3. Distribute via [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
4. Install with `/plugin install` command

---

## Best Practices

- Start with standalone `.claude/` for quick iteration
- Convert to plugin when ready to share
- Keep plugin names unique and descriptive
- Use `${CLAUDE_PLUGIN_ROOT}` for relative paths in MCP/hooks
- Test every component before distributing
