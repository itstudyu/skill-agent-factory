# Claude Code Sub-Agents — Reference Documentation

> Source: https://code.claude.com/docs/en/sub-agents
> Last fetched: 2026-02-21

---

## What Are Subagents?

Subagents are specialized AI assistants that handle specific types of tasks. Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions.

**Benefits:**
- Preserve context by keeping exploration/implementation out of main conversation
- Enforce constraints by limiting which tools a subagent can use
- Reuse configurations across projects with user-level subagents
- Control costs by routing tasks to faster, cheaper models (e.g., Haiku)

---

## Built-in Subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Read-only | File discovery, code search, codebase exploration |
| **Plan** | Inherits | Read-only | Codebase research for planning (used in plan mode) |
| **general-purpose** | Inherits | All tools | Complex research + multi-step operations |
| **Bash** | Inherits | Bash | Terminal commands in a separate context |

---

## Subagent File Structure

Subagent files use **YAML frontmatter** + **system prompt in Markdown**:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

---

## Where Subagents Live

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Current session | 1 (highest) |
| `.claude/agents/` | Current project | 2 |
| `~/.claude/agents/` | All your projects | 3 |
| Plugin's `agents/` | Where plugin is enabled | 4 (lowest) |

---

## Frontmatter Fields Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase + hyphens) |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Allowed tools. Inherits all if omitted |
| `disallowedTools` | No | Tools to deny |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` (default) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Max agentic turns before stopping |
| `skills` | No | Skills to preload into the subagent's context |
| `mcpServers` | No | MCP servers available to this subagent |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local` |
| `background` | No | `true` = always run as background task |
| `isolation` | No | `worktree` = run in isolated git worktree |

---

## Available Tools

```
Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, WebSearch,
TodoWrite, NotebookEdit, mcp__<server>__<tool>
```

---

## Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard permission checking with prompts |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny permission prompts |
| `bypassPermissions` | Skip all permission checks ⚠️ |
| `plan` | Plan mode (read-only exploration) |

---

## Example Agents

### Read-Only Code Reviewer
```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code clarity and readability
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)
```

### Debugger (Read + Write)
```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works
```

---

## Persistent Memory

Enable cross-session learning with `memory`:

```yaml
---
name: code-reviewer
description: Reviews code with accumulated project knowledge
memory: user
---

Update your agent memory with patterns, conventions, and issues you discover.
```

| Scope | Location | Use when |
|-------|----------|----------|
| `user` | `~/.claude/agent-memory/<name>/` | Cross-project learning |
| `project` | `.claude/agent-memory/<name>/` | Project-specific, shareable |
| `local` | `.claude/agent-memory-local/<name>/` | Project-specific, not committed |

---

## Preloading Skills

Inject skill content at startup (full content, not just available for invocation):

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions from the preloaded skills.
```

---

## Hooks in Subagent Frontmatter

```yaml
---
name: code-reviewer
description: Review code with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

---

## Best Practices

- **Design focused subagents**: each should excel at one specific task
- **Write detailed descriptions**: Claude uses description to decide when to delegate
- **Limit tool access**: grant only necessary permissions
- **Check into version control**: share project subagents with your team
- Use "proactively" in description to encourage automatic delegation
- Use `maxTurns` to prevent runaway agents
