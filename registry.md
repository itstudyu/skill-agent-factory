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
| devops-arch-review | skill | devops | sonnet | `review`, `architecture`, `structure`, `standards`, `naming`, `patterns` | v1.0 | User asks to check code structure, folder layout, naming conventions, error handling patterns, tr... | plugins/devops/skills/devops-arch-review/SKILL.md | 2026-03-01 |
| devops-code-review | skill | devops | sonnet | `review`, `code`, `quality`, `bugs`, `logic`, `performance` | v1.0 | Run after code is written. User asks to review code, check for bugs, logic errors, memory leaks, ... | plugins/devops/skills/devops-code-review/SKILL.md | 2026-03-01 |
| devops-frontend-review | skill | devops | sonnet | `review`, `frontend`, `ui`, `pixel-perfect`, `screenshot`, `design-match` | v1.1 | Run after frontend code is written as part of devops-pipeline. User provides a screenshot, image,... | plugins/devops/skills/devops-frontend-review/SKILL.md | 2026-03-01 |
| devops-git-commit | skill | devops | haiku | `git`, `commit`, `branch`, `version-control` | v1.0 | Run at the END of every development task. User wants to commit code, create a branch, or finalize... | plugins/devops/skills/devops-git-commit/SKILL.md | 2026-03-01 |
| devops-japanese-comments | skill | devops | haiku | `japanese`, `comments`, `logs`, `localization`, `i18n` | v1.0 | Run after code review. User wants to enforce Japanese in comments/logs, convert English comments ... | plugins/devops/skills/devops-japanese-comments/SKILL.md | 2026-03-01 |
| devops-requirements | skill | devops | sonnet | `requirements`, `planning`, `spec`, `feature`, `analysis` | v1.0 | Run at the START of every development request, before writing any code. User wants to implement a... | plugins/devops/skills/devops-requirements/SKILL.md | 2026-03-01 |
| devops-safety-check | skill | devops | haiku | `security`, `safety`, `secrets`, `vulnerability`, `sql-injection`, `xss` | v1.0 | Run after code is written. Quick security scan for secrets, SQL injection, XSS, vulnerable depend... | plugins/devops/skills/devops-safety-check/SKILL.md | 2026-03-01 |
| devops-skill-eval | skill | devops | sonnet | `eval`, `quality`, `skill`, `validate`, `test`, `benchmark` | v1.0 | User wants to test a skill before deploying, validate a newly created skill, or benchmark skill p... | plugins/devops/skills/devops-skill-eval/SKILL.md | 2026-03-01 |
| devops-test-gen | skill | devops | sonnet | `test`, `generate`, `unit-test`, `coverage`, `jest`, `pytest` | v1.0 | Run after code review is clean. User wants to generate unit tests for new code. Detects framework... | plugins/devops/skills/devops-test-gen/SKILL.md | 2026-03-01 |
| devops-version-check | skill | devops | haiku | `version`, `dependency`, `package`, `compatibility`, `deprecated` | v1.0 | User wants to verify code syntax for the project language version, check deprecated APIs, or vali... | plugins/devops/skills/devops-version-check/SKILL.md | 2026-03-01 |
| figma-code-sync | skill | figma | sonnet | `figma`, `sync`, `verify`, `design-match`, `implementation`, `validate` | v1.0 | User wants to validate that implemented code matches the Figma design, check for missing componen... | plugins/figma/skills/figma-code-sync/SKILL.md | 2026-03-01 |
| figma-component-inventory | skill | figma | sonnet | `figma`, `component`, `inventory`, `catalog`, `scan`, `audit`, `gap-analysis` | v1.0 | User wants to scan and catalog all components in a Figma file, perform a gap analysis between Fig... | plugins/figma/skills/figma-component-inventory/SKILL.md | 2026-03-01 |
| figma-design-analyzer | skill | figma | sonnet | `figma`, `design`, `analyze`, `blueprint`, `frontend`, `planning`, `implementation-plan` | v1.0 | Before coding begins. User wants to analyze a Figma design and produce a frontend implementation ... | plugins/figma/skills/figma-design-analyzer/SKILL.md | 2026-03-01 |
| figma-design-token-extractor | skill | figma | sonnet | `figma`, `design-token`, `colors`, `typography`, `css`, `scss`, `extract` | v1.0 | User wants to extract design tokens from Figma (colors, fonts, spacing, shadows) and convert to C... | plugins/figma/skills/figma-design-token-extractor/SKILL.md | 2026-03-01 |
| figma-framework-figma-mapper | skill | figma | sonnet | `figma`, `framework`, `component`, `mapping`, `ui-kit`, `primefaces` | v1.0 | User wants to map UI framework components (PrimeFaces, custom) to Figma design components. Genera... | plugins/figma/skills/figma-framework-figma-mapper/SKILL.md | 2026-03-01 |
| figma-project-context | skill | figma | sonnet | `figma`, `project`, `context`, `setup`, `framework`, `convention`, `init` | v1.0 | Before any Figma-to-code workflow begins. User wants to analyze the project structure and generat... | plugins/figma/skills/figma-project-context/SKILL.md | 2026-03-01 |
| figma-responsive-validator | skill | figma | sonnet | `figma`, `responsive`, `validate`, `mobile`, `layout`, `breakpoint`, `tablet` | v1.0 | User wants to validate responsive design across Mobile, Tablet, Desktop breakpoints. Detects layo... | plugins/figma/skills/figma-responsive-validator/SKILL.md | 2026-03-01 |
| pm-confidence-check | skill | pm | sonnet | `pm`, `confidence`, `pre-check`, `assessment`, `quality-gate` | v1.0 | Run BEFORE starting any implementation. Assesses confidence level to prevent wrong-direction work... | plugins/pm/skills/pm-confidence-check/SKILL.md | 2026-03-01 |
| pm-reflexion | skill | pm | sonnet | `pm`, `reflexion`, `error-learning`, `mistake`, `prevention`, `pdca` | v1.0 | Run when errors occur or after mistake detection. Records errors with root cause analysis, checks... | plugins/pm/skills/pm-reflexion/SKILL.md | 2026-03-01 |
| pm-self-check | skill | pm | sonnet | `pm`, `self-check`, `validation`, `post-check`, `evidence`, `hallucination` | v1.0 | Run AFTER implementation is complete. Validates work with evidence-based checks to prevent halluc... | plugins/pm/skills/pm-self-check/SKILL.md | 2026-03-01 |
| vertx-api-caller | skill | vertx | sonnet | `vertx`, `eventbus`, `frontend`, `javascript`, `sockjs`, `api-call` | v1.0 | フロントエンド（JavaScript/TypeScript）から Vert.x EventBus を呼び出すコードを書きたいとき。SockJS + EventBus クライアントを使った API... | plugins/vertx/skills/vertx-api-caller/SKILL.md | 2026-03-01 |
| vertx-eventbus-register | skill | vertx | sonnet | `vertx`, `java`, `java7`, `eventbus`, `handler`, `register`, `verticle` | v1.0 | Vert.x EventBus に新しいエンドポイント（ハンドラ）を追加したいとき。Java 7 の匿名内部クラス形式でハンドラを登録する。既存の Verticle に handler を追加す... | plugins/vertx/skills/vertx-eventbus-register/SKILL.md | 2026-03-01 |
| vertx-repo-analyzer | skill | vertx | sonnet | `vertx`, `java`, `eventbus`, `verticle`, `analysis`, `repo` | v1.0 | Vert.x プロジェクトの構造を把握したいとき。EventBus のエンドポイント一覧を確認したいとき。既存の Verticle クラスを調べたいとき。新しいエンドポイントを追加する前の事前調... | plugins/vertx/skills/vertx-repo-analyzer/SKILL.md | 2026-03-01 |
| devops-pipeline | agent | devops | sonnet | — | v1.0 | Development pipeline orchestrator. Automatically invoked by CLAUDE.md for all development tasks. ... | plugins/devops/agents/devops-pipeline.md | 2026-03-01 |
| figma-designer | agent | figma | opus | — | v1.0 | Creates new Figma designs using the Talk to Figma MCP. Reads project context and design tokens to... | plugins/figma/agents/figma-designer.md | 2026-03-01 |
| figma-to-code | agent | figma | opus | — | v1.0 | Converts Figma designs into production-ready frontend code. Use proactively when the user wants t... | plugins/figma/agents/figma-to-code.md | 2026-03-01 |
| pm-pipeline | agent | pm | sonnet | — | v1.0 | PM (Project Management) pipeline orchestrator. Wraps around the devops-pipeline with pre-check an... | plugins/pm/agents/pm-pipeline.md | 2026-03-01 |
| project-onboarding | agent | project | sonnet | — | v1.0 | Project onboarding agent. Auto-detects existing vs new projects, analyzes code patterns, and gene... | plugins/project/agents/project-onboarding.md | 2026-03-01 |
| vertx-pipeline | agent | vertx | sonnet | `vertx`, `pipeline`, `orchestrator`, `eventbus` | v1.0 | Vert.x EventBus development pipeline orchestrator. Runs the eventbus-team in sequence — repo-anal... | plugins/vertx/agents/vertx-pipeline.md | 2026-03-01 |

---

## Asset Types Reference

| Type | Format | Where to Place |
|------|--------|----------------|
| `skill` | `metadata.md` + `SKILL.md` | `plugins/{plugin}/skills/{name}/` |
| `agent` | `.md` with frontmatter | `plugins/{plugin}/agents/{name}.md` |
| `plugin` | Plugin directory with `.claude-plugin/plugin.json` | Project root or separate repo |
| `hook` | JSON config in `hooks/hooks.json` | Project `.claude/settings.json` or plugin `hooks/` |
| `mcp` | `claude mcp add` command or `.mcp.json` | Project `.mcp.json` or user `~/.claude.json` |
| `output-style` | `.md` with frontmatter | `~/.claude/output-styles/` or `.claude/output-styles/` |

---

## Statistics

- **Total assets**: 29
- **Skills**: 23
  - plugin/devops (10): devops-arch-review, devops-code-review, devops-frontend-review, devops-git-commit, devops-japanese-comments, devops-requirements, devops-safety-check, devops-skill-eval, devops-test-gen, devops-version-check
  - plugin/figma (7): figma-code-sync, figma-component-inventory, figma-design-analyzer, figma-design-token-extractor, figma-framework-figma-mapper, figma-project-context, figma-responsive-validator
  - plugin/pm (3): pm-confidence-check, pm-reflexion, pm-self-check
  - plugin/vertx (3): vertx-api-caller, vertx-eventbus-register, vertx-repo-analyzer
- **Agents**: 6 (devops-pipeline, figma-designer, figma-to-code, pm-pipeline, project-onboarding, vertx-pipeline)
- **Plugins**: 4 (devops, figma, pm, vertx)
- **Hooks**: 0
- **MCP Servers**: 0
- **Output Styles**: 0

*Last updated: 2026-03-01*