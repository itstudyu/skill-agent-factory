# Claude Code Hooks — Reference Documentation

> Source: https://code.claude.com/docs/en/hooks-guide
> Last fetched: 2026-02-21

---

## What Are Hooks?

Hooks are user-defined shell commands that execute at specific points in Claude Code's lifecycle. They provide **deterministic control** over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM.

**Common uses:**
- Format code after edits (Prettier, ESLint, Black)
- Block dangerous commands before execution
- Send desktop notifications when Claude needs input
- Re-inject context after compaction
- Audit configuration changes

---

## Hook Events

| Event | When it fires |
|-------|--------------|
| `SessionStart` | When a session begins or resumes |
| `UserPromptSubmit` | When you submit a prompt, before Claude processes it |
| `PreToolUse` | Before a tool call executes. **Can block it** |
| `PermissionRequest` | When a permission dialog appears |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `Notification` | When Claude Code sends a notification |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent finishes |
| `Stop` | When Claude finishes responding |
| `TeammateIdle` | When an agent team teammate is about to go idle |
| `TaskCompleted` | When a task is being marked as completed |
| `ConfigChange` | When a configuration file changes during a session |
| `PreCompact` | Before context compaction |
| `SessionEnd` | When a session terminates |

---

## Hook Configuration Structure

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

---

## Where to Configure Hooks

| Location | Scope | Shareable |
|----------|-------|-----------|
| `~/.claude/settings.json` | All your projects | No |
| `.claude/settings.json` | Single project | ✅ Yes (commit to repo) |
| `.claude/settings.local.json` | Single project | No (gitignored) |
| Plugin `hooks/hooks.json` | When plugin enabled | ✅ Yes (bundled) |
| Skill/agent frontmatter `hooks:` | While skill/agent active | ✅ Yes |

---

## Hook Input (stdin JSON)

Every hook receives JSON on stdin with common fields:

```json
{
  "session_id": "abc123",
  "cwd": "/Users/user/myproject",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

---

## Exit Codes

| Exit code | Effect |
|-----------|--------|
| **0** | Action proceeds. Stdout added to Claude's context (for `UserPromptSubmit`, `SessionStart`) |
| **2** | Action **BLOCKED**. Stderr message sent to Claude as feedback |
| **Other** | Action proceeds. Stderr logged but not shown to Claude |

---

## Matcher Reference

| Event | What the matcher filters | Example values |
|-------|--------------------------|----------------|
| `PreToolUse`, `PostToolUse` | Tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | How session started | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | Why session ended | `clear`, `logout`, `prompt_input_exit` |
| `Notification` | Notification type | `permission_prompt`, `idle_prompt` |
| `SubagentStart`, `SubagentStop` | Agent type | `Bash`, `Explore`, custom agent names |
| `PreCompact` | What triggered compaction | `manual`, `auto` |

---

## Common Hook Examples

### Auto-format code after edits
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

### Notify when Claude needs input (macOS)
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Block edits to protected files
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```
```bash
#!/bin/bash
# protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done
exit 0
```

### Re-inject context after compaction
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing.'"
          }
        ]
      }
    ]
  }
}
```

---

## Hook Types

### 1. `command` — Shell command (most common)
```json
{ "type": "command", "command": "./scripts/validate.sh" }
```

### 2. `prompt` — LLM-based decision
```json
{
  "type": "prompt",
  "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains\"}."
}
```

### 3. `agent` — Subagent with tool access
```json
{
  "type": "agent",
  "prompt": "Verify that all unit tests pass. Run the test suite and check the results.",
  "timeout": 120
}
```

---

## Structured JSON Output

For more control, exit 0 and print a JSON object to stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

`permissionDecision` options: `"allow"`, `"deny"`, `"ask"`

---

## Best Practices

- Use `jq` for JSON parsing in bash hooks
- Use absolute paths or `$CLAUDE_PROJECT_DIR` variable
- Make hook scripts executable: `chmod +x ./my-hook.sh`
- Check `stop_hook_active` in Stop hooks to prevent infinite loops
- Wrap shell profile `echo` statements with `if [[ $- == *i* ]]` to prevent JSON parsing issues
