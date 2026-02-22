# Skill & Agent Factory — Project Instructions

> **ALWAYS READ THIS FILE FIRST before any work in this project.**
> This is the master reference for how to operate this workspace.

---

## Project Overview

**Skill & Agent Factory** is a centralized workspace for creating, managing, and using Claude Code skills and agents. When a user describes a task, Claude routes it through the **skill-router** agent, which dynamically reads `registry.md` and selects the right skill(s) automatically.

Asset types supported:
1. **Skills** (`SKILL.md`) — Reusable capability modules for Claude Code
2. **Agents** (`.md` in `agents/`) — Task-specific autonomous configurations
3. **Plugins** — Packaged bundles of skills, agents, hooks, MCP servers
4. **Hooks** — Shell commands triggered at Claude Code lifecycle events
5. **MCP Servers** — External tool/API integrations via Model Context Protocol
6. **Output Styles** — Custom system prompt styles for specific use cases

All assets are **Claude Code-compatible** and ready to copy directly into any project.

---

## 🔀 Skill Routing

**Request flow:**
```
User Request
    ↓
skill-router          ← reads registry.md live → selects skill(s)
    ↓
Domain Skill(s)       ← backend / frontend / database / figma / etc.
    ↓
devops-pipeline       ← quality gate for all coding tasks
```

- For **clear, single-skill** requests → invoke the skill directly
- For **ambiguous or multi-domain** requests → invoke `skill-router` first
- For **all coding tasks** → `devops-pipeline` always runs after domain skills

---

## ⚠️ MANDATORY: DevOps Pipeline for ALL Development Requests

**ANY time a user asks to write, modify, fix, or create code — the `devops-pipeline` agent MUST run.**

This is non-negotiable. No exceptions.

### Triggers (always activate pipeline)
- Implement / create / build / add a feature
- Fix a bug / update existing code
- Connect to an API / integrate a service
- Create a component / write a function
- Any task that results in writing or changing code

### Pipeline Steps (in order)
| Step | Skill | Required? |
|------|-------|-----------|
| 1. Requirements Gathering | `devops-requirements` | **Always** |
| → Development | — | — |
| 2. Security Scan | `devops-safety-check` | **Always** |
| 3. Code Quality | `devops-code-review` | **Always** |
| 4. Japanese Comments | `devops-japanese-comments` | **Always** |
| 5. Frontend Review | `devops-frontend-review` | Only if UI + design provided |
| 6. Version Check | `devops-version-check` | **Always** |
| 7. Test Generation | `devops-test-gen` | **Always** |
| 8. Git Commit | `devops-git-commit` | **Always** |

### Key Rules
- **Step 1 is a hard gate** — never write code until requirements are fully understood
- **Ask the user** if anything is unclear — never assume
- **Never commit to master/main** unless user explicitly says to
- **Feature branch format:** `feature/{TaskNumber}/{Name}` — ask user for both
- **All comments must be Japanese**
- **Commit messages: Japanese, 1–4 lines**

See `agents/devops-pipeline.md` for the full orchestrator.

---

## 📐 Global Coding Standards

> Full details + examples → `standards/CODING-STANDARDS.md`

Apply to **every** file written or modified, regardless of language or category:

1. **File header** — first line of every source file: one-line Japanese summary comment
2. **Function max 30 lines** — split if exceeded; comment if unavoidable exception
3. **One file, one responsibility** — no unrelated logic in the same file
4. **Commit confirmation** — always show branch/files/message to user and wait for approval before `git commit`

---

## Directory Structure

```
skill-agent-factory/
├── CLAUDE.md              ← This file (auto-read by Claude Code)
├── README.md              ← GitHub documentation
├── registry.md            ← Master registry of ALL assets
├── install.sh             ← Global installer (symlinks to ~/.claude/)
├── skills/                ← ALL skills live here (flat, category-prefixed names)
│   └── {category}-{name}/
│       └── SKILL.md
├── agents/                ← ALL agents live here (flat)
│   └── {agent-name}.md
├── .claude-plugin/
│   └── plugin.json        ← Claude Code plugin manifest
├── standards/             ← Coding standards (detailed rules + examples)
│   └── CODING-STANDARDS.md
├── _docs/                 ← Official reference docs (DO NOT EDIT manually)
│   ├── skills.md
│   ├── sub-agents.md
│   ├── plugins.md
│   ├── hooks.md
│   ├── mcp.md
│   ├── output-styles.md
│   └── agent-teams.md
└── categories/            ← Category context files (CLAUDE.md only, no skills here)
    ├── backend/CLAUDE.md
    ├── frontend/CLAUDE.md
    ├── database/CLAUDE.md
    ├── api-reference/CLAUDE.md
    ├── devops/CLAUDE.md
    └── figma/CLAUDE.md
```

---

## Usage Scope

| Method | How | Skills recognized as |
|--------|-----|----------------------|
| `./install.sh` | Symlinks → `~/.claude/skills/` | **User-level** (all projects, any machine after git clone) |
| Git submodule + `pluginDirs` | Embed repo inside project | **Project-level** (bundled with repo, shared with team) |
| `--plugin-dir` flag | Load for session/project | **Project-level** (no embedding needed) |

---

## Skill Naming Convention

Skills use a **category prefix** so Claude can identify their domain:

| Category | Prefix | Example |
|----------|--------|---------|
| backend | `backend-` | `backend-code-review` |
| frontend | `frontend-` | `frontend-component-gen` |
| database | `database-` | `database-schema-doc` |
| api-reference | `api-` | `api-openapi-gen` |
| devops | `devops-` | `devops-dockerfile` |

---

## Workflow: How to Create or Update Assets

When the user describes a need, follow this workflow:

### Step 1 — Classify

Determine the best asset type:

| Type | Use When |
|------|----------|
| **Skill** | Reusable task Claude should do automatically or on-demand |
| **Agent** | End-to-end autonomous task with specific tools and workflow |
| **Plugin** | Collection of skills/agents/hooks for sharing across projects |
| **Hook** | Deterministic automation at lifecycle events |
| **MCP Server** | Integration with external API or tool |
| **Output Style** | Change how Claude communicates in a session |

### Step 2 — Check Registry

Before creating anything new:
1. Open `registry.md`
2. Search for similar existing assets
3. If similar exists → propose specific updates, confirm before applying
4. If new → proceed to create

### Step 3 — Reference the Right Docs

Always read the relevant doc in `_docs/` before writing:

| Creating... | Reference file |
|-------------|----------------|
| Skill | `_docs/skills.md` |
| Agent | `_docs/sub-agents.md` |
| Plugin | `_docs/plugins.md` |
| Hook | `_docs/hooks.md` |
| MCP Server | `_docs/mcp.md` |
| Output Style | `_docs/output-styles.md` |
| Agent Team | `_docs/agent-teams.md` |

### Step 4 — Create the Asset

**Skills** go in: `skills/{category}-{skill-name}/SKILL.md`
```yaml
---
name: backend-code-review
description: Reviews backend code for quality, security, and best practices.
  Use when the user asks to review, check, or audit backend/server-side code.
---

# Backend Code Review
[Instructions...]
```

**Agents** go in: `agents/{agent-name}.md`
```yaml
---
name: code-reviewer
description: Expert code reviewer. Use proactively after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: sonnet
---

[System prompt...]
```

### Step 5 — Update Registry

After creating or updating ANY asset, update `registry.md`:
- Add/update the row: Name | Type | Category | Version | Description | File Path | Last Modified
- Increment version on every meaningful update (v1.0 → v1.1)

### Step 6 — Update README.md

**Always update `README.md` when anything changes.** No exceptions.

What to update depending on the change:

| Change | README section to update |
|--------|--------------------------|
| New skill added | **Current Skills & Agents** table |
| New agent added | **Current Skills & Agents** table |
| New category added | **Categories** table |
| New folder/file added | **What's Inside** directory tree |
| Pipeline step changed | **DevOps Pipeline** section |
| Coding rule changed | **Global Coding Standards** table |
| Installation changed | **Installation** section |

### Step 7 — Remind User to Re-run install.sh

After creating new skills or agents, remind the user:
> "새 스킬/에이전트를 추가했으니 `./install.sh` 를 다시 실행해 주세요!"

---

## Quality Standards

### Skills must have:
- YAML frontmatter: `name`, `description` with **clear trigger keywords**
- Step-by-step instructions Claude will follow
- Examples (when helpful)
- Keep under 500 lines; move details to supporting files

### Agents must have:
- YAML frontmatter: `name`, `description`, `tools`, `model`
- Goal definition in the system prompt
- Numbered workflow steps
- Input/output format described

### All assets:
- Written in **English**
- Start at **v1.0**, increment on updates
- Descriptive names with category prefix (for skills)

---

## Communication Rules

- **Speak Korean** with the user
- **Write all assets in English**
- **Always confirm** before overwriting existing assets
- **Always ask** when requirements are unclear — never assume
- **Always update `registry.md`** after any creation or update
- **Always update `README.md`** when anything in the project changes — skills, agents, structure, rules, pipeline
- **Remind user to run `./install.sh`** after adding new skills/agents

---

*Last updated: 2026-02-21*
*Project: Skill & Agent Factory v1.0*
