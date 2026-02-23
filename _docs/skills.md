# Claude Code Skills — Reference Documentation

> Source: https://code.claude.com/docs/en/skills
> Last fetched: 2026-02-21

---

## What Are Skills?

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`.

Skills follow the [Agent Skills](https://agentskills.io) open standard.

---

## Skill File Structure

Each skill is a **directory** with `SKILL.md` as the entrypoint:

```
my-skill/
├── SKILL.md           # Main instructions (REQUIRED)
├── template.md        # Template for Claude to fill in (optional)
├── examples/
│   └── sample.md      # Example output (optional)
└── scripts/
    └── validate.sh    # Script Claude can execute (optional)
```

---

## Where Skills Live

| Location | Path | Applies to |
|----------|------|-----------|
| Enterprise | Managed settings | All org users |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |

---

## SKILL.md Format

```yaml
---
name: skill-name
description: What the skill does and when to use it. Claude uses this to decide when to apply the skill.
argument-hint: [optional-hint]
disable-model-invocation: false   # true = only manual /skill-name invocation
user-invocable: true              # false = Claude-only, hidden from menu
allowed-tools: Read, Grep         # Tools Claude can use without asking
model: sonnet                     # Optional: model override
context: fork                     # Optional: run in isolated subagent
agent: Explore                    # Optional: which subagent to use with context: fork
---

# Your skill instructions here

Step-by-step instructions Claude will follow when this skill is invoked.
```

---

## Frontmatter Fields Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (uses directory name if omitted). Lowercase, numbers, hyphens, max 64 chars |
| `description` | Recommended | What it does + when to use. Claude decides when to apply |
| `tags` | Recommended | Explicit intent tags for routing via `metadata.md` scan. Example: `[devops, review, code, quality]`. Include domain (devops, figma, backend…) + action (review, generate, validate…) |
| `requires` | No | Skills that must run before this one. Example: `[figma-design-token-extractor]`. Used for dependency resolution — validated by `make lint`. |
| `status` | No | `deprecated` = skill will be removed. Skips further lint checks |
| `argument-hint` | No | Autocomplete hint. Example: `[issue-number]` |
| `disable-model-invocation` | No | `true` = prevent Claude from auto-loading. Default: `false` |
| `user-invocable` | No | `false` = hide from `/` menu. Default: `true` |
| `allowed-tools` | No | Tools allowed without per-use approval when skill is active |
| `model` | No | Model to use when skill is active |
| `context` | No | `fork` = run in isolated subagent |
| `agent` | No | Subagent type with `context: fork` (e.g., `Explore`, `Plan`) |
| `hooks` | No | Hooks scoped to this skill's lifecycle |

---

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` | Access argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g., `$0`, `$1`) |
| `${CLAUDE_SESSION_ID}` | Current session ID |

---

## Invocation Control

| Frontmatter | You can invoke | Claude can invoke |
|-------------|---------------|------------------|
| (default) | ✅ Yes | ✅ Yes |
| `disable-model-invocation: true` | ✅ Yes | ❌ No |
| `user-invocable: false` | ❌ No | ✅ Yes |

---

## Skill Types

### Reference Skills (auto-loaded by Claude)
```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
```

### Task Skills (manually invoked)
```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

---

## Dynamic Context Injection

Use `!`command`` syntax to pre-fill dynamic data before the skill runs:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## Pull request context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

---

## Run Skills in a Subagent

Add `context: fork` to run the skill in isolation:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings
```

---

## Best Practices

- Keep `SKILL.md` under **500 lines**. Move details to supporting files
- Write clear descriptions with keywords users would naturally say
- Use `disable-model-invocation: true` for workflows with side effects
- Use `allowed-tools` to restrict tool access for safety
- Test with `/skill-name` invocation before deploying
