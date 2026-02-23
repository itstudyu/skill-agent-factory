# Skill & Agent Factory

A centralized workspace for creating, managing, and using **Claude Code skills and agents**, organized by development category.

When you give Claude Code a task, it automatically selects the right skill or agent from this factory based on what you're asking — and runs every development request through a **mandatory quality pipeline**.

---

## What's Inside

```
skill-agent-factory/
├── CLAUDE.md            ← Master instructions (auto-read by Claude Code)
├── README.md            ← This file
├── registry.md          ← Master registry of ALL assets (auto-updated by scripts)
├── install.sh           ← Global installer: symlinks + orphan cleanup + lint + hooks
├── skills/              ← ALL skills (flat, category-prefixed names)
│   └── {category}-{name}/SKILL.md
├── agents/              ← ALL agents
│   └── {agent-name}.md
├── scripts/             ← Automation utilities (run via install.sh or manually)
│   ├── sync-registry.py ← Auto-syncs registry.md + README.md from SKILL.md files
│   ├── lint-skills.py   ← Quality checker: frontmatter, requires refs, dep chains
│   └── dep-graph.py     ← Dependency tree visualizer + reverse lookup
├── standards/           ← Global coding rules (detailed examples)
│   └── CODING-STANDARDS.md
├── categories/          ← Category context docs (reference only — skills live in skills/)
│   ├── backend/CLAUDE.md
│   ├── frontend/CLAUDE.md
│   ├── database/CLAUDE.md
│   ├── api-reference/CLAUDE.md
│   ├── devops/CLAUDE.md
│   └── figma/CLAUDE.md
└── _docs/               ← Official Claude Code reference docs
```

**Skill naming convention:** `{category}-{skill-name}`
- `devops-code-review` → invoked as `/skill-agent-factory:devops-code-review`
- `backend-api-gen` → invoked as `/skill-agent-factory:backend-api-gen`

---

## DevOps Pipeline (Mandatory for All Development)

Every development request automatically runs through this pipeline:

```
[1] Requirements Gathering   ← Hard gate — reads project-context/, asks if unclear
         ↓  (Figma URL provided? → figma-to-code agent handles full Figma workflow)
         ↓  (write code)
[2] Security Scan            ← Secrets, injection patterns (lightweight)
[3] Code Quality Review      ← Logic, memory, N+1 queries, coding standards
[4] Japanese Comments        ← All comments converted/added in Japanese
[5] Frontend Review          ← Figma: figma-code-sync + figma-responsive-validator
                                Screenshot: pixel-perfect visual check
[6] Version Check            ← Language version & deprecated API check
[7] Test Generation          ← Unit tests auto-generated
[8] Git Commit               ← Shows summary, waits for user approval, then commits
```

Orchestrated by `agents/devops-pipeline.md`.

---

## Global Coding Standards

Applied to every file, regardless of language or category. Full details in `standards/CODING-STANDARDS.md`.

| Rule | Description |
|------|-------------|
| **File header** | First line of every source file: one-line Japanese summary comment |
| **Function max 30 lines** | Split if exceeded; comment if unavoidable exception |
| **One file, one responsibility** | No unrelated logic in the same file |
| **Commit confirmation** | Always shows branch/files/message — waits for user approval before committing |
| **Comments in Japanese** | All code comments and log messages in Japanese |
| **Commit messages in Japanese** | 1–4 lines, key content only |
| **Branch naming** | `feature/{TaskNumber}/{Name}` — never commits to master without explicit instruction |

---

## Installation

Choose the method that fits your use case:

| Method | Scope | Use When |
|--------|-------|----------|
| **Method 1** — Global Symlink | User-level (all projects, all sessions) | You want skills available everywhere on this machine |
| **Method 2** — Git Submodule | Per-project (bundled in repo) | You want skills tied to a specific project and shared with team |
| **Method 3** — Plugin Dir | Per-session or per-project | You want to load the factory without embedding it |

---

### Method 1 — Global Symlink → User-Level Skills on Any Computer

Run once after cloning. Makes all skills/agents available in **every** Claude Code project automatically — no flags needed.

```bash
git clone https://github.com/ysjapan97/skill-agent-factory ~/skill-agent-factory
cd ~/skill-agent-factory
chmod +x install.sh
./install.sh
```

**What it does:**
1. Symlinks `~/.claude/skills/` → this repo's `skills/` (available in all projects)
2. Symlinks `~/.claude/agents/` → this repo's `agents/` (available in all projects)
3. Adds `SessionStart` hooks to `~/.claude/settings.json` — Claude **automatically re-reads** the DevOps pipeline rules at every session start, after context compaction, and on session resume. No more forgetting instructions.

**To use on a new computer:**
```bash
git clone https://github.com/ysjapan97/skill-agent-factory ~/skill-agent-factory
cd ~/skill-agent-factory && ./install.sh
```

**To update after adding new skills:**
```bash
git pull
./install.sh   # links any newly added skills
```

**To uninstall:**
```bash
./install.sh --uninstall
```

---

### Method 2 — Git Submodule → Per-Project, Bundled in Repo

Use this when you want to embed the factory directly inside a project. The factory travels with your repo.

```bash
cd my-project
git submodule add https://github.com/ysjapan97/skill-agent-factory
git submodule update --init --recursive
```

Add to your project's `.claude/settings.json`:
```json
{
  "pluginDirs": ["./skill-agent-factory"]
}
```

**To update the submodule:**
```bash
cd skill-agent-factory && git pull origin main
cd .. && git add skill-agent-factory && git commit -m "chore: update skill-agent-factory"
```

**When a teammate clones your project:**
```bash
git clone --recurse-submodules https://github.com/you/my-project
# skills are automatically available — no extra setup needed
```

> Skills are namespaced when loaded as a plugin:
> `/skill-agent-factory:devops-code-review`

---

### Method 3 — Claude Code Plugin (`--plugin-dir`)

**Per session:**
```bash
claude --plugin-dir ~/path/to/skill-agent-factory
```

**Per project** — add to your project's `.claude/settings.json`:
```json
{
  "pluginDirs": ["~/path/to/skill-agent-factory"]
}
```

**Global via shell alias:**
```bash
alias claude='claude --plugin-dir ~/skill-agent-factory'
```

---

## Current Skills & Agents

### Devops Skills

| Skill | Purpose |
|-------|---------|
| `devops-arch-review` | Architecture and coding standards review. Use when the user asks to check code s |
| `devops-code-review` | Code quality and logic review. Run after code is written. Verifies AI-generated  |
| `devops-frontend-review` | Frontend pixel-perfect review. Run after frontend code is written. Compares impl |
| `devops-git-commit` | Git commit with branch strategy. Run at the END of every development task. Creat |
| `devops-japanese-comments` | Enforce Japanese language in code comments and log messages. Run after code revi |
| `devops-requirements` | Development requirements gathering. Use at the START of every development reques |
| `devops-safety-check` | Lightweight code security check. Run after code is written. Checks for secrets,  |
| `devops-skill-eval` | Evaluates the quality and correctness of a skill by running test scenarios again |
| `devops-test-gen` | Automatically generate unit tests for newly written code. Run after code review  |
| `devops-version-check` | Language version and dependency safety check. Verifies code uses correct syntax  |

### Figma Skills

| Skill | Purpose |
|-------|---------|
| `figma-code-sync` | Verifies that the implemented code matches the Figma design mapping. Use when yo |
| `figma-design-analyzer` | Analyzes Figma designs to produce a frontend implementation blueprint before cod |
| `figma-design-token-extractor` | Extracts design tokens (colors, fonts, spacing, shadows, border-radius, etc.) fr |
| `figma-framework-figma-mapper` | Maps UI framework components to Figma design components. Supports PrimeFaces as  |
| `figma-responsive-validator` | Validates responsive design compliance of frontend code across Mobile, Tablet, a |

### Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `devops-pipeline` | sonnet | Development pipeline orchestrator. Called by skill-router for development tasks. |
| `figma-to-code` | opus | Converts Figma designs into production-ready frontend code. Use proactively when |
| `project-onboarding` | sonnet | Project onboarding agent. Auto-detects existing vs new projects, analyzes code p |
| `skill-router` | sonnet | PRIMARY ENTRY POINT for ALL user requests. Always invoke skill-router first — it |

---

## Automation Scripts

| Script | When to Run | What It Does |
|--------|------------|--------------|
| `python3 scripts/sync-registry.py` | Auto (via install.sh) | Scans all SKILL.md + agents/*.md and updates registry.md + README.md |
| `python3 scripts/lint-skills.py` | Auto (via install.sh) | Checks frontmatter, requires refs, step structure, dep chain depth |
| `python3 scripts/lint-skills.py --strict` | CI / pre-merge | Same as above but warnings also count as errors |
| `python3 scripts/dep-graph.py` | On demand | Prints full dependency tree for all skills |
| `python3 scripts/dep-graph.py --reverse <skill>` | Before deleting a skill | Shows which skills depend on the target skill |
| `python3 scripts/dep-graph.py --check` | On demand | Prints only dependency issues (missing refs, deep chains) |

---

## Adding New Skills

### 1. Create the skill directory
```bash
mkdir -p skills/backend-my-skill
```

### 2. Write SKILL.md
```yaml
# skills/backend-my-skill/SKILL.md
---
name: backend-my-skill
description: What this skill does. Use when the user asks to... [clear trigger keywords]
tags: [backend, generate, code, api]
---

# Backend My Skill

Step-by-step instructions for Claude to follow...
```

`tags:` 는 skill-router의 Phase 1 필터링에 사용됩니다. 스킬의 도메인(devops, figma 등)과 액션(review, generate, validate 등)을 포함하세요.

### 3. Re-run installer
```bash
./install.sh
# 심링크 생성 + registry.md / README.md 자동 갱신 + lint 체크
```

registry.md와 README.md는 `sync-registry.py`가 자동으로 업데이트합니다. 수동 편집 불필요.

---

## Adding New Agents

```markdown
<!-- agents/my-agent.md -->
---
name: my-agent
description: When Claude should delegate to this agent. Use proactively when...
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a specialized agent for...
```

Then re-run `./install.sh` — registry.md and README are updated automatically.

---

## Categories

| Category | Description |
|----------|-------------|
| `backend` | Server APIs, business logic, auth, background jobs, testing |
| `frontend` | UI components, state management, styling, accessibility |
| `database` | Schema design, migrations, query optimization, ORM |
| `api-reference` | OpenAPI specs, API docs, SDK generation, webhooks |
| `devops` | CI/CD, Docker, Kubernetes, IaC, monitoring, pipeline |
| `figma` | Figma → Code workflow: token extraction, mapping, sync verification |

---

## Reference Docs

| File | Contents |
|------|----------|
| `standards/CODING-STANDARDS.md` | Global coding rules with detailed examples |
| `_docs/skills.md` | Skill format, frontmatter fields, advanced patterns |
| `_docs/sub-agents.md` | Agent format, tools, permission modes |
| `_docs/hooks.md` | Hook events, configuration, examples |
| `_docs/plugins.md` | Plugin structure, manifest, distribution |
| `_docs/mcp.md` | MCP server setup, scopes, authentication |
| `_docs/output-styles.md` | Custom output style format |
| `_docs/agent-teams.md` | Multi-agent coordination (experimental) |

---

## Requirements

- [Claude Code](https://claude.ai/code) v1.0.33 or later
- macOS / Linux (install.sh uses bash + symlinks)
- Python 3 (used by install.sh for settings.json merging)

---

## License

MIT
