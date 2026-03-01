---
name: manage-skills
description: Analyzes session changes to detect verification skill drift. Dynamically discovers existing skills, creates new ones or updates existing ones, then manages CLAUDE.md.
disable-model-invocation: true
argument-hint: "[optional: specific skill name or area to focus on]"
---

<!-- セッション変更分析 — verify スキルのドリフト検出・修正を担当 -->

# Session-Based Skill Maintenance

## Purpose

Analyzes changes in the current session to detect and fix verification skill drift:

1. **Coverage gaps** — changed files not referenced by any verify skill
2. **Invalid references** — skills referencing deleted or moved files
3. **Missing checks** — new patterns/rules not covered by existing checks
4. **Stale values** — config values or detection commands that no longer match

## When to Run

- After implementing a feature that introduces new patterns or rules
- When modifying existing verify skills and checking for consistency
- Before a PR to confirm verify skills cover changed areas
- When a verification run missed expected issues
- Periodically to align skills with codebase changes

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
# Source files modified more recently than this skill, excluding internals
find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' \
       -not -path '*/.claude/skills/*' -newer .claude/skills/manage-skills/SKILL.md \
       2>/dev/null | head -50
```

If both methods fail, ask the user for a list of changed files.

Merge into a deduplicated list. If an optional argument specifies a skill name or area, filter to relevant files only.

**Display:** Group files by top-level directory (first 1-2 path segments):

```markdown
## Session Changes Detected

**N files changed in this session:**

| Directory | Files |
|-----------|-------|
| src/components | `Button.tsx`, `Modal.tsx` |
| src/server | `router.ts`, `handler.ts` |
| tests | `api.test.ts` |
| (root) | `package.json`, `.eslintrc.js` |
```

### Step 2: Dynamic Skill Discovery & File Mapping

<!-- 動的スキル探索 — ファイルシステムからverifyスキルを自動検出 -->

#### Sub-step 2a: Auto-discover verify skills

**Discover from the file system directly, not from a manual registry:**

```bash
# Glob for verify-*/ directories under .claude/skills/
ls -d .claude/skills/verify-*/ 2>/dev/null
```

For each discovered skill, read its `SKILL.md` and extract file path patterns from:

1. **Related Files** section — parse table for file paths and glob patterns
2. **Workflow** section — extract file paths from grep/glob/read commands

If 0 skills are found (new project with no verify skills yet), skip to Step 4 (CREATE vs UPDATE decision). All changed files are marked "UNCOVERED".

#### Sub-step 2b: Match changed files to skills

For each changed file from Step 1, match against discovered skill patterns. A file matches a skill if:

- It matches the skill's cover file pattern
- It is located within a directory the skill references
- It matches a regex/string pattern used in the skill's detection commands

#### Sub-step 2c: Display mapping

```markdown
### File → Skill Mapping

| Skill | Trigger Files (changed) | Action |
|-------|------------------------|--------|
| verify-api | `router.ts`, `handler.ts` | CHECK |
| verify-ui | `Button.tsx` | CHECK |
| (no skill) | `package.json`, `.eslintrc.js` | UNCOVERED |
```

### Step 3: Coverage Gap Analysis for Affected Skills

<!-- カバレッジギャップ分析 — 影響スキルの検査漏れを検出 -->

For each AFFECTED skill (one with matched changed files), read the full SKILL.md and check:

1. **Missing file references** — changed files related to this skill's domain not listed in Related Files?
2. **Stale detection commands** — do the skill's grep/glob patterns still match current file structure? Run sample commands to test.
3. **Uncovered new patterns** — read changed files and identify new rules, configs, or patterns the skill doesn't check. Look for:
   - New type definitions, enum variants, or exported symbols
   - New registrations or configurations
   - New file naming or directory conventions
4. **Dangling references** — files listed in Related Files that no longer exist in the codebase?
5. **Changed values** — specific values the skill checks (identifiers, config keys, type names) that were modified?

Record each gap:

```markdown
| Skill | Gap Type | Details |
|-------|----------|---------|
| verify-api | Missing file | `src/server/newHandler.ts` not in Related Files |
| verify-ui | New pattern | New component uses unchecked convention |
| verify-test | Stale value | Test runner pattern in config changed |
```

### Step 4: CREATE vs UPDATE Decision

<!-- 作成 vs 更新の判定ツリー -->

Apply this decision tree:

```
For each group of uncovered files:
    IF files relate to an existing skill's domain:
        → Decision: UPDATE existing skill (expand coverage)
    ELSE IF 3+ related files share common rules/patterns:
        → Decision: CREATE new verify skill
    ELSE:
        → Mark as "exempt" (no skill needed)
```

Present results to the user:

```markdown
### Proposed Actions

**Decision: UPDATE existing skills** (N)
- `verify-api` — add 2 missing file references, update detection patterns
- `verify-test` — update detection commands for new config patterns

**Decision: CREATE new skills** (M)
- New skill needed — covers <pattern description> (X uncovered files)

**No action needed:**
- `package.json` — config file, exempt
- `README.md` — documentation, exempt
```

Use `AskUserQuestion` to confirm:
- Which existing skills to update
- Whether to create proposed new skills
- Option to skip entirely

### Step 5: Update Existing Skills

<!-- 既存スキル更新 — 追加・修正のみ、既存検査は削除しない -->

For each skill approved for update, read the current SKILL.md and apply targeted edits:

**Rules:**
- **Add/modify only** — never remove existing checks that still work
- Add new file paths to the **Related Files** table
- Add new detection commands for patterns found in changed files
- Add new workflow steps or sub-steps for uncovered rules
- Remove references to files confirmed deleted from the codebase
- Update specific changed values (identifiers, config keys, type names)

**Example — adding to Related Files:**

```markdown
## Related Files

| File | Purpose |
|------|---------|
| ... existing entries ... |
| `src/server/newHandler.ts` | New request handler with validation |
```

**Example — adding a detection command:**

````markdown
### Step N: Verify New Pattern

**File:** `path/to/file.ts`

**Check:** Description of what to verify.

```bash
grep -n "pattern" path/to/file.ts
```

**Violation:** What it looks like when wrong.
````

### Step 6: Create New Skills

<!-- 新スキル作成 — ユーザー確認後にテンプレートから生成 -->

**Important:** Always confirm the skill name with the user before creating.

For each new skill to create:

1. **Explore** — read related changed files to deeply understand the patterns

2. **Confirm name with user** — use `AskUserQuestion`:

   Present the patterns/domain the skill will cover and ask the user to provide or confirm a name.

   **Naming rules:**
   - Name must start with `verify-` (e.g., `verify-auth`, `verify-api`, `verify-caching`)
   - If user provides a name without `verify-` prefix, prepend it automatically and inform them
   - Use kebab-case (e.g., `verify-error-handling`, not `verify_error_handling`)

3. **Create** — generate `.claude/skills/verify-<name>/SKILL.md` using this template:

```yaml
---
name: verify-<name>
description: <one-line description>. Use after <trigger condition>.
---
```

Required sections:
- **Purpose** — 2-5 numbered verification categories
- **When to Run** — 3-5 trigger conditions
- **Related Files** — table of actual file paths in the codebase (verified with `ls`, no placeholders)
- **Workflow** — check steps, each specifying:
  - Tool to use (Grep, Glob, Read, Bash)
  - Exact file paths or patterns
  - PASS/FAIL criteria
  - Fix instructions on failure
- **Output Format** — markdown table for results
- **Exceptions** — at least 2-3 realistic "not a violation" cases

4. **Update CLAUDE.md** — add a row to the Skills table in `CLAUDE.md` after creating the new skill.

   **Note:** No manual registration needed in `manage-skills/SKILL.md` or `verify-implementation/SKILL.md`. Both meta-skills dynamically discover `.claude/skills/verify-*/` at runtime.

### Step 7: Validation

<!-- 検証 — マークダウン形式・ファイル参照・コマンド構文チェック -->

After all edits:

1. Re-read all modified SKILL.md files
2. Verify markdown format (unclosed code blocks, consistent table columns)
3. Check for broken file references — for each path in Related Files:

```bash
ls <file-path> 2>/dev/null || echo "MISSING: <file-path>"
```

4. Dry-run one detection command from each updated skill to validate syntax
5. Verify CLAUDE.md Skills table matches actual `.claude/skills/` directory contents

### Step 8: Summary Report

<!-- 最終レポート — 変更・生成・未カバーの要約 -->

Display the final report:

```markdown
## Session Skill Maintenance Report

### Changed files analyzed: N

### Skills updated: X
- `verify-<name>`: N new checks added, Related Files updated
- `verify-<name>`: detection commands updated for new patterns

### Skills created: Y
- `verify-<name>`: covers <pattern>

### Updated related files:
- `CLAUDE.md`: Skills table updated

### Unaffected skills: Z
- (no related changes)

### Uncovered changes (no skill applicable):
- `path/to/file` — exempt (reason)
```

---

## Quality Standards for Created/Updated Skills

<!-- スキル品質基準 — 全スキルが満たすべき要件 -->

All created or updated skills must have:

- **Actual file paths from the codebase** (verified with `ls`), not placeholders
- **Working detection commands** — real grep/glob patterns matching current files
- **PASS/FAIL criteria** — clear conditions for pass and fail on each check
- **At least 2-3 realistic exceptions** — descriptions of what is NOT a violation
- **Consistent format** — same as existing skills (frontmatter, section headers, table structure)

---

## Related Files

| File | Purpose |
|------|---------|
| `.claude/skills/verify-implementation/SKILL.md` | Integrated verification runner (discovers verify skills dynamically) |
| `.claude/skills/manage-skills/SKILL.md` | This file itself |
| `CLAUDE.md` | Project guidelines (this skill manages the Skills section) |
| `registry.md` | Asset registry for the Skill & Agent Factory |

## Exceptions

<!-- 例外 — スキル対象外のファイル種別 -->

The following are **NOT problems**:

1. **Lock files and generated files** — `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, auto-generated migration files, build outputs need no skill coverage
2. **One-off config changes** — version bumps in `package.json`/`Cargo.toml`, minor linter/formatter config changes need no new skill
3. **Documentation files** — `README.md`, `CHANGELOG.md`, `LICENSE` are not code patterns requiring verification
4. **Test fixture files** — files in fixture directories (`fixtures/`, `__fixtures__/`, `test-data/`) are not production code
5. **Unaffected skills** — skills marked UNAFFECTED need no review; most skills in most sessions fall here
6. **CLAUDE.md itself** — changes to CLAUDE.md are documentation updates, not verifiable code patterns
7. **Vendor/third-party code** — files in `vendor/`, `node_modules/`, or copied library directories follow external rules
8. **CI/CD config** — `.github/`, `.gitlab-ci.yml`, `Dockerfile` are infrastructure, not application patterns needing verify skills
