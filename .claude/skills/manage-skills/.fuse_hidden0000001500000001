---
name: manage-skills
description: Analyzes session changes to detect verification skill drift. Dynamically discovers ALL skills across the project, creates new verify skills or updates existing ones, then manages CLAUDE.md.
disable-model-invocation: true
argument-hint: "[optional: specific skill name or area to focus on]"
---

<!-- セッション変更分析 — 全スキル・エージェント・スクリプトのドリフト検出・修正を担当 -->

# Session-Based Skill Maintenance

## Purpose

Analyzes changes in the current session to detect and fix drift across ALL project assets:

1. **Coverage gaps** — changed files not referenced by any skill
2. **Invalid references** — skills referencing deleted or moved files
3. **Missing checks** — new patterns/rules not covered by existing checks
4. **Stale values** — config values or detection commands that no longer match
5. **Cross-asset consistency** — teams, registry, pipeline referencing skills that exist

## When to Run

- After implementing a feature that introduces new patterns or rules
- When modifying existing skills and checking for consistency
- Before a PR to confirm skills cover changed areas
- When a verification run missed expected issues
- Periodically to align skills with codebase changes

## Registered Assets

<!-- 登録済み全アセット — スキル・エージェント・スクリプト・標準の完全インベントリ -->

### DevOps Plugin Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| `devops-safety-check` | `plugins/devops/skills/devops-safety-check/` | Secret scanning, injection patterns, dependency vulnerabilities |
| `devops-code-review` | `plugins/devops/skills/devops-code-review/` | Logic correctness, performance, memory efficiency, code quality |
| `devops-arch-review` | `plugins/devops/skills/devops-arch-review/` | Architecture, folder structure, naming conventions, duplication |
| `devops-japanese-comments` | `plugins/devops/skills/devops-japanese-comments/` | Japanese comment conversion for all source files |
| `devops-frontend-review` | `plugins/devops/skills/devops-frontend-review/` | Frontend pixel-perfect, responsive validation |
| `devops-version-check` | `plugins/devops/skills/devops-version-check/` | Language/library version compatibility |
| `devops-test-gen` | `plugins/devops/skills/devops-test-gen/` | Unit test generation (happy path, edge case, error case) |
| `devops-git-commit` | `plugins/devops/skills/devops-git-commit/` | Branch strategy, commit message format, staging rules |
| `devops-requirements` | `plugins/devops/skills/devops-requirements/` | Requirements gathering, project-context validation |
| `devops-skill-eval` | `plugins/devops/skills/devops-skill-eval/` | Skill quality evaluation (happy/edge/negative scenarios) |

### Figma Plugin Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| `figma-design-analyzer` | `plugins/figma/skills/figma-design-analyzer/` | Figma design analysis and blueprint generation |
| `figma-code-sync` | `plugins/figma/skills/figma-code-sync/` | Figma-to-code synchronization |
| `figma-design-token-extractor` | `plugins/figma/skills/figma-design-token-extractor/` | Design token extraction (colors, typography, spacing) |
| `figma-framework-figma-mapper` | `plugins/figma/skills/figma-framework-figma-mapper/` | Framework component mapping |
| `figma-responsive-validator` | `plugins/figma/skills/figma-responsive-validator/` | Responsive breakpoint validation |
| `figma-project-context` | `plugins/figma/skills/figma-project-context/` | Project context for Figma integration |
| `figma-component-inventory` | `plugins/figma/skills/figma-component-inventory/` | Component inventory management |

### Vert.x Plugin Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| `vertx-repo-analyzer` | `plugins/vertx/skills/vertx-repo-analyzer/` | Repository structure analysis for Vert.x projects |
| `vertx-eventbus-register` | `plugins/vertx/skills/vertx-eventbus-register/` | EventBus address registration |
| `vertx-api-caller` | `plugins/vertx/skills/vertx-api-caller/` | API caller generation from templates |

### Standalone Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| `devops-pr-description` | `skills/devops-pr-description/` | PR description generation |

### Agents

| Agent | Location | Purpose |
|-------|----------|---------|
| `devops-pipeline` | `plugins/devops/agents/devops-pipeline.md` | Development pipeline orchestration (quality gate) |
| `figma-to-code` | `plugins/figma/agents/figma-to-code.md` | Figma design to code conversion |
| `figma-designer` | `plugins/figma/agents/figma-designer.md` | Figma design workflow |
| `project-onboarding` | `plugins/project/agents/project-onboarding.md` | Project context setup |
| `vertx-pipeline` | `plugins/vertx/agents/vertx-pipeline.md` | Vert.x EventBus pipeline |
| `skill-router` | `agents/skill-router.md` | Skill routing and dispatch |

### Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `lint-skills.py` | `scripts/lint-skills.py` | Skill structure, frontmatter, references, circular dependency checks |
| `sync-registry.py` | `scripts/sync-registry.py` | registry.md and README.md auto-sync |
| `dep-graph.py` | `scripts/dep-graph.py` | Dependency graph visualization and cycle detection |

### Standards

| Standard | Location | Purpose |
|----------|----------|---------|
| `CODING-STANDARDS.md` | `standards/CODING-STANDARDS.md` | 10 global coding rules (Japanese headers, 30-line functions, etc.) |

## Workflow

### Step 1: Collect Session Changes

<!-- 変更ファイル収集 — git diff + fallback -->

Collect all files changed in the current session.

**Git repository:**

```bash
# Uncommitted changes (staged + unstaged + untracked)
git diff HEAD --name-only 2>/dev/null
git ls-files --others --exclude-standard 2>/dev/null

# All changes since branching from main/master
git diff main...HEAD --name-only 2>/dev/null || git diff master...HEAD --name-only 2>/dev/null
```

**Non-git fallback:**

```bash
find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' \
       -not -path '*/.claude/skills/*' -newer .claude/skills/manage-skills/SKILL.md \
       2>/dev/null | head -50
```

If both methods fail, ask the user for a list of changed files.

Merge into a deduplicated list. If an optional argument specifies a skill name or area, filter to relevant files only.

**Display:** Group files by top-level directory:

```markdown
## Session Changes Detected

**N files changed in this session:**

| Directory | Files |
|-----------|-------|
| plugins/devops/skills | `devops-safety-check/SKILL.md` |
| plugins/figma/skills | `figma-code-sync/SKILL.md` |
| plugins/vertx/skills | `vertx-api-caller/SKILL.md` |
| scripts | `lint-skills.py` |
| standards | `CODING-STANDARDS.md` |
```

### Step 2: Dynamic Asset Discovery & File Mapping

<!-- 動的アセット探索 — 全スキル・エージェント・スクリプトを自動検出 -->

#### Sub-step 2a: Auto-discover ALL assets

**Discover from the file system directly, covering all locations:**

```bash
# Plugin skills (devops, figma, vertx)
ls -d plugins/*/skills/*/SKILL.md 2>/dev/null

# Plugin agents
ls plugins/*/agents/*.md 2>/dev/null

# Standalone skills
ls -d skills/*/SKILL.md 2>/dev/null

# Standalone agents
ls agents/*.md 2>/dev/null

# Meta skills (verify-* and manage-skills)
ls -d .claude/skills/*/SKILL.md 2>/dev/null

# Scripts
ls scripts/*.py 2>/dev/null

# Standards
ls standards/*.md 2>/dev/null
```

For each discovered asset, read its SKILL.md/metadata.md and extract file path patterns from:

1. **Related Files** section — parse table for file paths and glob patterns
2. **Workflow** section — extract file paths from grep/glob/read commands
3. **metadata.md requires** field — dependency references

Compare discovered assets against the **Registered Assets** tables above. Report any discrepancies (new assets not registered, registered assets missing from filesystem).

#### Sub-step 2b: Match changed files to assets

For each changed file from Step 1, match against discovered asset patterns. A file matches an asset if:

- It is the asset's own SKILL.md, metadata.md, or resource file
- It matches the asset's cover file pattern or referenced directories
- It matches a regex/string pattern used in the asset's detection commands

#### Sub-step 2c: Display mapping

```markdown
### File → Asset Mapping

| Asset | Trigger Files (changed) | Action |
|-------|------------------------|--------|
| devops-safety-check | `SKILL.md` (self) | CHECK |
| devops-pipeline | `devops-pipeline.md` (self) | CHECK |
| lint-skills.py | `lint-skills.py` (self) | CHECK |
| (no asset) | `new-file.ts` | UNCOVERED |
```

### Step 3: Coverage Gap Analysis for Affected Assets

<!-- カバレッジギャップ分析 — 影響アセットの検査漏れを検出 -->

For each AFFECTED asset (one with matched changed files), read the full content and check:

1. **Missing file references** — changed files related to this asset's domain not listed in Related Files?
2. **Stale detection commands** — do grep/glob patterns still match current file structure? Run sample commands to test.
3. **Uncovered new patterns** — read changed files and identify new rules, configs, or patterns the asset doesn't check.
4. **Dangling references** — files listed in Related Files that no longer exist in the codebase?
5. **Changed values** — specific values the asset checks that were modified?
6. **Cross-reference integrity** — does the devops-pipeline still reference all skills correctly? Does registry.md match?

Record each gap:

```markdown
| Asset | Gap Type | Details |
|-------|----------|---------|
| devops-safety-check | New pattern | New API key format not in detection patterns |
| devops-pipeline | Stale ref | References skill that was renamed |
| lint-skills.py | Missing check | New team not in KNOWN_TEAMS |
```

### Step 4: CREATE vs UPDATE Decision

<!-- 作成 vs 更新の判定ツリー -->

Apply this decision tree:

```
For each group of uncovered files:
    IF files relate to an existing asset's domain:
        → Decision: UPDATE existing asset (expand coverage)
    ELSE IF 3+ related files share common rules/patterns:
        → Decision: CREATE new verify skill
    ELSE:
        → Mark as "exempt" (no skill needed)
```

Present results to the user and use `AskUserQuestion` to confirm.

### Step 5: Update Existing Assets

<!-- 既存アセット更新 — 追加・修正のみ、既存検査は削除しない -->

For each asset approved for update, read the current content and apply targeted edits:

**Rules:**
- **Add/modify only** — never remove existing checks that still work
- Add new file paths to **Related Files** tables
- Add new detection commands for patterns found in changed files
- Remove references to files confirmed deleted from the codebase
- Update specific changed values (identifiers, config keys, type names)
- Update **Registered Assets** tables in this file if assets were added/removed/moved

### Step 6: Create New Verify Skills

<!-- 新verifyスキル作成 — ユーザー確認後にテンプレートから生成 -->

**Important:** Always confirm the skill name with the user before creating.

**Naming rules:**
- Name must start with `verify-` (e.g., `verify-auth`, `verify-api`)
- kebab-case only

**Required sections:** Purpose, When to Run, Related Files, Workflow (with PASS/FAIL criteria), Output Format, Exceptions

After creating:
1. Update **Registered Assets** in this file
2. Update `CLAUDE.md` Skills table
3. No manual registration needed in `verify-implementation/SKILL.md` — it discovers dynamically

### Step 7: Validation

<!-- 検証 — マークダウン形式・ファイル参照・コマンド構文チェック -->

After all edits:

1. Re-read all modified files
2. Verify markdown format (unclosed code blocks, consistent table columns)
3. Check for broken file references:

```bash
ls <file-path> 2>/dev/null || echo "MISSING: <file-path>"
```

4. Dry-run one detection command from each updated asset to validate syntax
5. Verify **Registered Assets** tables match actual filesystem
6. Verify CLAUDE.md Skills table is up to date

### Step 8: Summary Report

<!-- 最終レポート — 変更・生成・未カバーの要約 -->

```markdown
## Session Skill Maintenance Report

### Changed files analyzed: N
### Assets affected: X (of Y total registered)
### Assets updated: U
### Verify skills created: C
### Uncovered changes: E (exempt)
```

---

## Quality Standards

<!-- スキル品質基準 -->

All created or updated assets must have:

- **Actual file paths** (verified with `ls`), not placeholders
- **Working detection commands** matching current files
- **PASS/FAIL criteria** for each check
- **At least 2-3 realistic exceptions**
- **Consistent format** with existing assets

---

## Related Files

| File | Purpose |
|------|---------|
| `.claude/skills/verify-implementation/SKILL.md` | Integrated verification runner |
| `CLAUDE.md` | Project guidelines and routing |
| `registry.md` | Asset registry |
| `plugins/devops/agents/devops-pipeline.md` | DevOps pipeline orchestration |
| `scripts/lint-skills.py` | Skill structure linter |
| `scripts/sync-registry.py` | Registry auto-sync |
| `scripts/dep-graph.py` | Dependency graph and cycle detection |
| `standards/CODING-STANDARDS.md` | 10 global coding rules |

## Exceptions

<!-- 例外 — 管理対象外のファイル種別 -->

The following are **NOT problems**:

1. **Lock files and generated files** — `package-lock.json`, `yarn.lock`, build outputs need no coverage
2. **One-off config changes** — version bumps, minor linter config changes
3. **Documentation files** — `README.md`, `CHANGELOG.md`, `LICENSE`
4. **Test fixture files** — files in `fixtures/`, `test-data/`
5. **Vendor/third-party code** — `vendor/`, `node_modules/`
6. **CI/CD config** — `.github/`, `Dockerfile`
7. **CLAUDE.md itself** — documentation updates, not verifiable code patterns
8. **This file itself** — changes to manage-skills/SKILL.md are meta-maintenance
