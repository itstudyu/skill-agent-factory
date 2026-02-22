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

| Name | Type | Category | Version | Description | File Path | Last Modified |
|------|------|----------|---------|-------------|-----------|---------------|
| devops-arch-review | skill | devops | v1.0 | Architecture and coding standards review. Use when the user asks to check code structure, folder layout, naming conve... | skills/devops-arch-review/SKILL.md | 2026-02-22 |
| devops-code-review | skill | devops | v1.0 | Code quality and logic review. Run after code is written. Verifies AI-generated code has no bugs, logic errors, memor... | skills/devops-code-review/SKILL.md | 2026-02-22 |
| devops-frontend-review | skill | devops | v1.0 | Frontend pixel-perfect review. Run after frontend code is written. Compares implementation against provided screensho... | skills/devops-frontend-review/SKILL.md | 2026-02-22 |
| devops-git-commit | skill | devops | v1.0 | Git commit with branch strategy. Run at the END of every development task. Creates a feature branch if needed, writes... | skills/devops-git-commit/SKILL.md | 2026-02-22 |
| devops-japanese-comments | skill | devops | v1.0 | Enforce Japanese language in code comments and log messages. Run after code review. Converts all English comments to ... | skills/devops-japanese-comments/SKILL.md | 2026-02-22 |
| devops-requirements | skill | devops | v1.0 | Development requirements gathering. Use at the START of every development request before writing any code. Triggers o... | skills/devops-requirements/SKILL.md | 2026-02-22 |
| devops-safety-check | skill | devops | v1.0 | Lightweight code security check. Run after code is written. Checks for secrets, vulnerable dependencies, SQL injectio... | skills/devops-safety-check/SKILL.md | 2026-02-22 |
| devops-skill-eval | skill | devops | v1.0 | Evaluates the quality and correctness of a skill by running test scenarios against it. Use when the user wants to tes... | skills/devops-skill-eval/SKILL.md | 2026-02-22 |
| devops-test-gen | skill | devops | v1.0 | Automatically generate unit tests for newly written code. Run after code review is clean. Generates tests appropriate... | skills/devops-test-gen/SKILL.md | 2026-02-22 |
| devops-version-check | skill | devops | v1.0 | Language version and dependency safety check. Verifies code uses correct syntax for the project's language version, A... | skills/devops-version-check/SKILL.md | 2026-02-22 |
| figma-code-sync | skill | figma | v1.0 | Verifies that the implemented code matches the Figma design mapping. Use when you want to validate the implementation... | skills/figma-code-sync/SKILL.md | 2026-02-22 |
| figma-design-analyzer | skill | figma | v1.0 | Analyzes Figma designs to produce a frontend implementation blueprint before coding begins. Captures screenshots of e... | skills/figma-design-analyzer/SKILL.md | 2026-02-22 |
| figma-design-token-extractor | skill | figma | v1.0 | Extracts design tokens (colors, fonts, spacing, shadows, border-radius, etc.) from Figma files via Figma MCP and conv... | skills/figma-design-token-extractor/SKILL.md | 2026-02-22 |
| figma-framework-figma-mapper | skill | figma | v1.0 | Maps UI framework components to Figma design components. Supports PrimeFaces as a preset (with Figma UI Kit). Also su... | skills/figma-framework-figma-mapper/SKILL.md | 2026-02-22 |
| figma-responsive-validator | skill | figma | v1.0 | Validates responsive design compliance of frontend code across Mobile, Tablet, and Desktop breakpoints. Performs stat... | skills/figma-responsive-validator/SKILL.md | 2026-02-22 |
| devops-pipeline | agent | devops | v1.0 | Full development pipeline orchestrator. Use proactively for ALL development requests — any time the user asks to impl... | agents/devops-pipeline.md | 2026-02-22 |
| figma-to-code | agent | figma | v1.0 | Converts Figma designs into production-ready frontend code. Use proactively when the user wants to generate code from... | agents/figma-to-code.md | 2026-02-22 |
| project-onboarding | agent | project | v1.0 | Project onboarding agent. Auto-detects existing vs new projects, analyzes code patterns, and generates project-contex... | agents/project-onboarding.md | 2026-02-22 |
| skill-router | agent | skill | v1.0 | Central skill router for all user requests. Uses 2-phase matching — registry.md for fast category filtering, then ful... | agents/skill-router.md | 2026-02-22 |

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

- **Total assets**: 19
- **Skills**: 15
  - Devops (10): devops-arch-review, devops-code-review, devops-frontend-review, devops-git-commit, devops-japanese-comments, devops-requirements, devops-safety-check, devops-skill-eval, devops-test-gen, devops-version-check
  - Figma (5): figma-code-sync, figma-design-analyzer, figma-design-token-extractor, figma-framework-figma-mapper, figma-responsive-validator
- **Agents**: 4 (devops-pipeline, figma-to-code, project-onboarding, skill-router)
- **Plugins**: 0
- **Hooks**: 0
- **MCP Servers**: 0
- **Output Styles**: 0

*Last updated: 2026-02-22*