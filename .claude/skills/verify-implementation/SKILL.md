---
name: verify-implementation
description: Sequentially runs ALL verification checks across the project — verify skills, devops pipeline skills, figma skills, vertx skills, scripts, and coding standards. Produces an integrated report. Use after implementation, before PR, during review.
disable-model-invocation: true
argument-hint: "[optional: skill name, category (devops/figma/vertx), or 'all']"
---

<!-- 統合検証実行 — 全プロジェクトアセットを順次検証し統合レポートを生成 -->

# Implementation Verification

## Purpose

Runs comprehensive verification across ALL project assets:

- **verify-* skills** — custom verification rules created by `/manage-skills`
- **DevOps pipeline skills** — safety, code review, architecture, Japanese comments, tests, version
- **Figma skills** — design analysis, code sync, responsive validation
- **Vert.x skills** — repo analysis, EventBus registration, API caller
- **Scripts** — lint-skills.py, sync-registry.py, dep-graph.py
- **Standards** — CODING-STANDARDS.md compliance

## When to Run

- After implementing a new feature
- Before creating a Pull Request
- During code review
- When auditing codebase rule compliance

## Verification Categories

<!-- 検証カテゴリ — 実行順序と担当アセット -->

| # | Category | Assets | What it checks |
|---|----------|--------|---------------|
| 1 | Skill Structure | `lint-skills.py` | Frontmatter, required fields, circular deps, stale refs |
| 2 | Dependency Graph | `dep-graph.py` | Circular references, deep chains (>3) |
| 3 | Registry Sync | `sync-registry.py` | registry.md and README.md up to date |
| 4 | Security | `devops-safety-check` | Secrets, injection patterns, vulnerabilities |
| 5 | Code Quality | `devops-code-review` | Logic, performance, N+1, dead code |
| 6 | Architecture | `devops-arch-review` | Structure, naming, duplication, SRP |
| 7 | Japanese Comments | `devops-japanese-comments` | All comments/logs in Japanese |
| 8 | Coding Standards | `CODING-STANDARDS.md` | 10 global rules (headers, 30-line funcs, etc.) |
| 9 | Version Compat | `devops-version-check` | Language/library version, deprecated APIs |
| 10 | Tests | `devops-test-gen` | Test coverage for changed files |
| 11 | Frontend | `devops-frontend-review` + figma skills | UI pixel-perfect, responsive, design tokens |
| 12 | Vert.x | vertx skills | EventBus, API templates, repo structure |
| 13 | Git | `devops-git-commit` | Branch strategy, commit format |
| 14 | Custom | `.claude/skills/verify-*` | Any verify skills created by `/manage-skills` |

## Workflow

### Step 1: Asset Discovery & Scope

<!-- 動的アセット探索 — カテゴリ別に全アセットを検出 -->

**Discover all verifiable assets from the file system:**

```bash
# Custom verify skills
ls -d .claude/skills/verify-*/SKILL.md 2>/dev/null

# DevOps plugin skills
ls -d plugins/devops/skills/*/SKILL.md 2>/dev/null

# Figma plugin skills
ls -d plugins/figma/skills/*/SKILL.md 2>/dev/null

# Vert.x plugin skills
ls -d plugins/vertx/skills/*/SKILL.md 2>/dev/null

# Scripts
ls scripts/*.py 2>/dev/null

# Standards
ls standards/*.md 2>/dev/null
```

**Scope filtering:** If an optional argument is provided:
- Skill name (e.g., `devops-safety-check`) → run only that skill
- Category (e.g., `devops`, `figma`, `vertx`) → run only that category
- `all` or no argument → run everything

**If 0 assets found:** Display guidance and terminate.

**Display discovered scope:**

```markdown
## Implementation Verification

Running verification across N assets in M categories:

| Category | Assets | Count |
|----------|--------|-------|
| Skill Structure | lint-skills.py | 1 |
| Security | devops-safety-check | 1 |
| Code Quality | devops-code-review | 1 |
| Custom Verify | verify-api, verify-auth | 2 |
| ... | ... | ... |

Starting verification...
```

### Step 2: Sequential Execution by Category

<!-- 順次実行 — カテゴリ順に全検査を実行 -->

Execute each category in the order defined in the **Verification Categories** table.

#### 2a. Script-based checks (Categories 1-3)

Run scripts directly and capture output:

```bash
# Category 1: Skill Structure
python3 scripts/lint-skills.py --strict 2>&1

# Category 2: Dependency Graph
python3 scripts/dep-graph.py --check 2>&1

# Category 3: Registry Sync
python3 scripts/sync-registry.py --dry-run 2>&1
```

Parse script output for errors/warnings. Record as PASS (0 errors), WARN (warnings only), or FAIL (errors found).

**If a script fails to execute:** Record as `ERROR` and continue to the next category.

#### 2b. Skill-based checks (Categories 4-13)

For each skill in categories 4-13:

1. Read the skill's `SKILL.md` and parse: **Workflow**, **Exceptions**, **Related Files**
2. Execute each check defined in the Workflow section
3. Compare results against PASS/FAIL criteria
4. Exempt patterns matching Exceptions
5. Record issues with file path, line number, problem, fix suggestion

**If SKILL.md parsing fails:** Mark as `SKIP` with `PARSE_ERROR`. Continue to next skill.
**If individual check fails:** Mark as `ERROR`. Continue to next check.

#### 2c. Custom verify skills (Category 14)

For each `.claude/skills/verify-*/SKILL.md` discovered:

1. Read and parse the skill's full Workflow
2. Execute all checks as defined
3. Apply the skill's own Exceptions
4. Record results

#### 2d. Per-category progress

Display after each category completes:

```markdown
### [Category N] <name> — complete

- Checks: N
- Passed: X
- Issues: Y
- Exempted: Z
- Errors: E

[Moving to next category...]
```

### Step 3: Integrated Report

<!-- 統合レポート — 全カテゴリ結果を1つのレポートに集約 -->

```markdown
## Implementation Verification Report

### Summary

| # | Category | Asset | Status | Issues | Errors |
|---|----------|-------|--------|--------|--------|
| 1 | Skill Structure | lint-skills.py | PASS | 0 | 0 |
| 2 | Dependency Graph | dep-graph.py | PASS | 0 | 0 |
| 3 | Registry Sync | sync-registry.py | WARN | 1 | 0 |
| 4 | Security | devops-safety-check | FAIL | 3 | 0 |
| ... | ... | ... | ... | ... | ... |

**Total: X issues / E errors across N categories**
```

**All checks pass:**

```markdown
All verifications passed across N categories!
Ready for code review.
```

**Issues found:**

```markdown
### Issues Found

| # | Category | File | Problem | Fix |
|---|----------|------|---------|-----|
| 1 | Security | `src/api.ts:42` | Hardcoded API key | Move to .env |
| 2 | Code Quality | `src/handler.ts:15` | Missing await | Add await |
| 3 | Japanese Comments | `src/utils.ts:1` | English header | Convert to Japanese |
```

### Step 4: User Action Confirmation

<!-- ユーザー確認 — 修正オプション提示 -->

If issues found, use `AskUserQuestion`:

1. **Fix all** — automatically apply all recommended fixes
2. **Fix by category** — choose which categories to fix
3. **Fix individually** — review each fix one by one
4. **Skip** — exit without changes

### Step 5: Apply Fixes

<!-- 修正適用 -->

Apply fixes based on user selection, displaying progress per category.

### Step 6: Re-verify After Fixes

<!-- 修正後再検証 — Before/After比較 -->

Re-run only affected categories and compare Before/After:

```markdown
## Post-fix Re-verification

| Category | Before | After |
|----------|--------|-------|
| Security | 3 issues | PASS |
| Japanese Comments | 1 issue | PASS |

All verifications passed!
```

---

## Exceptions

<!-- 例外 — 問題ではないケース -->

The following are **NOT problems**:

1. **Projects with no verify skills** — Categories 1-13 still run; only Category 14 is empty
2. **Skill-specific exceptions** — each skill's Exceptions section is respected
3. **verify-implementation itself** — not included in execution targets
4. **manage-skills** — not included in execution targets
5. **Script execution errors** — one script failing does not abort others
6. **SKILL.md parse errors** — one skill failing to parse does not abort others
7. **Skipped categories** — when user specifies a scope filter, unlisted categories are expected to be absent

## Related Files

| File | Purpose |
|------|---------|
| `.claude/skills/manage-skills/SKILL.md` | Skill maintenance (creates/updates verify skills, tracks all assets) |
| `CLAUDE.md` | Project guidelines and routing |
| `registry.md` | Asset registry |
| `plugins/devops/agents/devops-pipeline.md` | DevOps pipeline orchestration |
| `scripts/lint-skills.py` | Skill structure linter |
| `scripts/sync-registry.py` | Registry auto-sync |
| `scripts/dep-graph.py` | Dependency graph and cycle detection |
| `standards/CODING-STANDARDS.md` | 10 global coding rules |
