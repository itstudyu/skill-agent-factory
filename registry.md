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

| Name | Type | Category | Tags | Version | Description | File Path | Last Modified |
|------|------|----------|------|---------|-------------|-----------|---------------|
| devops-arch-review | skill | devops | `devops`, `review`, `architecture`, `structure`, `standards` | v1.0 | Architecture and coding standards review. Use when the user asks to check code structure, folder ... | skills/devops-arch-review/SKILL.md | 2026-02-22 |
| devops-code-review | skill | devops | `devops`, `review`, `code`, `quality`, `bugs`, `logic` | v1.0 | Code quality and logic review. Run after code is written. Verifies AI-generated code has no bugs,... | skills/devops-code-review/SKILL.md | 2026-02-22 |
| devops-frontend-review | skill | devops | `devops`, `review`, `frontend`, `ui`, `pixel-perfect`, `screenshot` | v1.0 | Frontend pixel-perfect review. Run after frontend code is written. Compares implementation agains... | skills/devops-frontend-review/SKILL.md | 2026-02-22 |
| devops-git-commit | skill | devops | `devops`, `git`, `commit`, `branch`, `version-control` | v1.0 | Git commit with branch strategy. Run at the END of every development task. Creates a feature bran... | skills/devops-git-commit/SKILL.md | 2026-02-22 |
| devops-japanese-comments | skill | devops | `devops`, `japanese`, `comments`, `logs`, `localization` | v1.0 | Enforce Japanese language in code comments and log messages. Run after code review. Converts all ... | skills/devops-japanese-comments/SKILL.md | 2026-02-22 |
| devops-pr-description | skill | devops | — | v1.0 | DEPRECATED — このスキルは削除予定です。PR説明文の生成はdevops-git-commitスキルに統合されています。 | skills/devops-pr-description/SKILL.md | 2026-02-22 |
| devops-requirements | skill | devops | `devops`, `requirements`, `planning`, `spec`, `feature` | v1.0 | Development requirements gathering. Use at the START of every development request before writing ... | skills/devops-requirements/SKILL.md | 2026-02-22 |
| devops-safety-check | skill | devops | `devops`, `security`, `safety`, `secrets`, `vulnerability` | v1.0 | Lightweight code security check. Run after code is written. Checks for secrets, vulnerable depend... | skills/devops-safety-check/SKILL.md | 2026-02-22 |
| devops-skill-eval | skill | devops | `devops`, `eval`, `quality`, `skill`, `validate`, `test` | v1.0 | Evaluates the quality and correctness of a skill by running test scenarios against it. Use when t... | skills/devops-skill-eval/SKILL.md | 2026-02-22 |
| devops-test-gen | skill | devops | `devops`, `test`, `generate`, `unit-test`, `coverage` | v1.0 | Automatically generate unit tests for newly written code. Run after code review is clean. Generat... | skills/devops-test-gen/SKILL.md | 2026-02-22 |
| devops-version-check | skill | devops | `devops`, `version`, `dependency`, `package`, `compatibility` | v1.0 | Language version and dependency safety check. Verifies code uses correct syntax for the project's... | skills/devops-version-check/SKILL.md | 2026-02-22 |
| figma-code-sync | skill | figma | `figma`, `sync`, `verify`, `design-match`, `implementation` | v1.0 | Verifies that the implemented code matches the Figma design mapping. Use when you want to validat... | skills/figma-code-sync/SKILL.md | 2026-02-22 |
| figma-design-analyzer | skill | figma | `figma`, `design`, `analyze`, `blueprint`, `frontend`, `planning` | v1.0 | Analyzes Figma designs to produce a frontend implementation blueprint before coding begins. Captu... | skills/figma-design-analyzer/SKILL.md | 2026-02-22 |
| figma-design-token-extractor | skill | figma | `figma`, `design-token`, `colors`, `typography`, `css`, `extract` | v1.0 | Extracts design tokens (colors, fonts, spacing, shadows, border-radius, etc.) from Figma files vi... | skills/figma-design-token-extractor/SKILL.md | 2026-02-22 |
| figma-framework-figma-mapper | skill | figma | `figma`, `framework`, `component`, `mapping`, `ui-kit` | v1.0 | Maps UI framework components to Figma design components. Supports PrimeFaces as a preset (with Fi... | skills/figma-framework-figma-mapper/SKILL.md | 2026-02-22 |
| figma-responsive-validator | skill | figma | `figma`, `responsive`, `validate`, `mobile`, `layout`, `breakpoint` | v1.0 | Validates responsive design compliance of frontend code across Mobile, Tablet, and Desktop breakp... | skills/figma-responsive-validator/SKILL.md | 2026-02-22 |
| devops-pipeline | agent | devops | — | v1.0 | Development pipeline orchestrator. Called by skill-router for development tasks. Trigger directly... | agents/devops-pipeline.md | 2026-02-22 |
| figma-to-code | agent | figma | — | v1.0 | Converts Figma designs into production-ready frontend code. Use proactively when the user wants t... | agents/figma-to-code.md | 2026-02-22 |
| project-onboarding | agent | project | — | v1.0 | Project onboarding agent. Auto-detects existing vs new projects, analyzes code patterns, and gene... | agents/project-onboarding.md | 2026-02-22 |
| skill-router | agent | skill | — | v1.0 | PRIMARY ENTRY POINT for ALL user requests. Always invoke skill-router first — it analyzes intent ... | agents/skill-router.md | 2026-02-22 |

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

- **Total assets**: 20
- **Skills**: 16
  - Devops (11): devops-arch-review, devops-code-review, devops-frontend-review, devops-git-commit, devops-japanese-comments, devops-pr-description, devops-requirements, devops-safety-check, devops-skill-eval, devops-test-gen, devops-version-check
  - Figma (5): figma-code-sync, figma-design-analyzer, figma-design-token-extractor, figma-framework-figma-mapper, figma-responsive-validator
- **Agents**: 4 (devops-pipeline, figma-to-code, project-onboarding, skill-router)
- **Plugins**: 0
- **Hooks**: 0
- **MCP Servers**: 0
- **Output Styles**: 0

*Last updated: 2026-02-22*