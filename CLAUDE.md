# Skill & Agent Factory — Project Instructions

> **ALWAYS READ THIS FILE FIRST before any work in this project.**
> This is the master reference for how to operate this workspace.

---

## Project Overview

**Skill & Agent Factory** is a centralized workspace for creating, managing, and using Claude Code skills and agents. When a user describes a task, Claude routes it through the **skill-router** agent, which reads all `skills/*/metadata.md` files (lightweight tag-based filter) then reads `SKILL.md` only for matched candidates.

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
skill-router          ← Phase 1: reads all metadata.md (tag scan, ~10 lines each)
    ↓                    Phase 2: reads SKILL.md for top 3~5 candidates only
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
├── plugins/               ← ALL skills & agents live here (plugin-grouped)
│   ├── devops/            ← DevOps plugin (10 skills + devops-pipeline agent)
│   │   ├── plugin.json
│   │   ├── agents/devops-pipeline.md
│   │   └── skills/{skill-name}/
│   │       ├── metadata.md  ← lightweight routing (tags, use-when, model) — always loaded
│   │       └── SKILL.md     ← full instructions — loaded only when selected
│   ├── figma/             ← Figma plugin (5 skills + figma-to-code agent)
│   │   ├── plugin.json
│   │   ├── agents/figma-to-code.md
│   │   └── skills/{skill-name}/
│   └── project/           ← Project plugin (project-onboarding agent)
│       ├── plugin.json
│       └── agents/project-onboarding.md
├── skills/                ← Legacy — 削除予定 (devops-pr-description: deprecated のみ残存)
├── agents/                ← Legacy — 削除予定 (skill-router: deprecated)
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

**Skills** require TWO files:

`plugins/{plugin}/skills/{category}-{skill-name}/metadata.md` — lightweight routing file (always loaded)
```yaml
---
name: backend-code-review
category: devops
tags: [review, code, quality, bugs, backend]
model: sonnet
use-when: >
  User asks to review backend code for quality, security, or best practices.
  Triggers: "코드 리뷰", "review this", "check for bugs", "バグチェック"
---
```

`plugins/{plugin}/skills/{category}-{skill-name}/SKILL.md` — full instructions (loaded only when selected)
```yaml
---
name: backend-code-review
description: Reviews backend code for quality, security, and best practices.
---

# Backend Code Review
[Instructions...]
```

**metadata.md 필수 필드:**
| Field | Description |
|-------|-------------|
| `name` | 스킬 고유 이름 (폴더명과 일치) |
| `category` | `devops` / `figma` / `backend` 등 |
| `tags` | 라우팅 태그 배열 — 정밀하게 작성할수록 정확도 상승 |
| `model` | `haiku` (빠른 단순 작업) / `sonnet` (복잡한 분석) |
| `use-when` | 트리거 키워드 포함 자연어 설명 (한국어 + 영어 + 일본어) |

**Agents** go in: `plugins/{plugin}/agents/{agent-name}.md`
```yaml
---
name: code-reviewer
description: Expert code reviewer. Use proactively after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: sonnet
---

[System prompt...]
```

### Step 5 — Auto-sync Registry

After creating or updating ANY asset, run:
```bash
python3 scripts/sync-registry.py
```
This auto-updates `registry.md` and `README.md` from `metadata.md` files.
- Increment version manually in `metadata.md` on meaningful updates (v1.0 → v1.1)

### Step 6 — Update README.md (auto via sync-registry.py)

`sync-registry.py` handles README updates automatically. Manual edits only needed for:

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

**metadata.md** (routing layer — required):
- `name`, `category`, `tags` (정밀한 태그), `model`, `use-when` (트리거 키워드 포함)
- Keep under 15 lines — this file is always loaded

**SKILL.md** (instruction layer — required):
- `name`, `description` with trigger keywords
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

## Versioning Strategy

All assets (`metadata.md`, `SKILL.md`, agent files) carry a `version:` field. Follow these rules consistently.

### Version Format: `vMAJOR.MINOR`

| Change Type | Bump | Example | When |
|-------------|------|---------|------|
| Breaking — rename, remove steps, change output format | **MAJOR** | v1.0 → v2.0 | Existing users must adapt |
| Non-breaking — new steps, improved instructions, new tags | **MINOR** | v1.0 → v1.1 | Backward compatible |
| Spelling / comment / formatting only | **none** | stays v1.0 | No behavior change |

### Workflow

1. **Edit** the skill/agent content
2. **Bump version** in `metadata.md` (and `SKILL.md` if it also has `version:`)
3. **Run** `python3 scripts/sync-registry.py` — registry auto-reflects the new version
4. **Run** `python3 scripts/lint-skills.py` — confirm no regressions
5. **Commit** with a message that includes the version bump: e.g., `feat: devops-code-review v1.0 → v1.1`

### Practical Examples

```
# MINOR bump — added a new check rule
metadata.md:  version: v1.1
SKILL.md:     version: v1.1

# MAJOR bump — renamed output format (breaking)
metadata.md:  version: v2.0
SKILL.md:     version: v2.0
```

### No Individual Changelogs Needed

`registry.md` acts as the central version ledger. Each `sync-registry.py` run updates the **Last Modified** column automatically. There is no need to maintain per-skill `CHANGELOG.md` files unless the skill is externally shared.

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

*Last updated: 2026-02-23*
*Project: Skill & Agent Factory v2.0 (Phase B+C: plugin structure + native routing)*
