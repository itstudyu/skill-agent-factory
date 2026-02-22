# Claude Code Output Styles — Reference Documentation

> Source: https://code.claude.com/docs/en/output-styles
> Last fetched: 2026-02-21

---

## What Are Output Styles?

Output styles allow you to use Claude Code as any type of agent while keeping its core capabilities. They directly modify Claude Code's **system prompt** to change how Claude communicates and behaves.

---

## Built-in Output Styles

| Style | Description |
|-------|-------------|
| **Default** | Standard software engineering assistant |
| **Explanatory** | Adds educational "Insights" between tasks. Helps understand implementation choices |
| **Learning** | Collaborative learn-by-doing mode. Adds insights + `TODO(human)` markers for you to fill in |

---

## How to Change Output Style

```bash
# Via menu
/output-style

# Direct switch
/output-style explanatory
/output-style learning
/output-style default
```

Settings are saved in `.claude/settings.local.json` under the `outputStyle` field.

---

## Create a Custom Output Style

Custom output styles are Markdown files with YAML frontmatter:

```markdown
---
name: My Custom Style
description: A brief description shown to the user
keep-coding-instructions: false
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering tasks.

[Your custom instructions here...]

## Specific Behaviors

[Define how Claude should behave in this style...]
```

---

## Where to Store Custom Styles

| Location | Scope |
|----------|-------|
| `~/.claude/output-styles/` | User level (all projects) |
| `.claude/output-styles/` | Project level |

---

## Frontmatter Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Display name | File name |
| `description` | Description shown in `/output-style` menu | None |
| `keep-coding-instructions` | Keep coding-related parts of the default system prompt | `false` |

---

## How Output Styles Work

1. All output styles **exclude** instructions for efficient output (conciseness)
2. Custom output styles **exclude** coding instructions (verifying with tests, etc.) — unless `keep-coding-instructions: true`
3. Custom instructions are **appended** to the end of the system prompt
4. Claude receives **reminders** to adhere to the style during conversation

---

## Output Style vs. Other Features

| Feature | What it does |
|---------|-------------|
| **Output Style** | Modifies the main system prompt (always active when selected) |
| **CLAUDE.md** | Added as a user message AFTER the system prompt |
| `--append-system-prompt` | Appends to the system prompt |
| **Agents** | Invoked for specific tasks; includes model/tools/context settings |
| **Skills** | Task-specific prompts invoked on-demand; always active when auto-loaded |

---

## Custom Style Example: Documentation Writer

```markdown
---
name: Documentation Writer
description: Transforms Claude into a technical documentation specialist
keep-coding-instructions: false
---

# Documentation Writer Mode

You are a technical documentation specialist. Your primary role is to help users create, improve, and maintain high-quality technical documentation.

## Core Behaviors

1. **Always ask about audience first**: Before writing, confirm who the documentation is for
2. **Use clear, active voice**: Write "Click the button" not "The button should be clicked"
3. **Include examples**: Every concept needs a concrete example
4. **Structure matters**: Use consistent heading hierarchy (H1 → H2 → H3)

## Output Format

- Lead with the most important information
- Use bullet points for lists of 3+ items
- Include a "Quick Start" section for tutorials
- Add a "Troubleshooting" section for complex features
- End with "Next Steps" or "Related Resources"

## Code Examples

When including code:
- Always specify the programming language in code blocks
- Include comments for non-obvious lines
- Show both success and error cases
```

---

## Best Practices

- Use `keep-coding-instructions: true` when your style extends (rather than replaces) coding behavior
- Keep descriptions concise — they appear in the menu
- Test your style with `/output-style your-style-name`
- Combine with CLAUDE.md for project-specific context that persists across style changes
