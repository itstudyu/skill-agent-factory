# Claude Code Agent Teams — Reference Documentation

> Source: https://code.claude.com/docs/en/agent-teams
> Last fetched: 2026-02-21
> ⚠️ **Experimental feature** — disabled by default

---

## What Are Agent Teams?

Agent teams let you coordinate **multiple Claude Code instances** working together. One session acts as the **team lead**, coordinating work. **Teammates** work independently, each in its own context window, and communicate directly with each other.

Unlike subagents, teammates can message each other directly and claim tasks from a shared task list.

---

## Enable Agent Teams

Add to `settings.json` or environment:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## When to Use Agent Teams vs. Subagents

| | Subagents | Agent Teams |
|--|-----------|-------------|
| **Context** | Own context window | Own context window |
| **Communication** | Report to main agent only | Teammates message each other directly |
| **Coordination** | Main agent manages everything | Shared task list with self-coordination |
| **Best for** | Focused tasks where only result matters | Complex work requiring discussion/collaboration |
| **Token cost** | Lower | Higher (each teammate = separate Claude instance) |

**Use subagents** when: focused task, only result needed, no inter-agent coordination needed.
**Use agent teams** when: parallel exploration, research/review, debugging competing hypotheses, cross-layer changes.

---

## Architecture

| Component | Role |
|-----------|------|
| **Team lead** | Main Claude Code session. Creates team, spawns teammates, coordinates |
| **Teammates** | Separate Claude Code instances, each working on assigned tasks |
| **Task list** | Shared work items that teammates claim and complete |
| **Mailbox** | Messaging system between agents |

**Stored locally:**
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

---

## Starting a Team

Tell Claude to create a team in natural language:

```
Create an agent team to explore this from different angles: one teammate
on UX, one on technical architecture, one playing devil's advocate.
```

Claude creates the team, spawns teammates, and coordinates work.

---

## Display Modes

| Mode | How | Requirement |
|------|-----|-------------|
| **In-process** (default) | All teammates in main terminal, use Shift+Down to cycle | Any terminal |
| **Split panes** | Each teammate gets its own pane | tmux or iTerm2 |

Set in `settings.json`:
```json
{ "teammateMode": "in-process" }
```

Or per-session:
```bash
claude --teammate-mode in-process
```

---

## Controlling the Team

```
# Specify teammates and models
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.

# Require plan approval
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.

# Assign tasks
Tell the backend teammate to start on the API endpoints.

# Shut down teammates
Ask the researcher teammate to shut down.

# Clean up
Clean up the team
```

---

## Hooks for Agent Teams

```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/check-teammate-quality.sh"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-task-output.sh"
          }
        ]
      }
    ]
  }
}
```

- **`TeammateIdle`**: Exit code 2 = send feedback and keep teammate working
- **`TaskCompleted`**: Exit code 2 = prevent task completion

---

## Best Use Cases

### Parallel Code Review
```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

### Debugging with Competing Hypotheses
```
Users report the app exits after one message. Spawn 5 agent teammates
to investigate different hypotheses. Have them talk to each other to
disprove each other's theories. Update the findings doc with consensus.
```

---

## Permissions

- Teammates inherit the lead's permission settings
- If lead uses `--dangerously-skip-permissions`, all teammates do too
- Cannot set per-teammate modes at spawn time (change after spawning)

---

## Context Behavior

- Teammates load same project context as a regular session: CLAUDE.md, MCP servers, skills
- They receive the spawn prompt from the lead
- **Lead's conversation history does NOT carry over**
- Include task-specific details in the spawn prompt

---

## Known Limitations

- No session resumption with in-process teammates
- Task status can lag (teammates sometimes fail to mark tasks complete)
- Shutdown can be slow
- One team per session
- No nested teams (teammates cannot spawn their own teams)
- Lead is fixed for the team's lifetime
- Split panes require tmux or iTerm2 (not VS Code integrated terminal)

---

## Best Practices

- Give teammates enough context in the spawn prompt
- Size tasks appropriately (not too small, not too large — aim for 1 clear deliverable each)
- Avoid file conflicts (each teammate should own different files)
- Monitor and steer — don't let teams run fully unattended
- Start with research/review tasks before attempting parallel implementation
- Have 5-6 tasks per teammate for efficiency
