# Skill & Agent Factory

A centralized workspace for creating, managing, and using **Claude Code skills and agents**, organized as plugin bundles.

When you give Claude Code a task, it automatically selects the right skill or agent based on what you're asking — and runs every development request through a **mandatory quality pipeline**.

---

## What's Inside

```
skill-agent-factory/
├── CLAUDE.md              ← Master instructions (auto-read by Claude Code)
├── README.md              ← This file
├── Makefile               ← Dev commands: make install / lint / validate / graph
├── registry.md            ← Master registry of ALL assets (auto-updated)
├── install.sh             ← Global installer: symlinks + orphan cleanup + lint
├── plugins/               ← ALL skills & agents live here (plugin-grouped)
│   ├── devops/            ← DevOps plugin (10 skills + devops-pipeline agent)
│   │   ├── plugin.json    ← Plugin manifest + team membership declarations
│   │   ├── agents/devops-pipeline.md
│   │   └── skills/{skill-name}/
│   │       ├── metadata.md    ← Tier 1: routing (tags, use-when, model) — always loaded
│   │       ├── SKILL.md       ← Tier 2: full instructions — loaded only when selected
│   │       └── resources/     ← Tier 3: checklists, templates — loaded on-demand
│   ├── figma/             ← Figma plugin (5 skills + figma-to-code agent)
│   │   ├── plugin.json
│   │   ├── agents/figma-to-code.md
│   │   └── skills/{skill-name}/
│   └── project/           ← Project plugin (project-onboarding agent)
│       ├── plugin.json
│       └── agents/project-onboarding.md
├── scripts/               ← Automation utilities (also available via Makefile)
│   ├── sync-registry.py   ← Auto-syncs registry.md + README.md from metadata.md
│   ├── lint-skills.py     ← Quality checker: frontmatter, refs, teams, dep chains
│   └── dep-graph.py       ← Dependency tree visualizer + reverse lookup
├── standards/             ← Global coding rules
│   └── CODING-STANDARDS.md
└── _docs/                 ← Official Claude Code reference docs
```

---

## 3-Tier Skill Architecture

Each skill uses progressive disclosure to minimize context load:

| Tier | File | When Loaded |
|------|------|-------------|
| **Tier 1** | `metadata.md` | **Always** — lightweight routing (~10 lines) |
| **Tier 2** | `SKILL.md` | Only when the skill is selected |
| **Tier 3** | `resources/` | On-demand — checklists, templates, examples |

This means Claude only reads what it needs, keeping context lean.

---

## Agent Teams

Skills across plugins are grouped into **teams** for coordinated execution. Team membership is declared in each `plugin.json` and validated by `make lint`.

| Team | Execution | Skills |
|------|-----------|--------|
| `review-team` | **Parallel** | code-review + arch-review + safety-check + responsive-validator |
| `quality-team` | **Sequential** | test-gen + japanese-comments + version-check |
| `commit-team` | **Sequential** | git-commit |
| `feature-team` | **Gated** | requirements → design-analyzer → implementation |

When a new plugin is added, declare its team membership in `plugin.json` before creating skill files. `make lint` will catch invalid team names or broken references automatically.

> **Planned:** `plugins/teams/agents/` orchestrators (implement when ≥ 3 plugins registered per team)

---

## DevOps Pipeline (Mandatory for All Development)

Every development request automatically runs through this pipeline:

```
[0] Project Context Check    ← Verifies project-context/ exists (runs project-onboarding if not)
[1] Requirements Gathering   ← Hard gate — reads project-context/, asks if unclear
         ↓  (Figma URL? → figma-to-code agent handles full Figma workflow)
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

Orchestrated by `plugins/devops/agents/devops-pipeline.md`.

---

## Global Coding Standards

Applied to every file, regardless of language or category. Full details in `standards/CODING-STANDARDS.md`.

| Rule | Description |
|------|-------------|
| **File header** | First line of every source file: one-line Japanese summary comment |
| **Function max 30 lines** | Split if exceeded; comment if unavoidable exception |
| **One file, one responsibility** | No unrelated logic in the same file |
| **Commit confirmation** | Always shows branch/files/message — waits for user approval |
| **Comments in Japanese** | All code comments and log messages in Japanese |
| **Commit messages in Japanese** | 1–4 lines, key content only |
| **Branch naming** | `feature/{TaskNumber}/{Name}` — never commits to master without explicit instruction |

---

## Quick Start (Makefile)

```bash
make install      # symlink skills/agents to ~/.claude/
make lint         # check skill/agent quality
make lint-strict  # warnings also count as errors
make sync         # update registry.md and README.md
make graph        # show full dependency tree
make check        # check dependency issues only
make validate     # lint + sync + check (run before committing)
make help         # show all commands
```

---

## Installation

### Method 1 — Global Symlink (recommended)

Run once after cloning. Makes all skills/agents available in every Claude Code project.

```bash
git clone https://github.com/ysjapan97/skill-agent-factory ~/skill-agent-factory
cd ~/skill-agent-factory
chmod +x install.sh
./install.sh
```

**To update after adding new skills:**
```bash
git pull && ./install.sh
```

**To uninstall:**
```bash
./install.sh --uninstall
```

---

### Method 2 — Git Submodule (per-project)

Embed the factory inside a project so it travels with the repo.

```bash
cd my-project
git submodule add https://github.com/ysjapan97/skill-agent-factory
```

Add to `.claude/settings.json`:
```json
{ "pluginDirs": ["./skill-agent-factory"] }
```

**When a teammate clones:**
```bash
git clone --recurse-submodules https://github.com/you/my-project
```

---

### Method 3 — Plugin Dir (per-session)

```bash
claude --plugin-dir ~/path/to/skill-agent-factory
```

---

## Current Skills & Agents

### Devops Plugin Skills

| Skill | Model | Tags | Purpose |
|-------|-------|------|---------|
| `devops-arch-review` | sonnet | `review`, `architecture`, `structure`, `standards`, `naming`, `patterns` | User asks to check code structure, folder layout, naming conventions, error hand |
| `devops-code-review` | sonnet | `review`, `code`, `quality`, `bugs`, `logic`, `performance` | Run after code is written. User asks to review code, check for bugs, logic error |
| `devops-frontend-review` | sonnet | `review`, `frontend`, `ui`, `pixel-perfect`, `screenshot`, `design-match` | Run after frontend code is written. User provides a screenshot, image, or Figma  |
| `devops-git-commit` | haiku | `git`, `commit`, `branch`, `version-control` | Run at the END of every development task. User wants to commit code, create a br |
| `devops-japanese-comments` | haiku | `japanese`, `comments`, `logs`, `localization`, `i18n` | Run after code review. User wants to enforce Japanese in comments/logs, convert  |
| `devops-requirements` | sonnet | `requirements`, `planning`, `spec`, `feature`, `analysis` | Run at the START of every development request, before writing any code. User wan |
| `devops-safety-check` | haiku | `security`, `safety`, `secrets`, `vulnerability`, `sql-injection`, `xss` | Run after code is written. Quick security scan for secrets, SQL injection, XSS,  |
| `devops-skill-eval` | sonnet | `eval`, `quality`, `skill`, `validate`, `test`, `benchmark` | User wants to test a skill before deploying, validate a newly created skill, or  |
| `devops-test-gen` | sonnet | `test`, `generate`, `unit-test`, `coverage`, `jest`, `pytest` | Run after code review is clean. User wants to generate unit tests for new code.  |
| `devops-version-check` | haiku | `version`, `dependency`, `package`, `compatibility`, `deprecated` | User wants to verify code syntax for the project language version, check depreca |

### Figma Plugin Skills

| Skill | Model | Tags | Purpose |
|-------|-------|------|---------|
| `figma-code-sync` | sonnet | `figma`, `sync`, `verify`, `design-match`, `implementation`, `validate` | User wants to validate that implemented code matches the Figma design, check for |
| `figma-design-analyzer` | sonnet | `figma`, `design`, `analyze`, `blueprint`, `frontend`, `planning`, `implementation-plan` | Before coding begins. User wants to analyze a Figma design and produce a fronten |
| `figma-design-token-extractor` | sonnet | `figma`, `design-token`, `colors`, `typography`, `css`, `scss`, `extract` | User wants to extract design tokens from Figma (colors, fonts, spacing, shadows) |
| `figma-framework-figma-mapper` | sonnet | `figma`, `framework`, `component`, `mapping`, `ui-kit`, `primefaces` | User wants to map UI framework components (PrimeFaces, custom) to Figma design c |
| `figma-responsive-validator` | haiku | `figma`, `responsive`, `validate`, `mobile`, `layout`, `breakpoint`, `tablet` | User wants to validate responsive design across Mobile, Tablet, Desktop breakpoi |

### Agents

| Agent | Plugin | Model | Purpose |
|-------|--------|-------|---------|
| `devops-pipeline` | devops | sonnet | Development pipeline orchestrator. Called by skill-router for development tasks. |
| `figma-to-code` | figma | opus | Converts Figma designs into production-ready frontend code. Use proactively when |
| `project-onboarding` | project | sonnet | Project onboarding agent. Auto-detects existing vs new projects, analyzes code p |


## Adding a New Skill

### 1. Create the skill directory
```bash
mkdir -p plugins/{plugin}/skills/{category}-{skill-name}
```

### 2. Write `metadata.md` (Tier 1 — routing)
```yaml
---
name: backend-my-skill
category: backend
tags: [backend, generate, code, api]
model: sonnet
allowed-tools: Read, Write, Bash
version: v1.0
use-when: >
  User wants to... Triggers: "키워드", "keyword", "キーワード"
---
```

### 3. Write `SKILL.md` (Tier 2 — instructions)
```yaml
---
name: backend-my-skill
version: v1.0
description: What this skill does.
tags: [backend, generate, code, api]
allowed-tools: Read, Write, Bash
---

# Backend My Skill

## STEP_1 — ...
```

### 4. (Optional) Add `resources/` (Tier 3 — on-demand)
```
plugins/{plugin}/skills/{skill-name}/resources/
├── checklist.md
└── template.md
```

### 5. Declare team membership in `plugin.json`
```json
"teams": {
  "review-team": ["backend-my-skill"]
}
```

### 6. Validate and sync
```bash
make validate   # lint + sync + dep-check
./install.sh    # re-link to ~/.claude/
```

---

## Adding a New Plugin

```bash
mkdir -p plugins/{name}/{skills,agents}
```

Create `plugins/{name}/plugin.json`:
```json
{
  "name": "{name}",
  "description": "...",
  "version": "1.0.0",
  "skills": [],
  "agents": [],
  "teams": {
    "review-team": [],
    "feature-team": []
  }
}
```

Then add skills following the steps above.

---

## Automation Scripts

| Command | What It Does |
|---------|-------------|
| `make validate` | lint + sync + dep-check (run before every commit) |
| `make lint` | Frontmatter, teams refs, dep chains, step structure |
| `make lint-strict` | Same but warnings = errors |
| `make sync` | Updates registry.md + README.md from metadata.md files |
| `make graph` | Full dependency tree |
| `make check` | Dependency issues only |
| `python3 scripts/dep-graph.py --reverse <skill>` | What breaks if this skill is deleted |

---

## Versioning

All assets use `version: vMAJOR.MINOR` in their frontmatter.

| Change | Bump |
|--------|------|
| Breaking (rename, remove steps, change output format) | MAJOR (v1.0 → v2.0) |
| Non-breaking (new steps, improved instructions, new tags) | MINOR (v1.0 → v1.1) |
| Spelling / formatting only | none |

Run `make sync` after bumping — registry.md auto-reflects the new version.

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
| `_docs/agent-teams.md` | Multi-agent coordination |

---

## Requirements

- [Claude Code](https://claude.ai/code) v1.0.33 or later
- macOS / Linux (install.sh uses bash + symlinks)
- Python 3 (scripts/\*.py)
- GNU Make (Makefile)

---

## License

MIT
