# Asset Registry — Skill & Agent Factory

> Master registry of all skills, agents, plugins, hooks, MCP servers, and output styles.
> **Always update this file after creating or modifying any asset.**

---

## How to Use This Registry

1. **Before creating**: search this table for similar existing assets
2. **If similar exists**: propose an update and increment the version
3. **If new**: create the asset and add a new row here
4. **Version format**: `v1.0`, `v1.1`, `v2.0` (major.minor)

---

## Registry Table

| Name | Type | Plugin | Model | Tags | Version | Description | File Path | Last Modified |
|------|------|--------|-------|------|---------|-------------|-----------|---------------|
| devops-arch-review | skill | devops | sonnet | `review`, `architecture`, `structure`, `standards`, `naming`, `patterns` | v1.0 | User asks to check code structure, folder layout, naming conventions, error handling patterns, tr... | plugins/devops/skills/devops-arch-review/SKILL.md | 2026-02-23 |
| devops-code-review | skill | devops | sonnet | `review`, `code`, `quality`, `bugs`, `logic`, `performance` | v1.0 | Run after code is written. User asks to review code, check for bugs, logic errors, memory leaks, ... | plugins/devops/skills/devops-code-review/SKILL.md | 2026-02-23 |
| devops-frontend-review | skill | devops | sonnet | `review`, `frontend`, `ui`, `pixel-perfect`, `screenshot`, `design-match` | v1.0 | Run after frontend code is written. User provides a screenshot, image, or Figma link to compare a... | plugins/devops/skills/devops-frontend-review/SKILL.md | 2026-02-23 |
| devops-git-commit | skill | devops | haiku | `git`, `commit`, `branch`, `version-control` | v1.0 | Run at the END of every development task. User wants to commit code, create a branch, or finalize... | plugins/devops/skills/devops-git-commit/SKILL.md | 2026-02-23 |
| devops-japanese-comments | skill | devops | haiku | `japanese`, `comments`, `logs`, `localization`, `i18n` | v1.0 | Run after code review. User wants to enforce Japanese in comments/logs, convert English comments ... | plugins/devops/skills/devops-japanese-comments/SKILL.md | 2026-02-23 |
| devops-requirements | skill | devops | sonnet | `requirements`, `planning`, `spec`, `feature`, `analysis` | v1.0 | Run at the START of every development request, before writing any code. User wants to implement a... | plugins/devops/skills/devops-requirements/SKILL.md | 2026-02-23 |
| devops-safety-check | skill | devops | haiku | `security`, `safety`, `secrets`, `vulnerability`, `sql-injection`, `xss` | v1.0 | Run after code is written. Quick security scan for secrets, SQL injection, XSS, vulnerable depend... | plugins/devops/skills/devops-safety-check/SKILL.md | 2026-02-23 |
| devops-skill-eval | skill | devops | sonnet | `eval`, `quality`, `skill`, `validate`, `test`, `benchmark` | v1.0 | User wants to test a skill before deploying, validate a newly created skill, or benchmark skill p... | plugins/devops/skills/devops-skill-eval/SKILL.md | 2026-02-23 |
| devops-test-gen | skill | devops | sonnet | `test`, `generate`, `unit-test`, `coverage`, `jest`, `pytest` | v1.0 | Run after code review is clean. User wants to generate unit tests for new code. Detects framework... | plugins/devops/skills/devops-test-gen/SKILL.md | 2026-02-23 |
| devops-version-check | skill | devops | haiku | `version`, `dependency`, `package`, `compatibility`, `deprecated` | v1.0 | User wants to verify code syntax for the project language version, check deprecated APIs, or vali... | plugins/devops/skills/devops-version-check/SKILL.md | 2026-02-23 |
| figma-code-sync | skill | figma | sonnet | `figma`, `sync`, `verify`, `design-match`, `implementation`, `validate` | v1.0 | User wants to validate that implemented code matches the Figma design, check for missing componen... | plugins/figma/skills/figma-code-sync/SKILL.md | 2026-02-23 |
| figma-design-analyzer | skill | figma | sonnet | `figma`, `design`, `analyze`, `blueprint`, `frontend`, `planning`, `implementation-plan` | v1.0 | Before coding begins. User wants to analyze a Figma design and produce a frontend implementation ... | plugins/figma/skills/figma-design-analyzer/SKILL.md | 2026-02-23 |
| figma-design-token-extractor | skill | figma | sonnet | `figma`, `design-token`, `colors`, `typography`, `css`, `scss`, `extract` | v1.0 | User wants to extract design tokens from Figma (colors, fonts, spacing, shadows) and convert to C... | plugins/figma/skills/figma-design-token-extractor/SKILL.md | 2026-02-23 |
| figma-framework-figma-mapper | skill | figma | sonnet | `figma`, `framework`, `component`, `mapping`, `ui-kit`, `primefaces` | v1.0 | User wants to map UI framework components (PrimeFaces, custom) to Figma design components. Genera... | plugins/figma/skills/figma-framework-figma-mapper/SKILL.md | 2026-02-23 |
| figma-responsive-validator | skill | figma | haiku | `figma`, `responsive`, `validate`, `mobile`, `layout`, `breakpoint`, `tablet` | v1.0 | User wants to validate responsive design across Mobile, Tablet, Desktop breakpoints. Detects layo... | plugins/figma/skills/figma-responsive-validator/SKILL.md | 2026-02-23 |
| devops-pipeline | agent | devops | sonnet | — | v1.0 | Development pipeline orchestrator. Called by skill-router for development tasks. Trigger directly... | plugins/devops/agents/devops-pipeline.md | 2026-02-23 |
| figma-to-code | agent | figma | opus | — | v1.0 | Converts Figma designs into production-ready frontend code. Use proactively when the user wants t... | plugins/figma/agents/figma-to-code.md | 2026-02-23 |
| project-onboarding | agent | project | sonnet | — | v1.0 | Project onboarding agent. Auto-detects existing vs new projects, analyzes code patterns, and gene... | plugins/project/agents/project-onboarding.md | 2026-02-23 |

---

## Asset Types Reference

| Type | Format | Where to Place |
|------|--------|----------------|
| `skill` | `SKILL.md` with frontmatter | `{category}/skills/{name}/SKILL.md` |
| `agent` | `.md` with frontmatter | `{category}/agents/{name}.md` |
| `plugin` | Plugin directory with `.claude-plugin/plugin.json` | Project root or separate repo |
| `hook` | JSON config in `hooks/hooks.json` | Project `.claude/settings.json` or plugin `hooks/` |
| `mcp` | `claude mcp add` command or `.mcp.json` | Project `.mcp.json` or user `~/.claude.json` |
| `output-style` | `.md` with frontmatter | `~/.claude/output-styles/` or `.claude/output-styles/` |

---

## Statistics

- **Total assets**: 18
- **Skills**: 15
  - plugin/devops (10): devops-arch-review, devops-code-review, devops-frontend-review, devops-git-commit, devops-japanese-comments, devops-requirements, devops-safety-check, devops-skill-eval, devops-test-gen, devops-version-check
  - plugin/figma (5): figma-code-sync, figma-design-analyzer, figma-design-token-extractor, figma-framework-figma-mapper, figma-responsive-validator
- **Agents**: 3 (devops-pipeline, figma-to-code, project-onboarding)
- **Plugins**: 3 (devops, figma, project)
- **Hooks**: 0
- **MCP Servers**: 0
- **Output Styles**: 0

*Last updated: 2026-02-23*