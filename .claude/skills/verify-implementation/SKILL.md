---
name: verify-implementation
description: Sequentially runs all verify skills in the project to produce an integrated verification report. Use after feature implementation, before PR, during code review.
disable-model-invocation: true
argument-hint: "[optional: specific verify skill name]"
---

<!-- 統合検証実行 — 全verifyスキルを順次実行し統合レポートを生成 -->

# Implementation Verification

## Purpose

Sequentially executes all `verify-*` skills registered in the project to perform integrated verification:

- Run checks defined in each skill's Workflow
- Reference each skill's Exceptions to prevent false positives
- Suggest fixes for discovered issues
- Apply fixes after user approval and re-verify

## When to Run

- After implementing a new feature
- Before creating a Pull Request
- During code review
- When auditing codebase rule compliance

## Workflow

### Step 1: Dynamic Skill Discovery

<!-- 動的スキル探索 — 手動リストではなくファイルシステムから直接検出 -->

**Discover from the file system directly, not from a manual list:**

```bash
ls -d .claude/skills/verify-*/ 2>/dev/null
```

Verify that each discovered directory contains a `SKILL.md`. Skip directories without one.

If an optional argument is provided, filter to skills matching that name only.

**If 0 skills found:**

```markdown
## Implementation Verification

No verification skills found. Run `/manage-skills` to create verification skills for your project.
```

Terminate the workflow in this case.

**If 1+ skills found:**

Read the `name` and `description` from each skill's frontmatter and display:

```markdown
## Implementation Verification

Running the following verification skills sequentially:

| # | Skill | Description |
|---|-------|-------------|
| 1 | verify-<name1> | <description1> |
| 2 | verify-<name2> | <description2> |

Starting verification...
```

### Step 2: Sequential Execution

<!-- 順次実行 — 各スキルのWorkflow検査を実行 -->

For each discovered verify skill, perform the following:

#### 2a. Read skill SKILL.md

Read the skill's `.claude/skills/verify-<name>/SKILL.md` and parse these sections:

- **Workflow** — check steps and detection commands to execute
- **Exceptions** — patterns considered not a violation
- **Related Files** — files to check

**If SKILL.md parsing fails:** Mark the skill as `SKIP` and record `PARSE_ERROR` in the report. Continue executing other skills.

#### 2b. Run checks

Execute each check defined in the Workflow section in order:

1. Use the tool specified in the check (Grep, Glob, Read, Bash) to detect patterns
2. Compare results against the skill's PASS/FAIL criteria
3. Exempt patterns matching the Exceptions section
4. For FAIL results, record the issue:
   - File path and line number
   - Problem description
   - Recommended fix (with code example)

**If an individual check fails to execute (command error etc.):** Record that check as `ERROR` and continue to the next check. A single check failure does not abort the entire skill run.

#### 2c. Record per-skill results

Display progress after each skill completes:

```markdown
### verify-<name> verification complete

- Checks: N
- Passed: X
- Issues: Y
- Exempted: Z
- Errors: E

[Moving to next skill...]
```

### Step 3: Integrated Report

<!-- 統合レポート — 全スキル結果を1つのレポートに集約 -->

After all skills complete, consolidate results into a single report:

```markdown
## Implementation Verification Report

### Summary

| Verify Skill | Status | Issues | Errors | Details |
|-------------|--------|--------|--------|---------|
| verify-<name1> | PASS / X issues | N | E | details... |
| verify-<name2> | PASS / X issues | N | E | details... |

**Total issues found: X / Errors: E**
```

**If all checks pass:**

```markdown
All verifications passed!

Implementation complies with all project rules:

- verify-<name1>: <pass summary>
- verify-<name2>: <pass summary>

Ready for code review.
```

**If issues found:**

List each issue with file path, problem description, and recommended fix:

```markdown
### Issues Found

| # | Skill | File | Problem | Fix |
|---|-------|------|---------|-----|
| 1 | verify-<name1> | `path/to/file.ts:42` | Problem description | Fix code example |
| 2 | verify-<name2> | `path/to/file.tsx:15` | Problem description | Fix code example |
```

### Step 4: User Action Confirmation

<!-- ユーザー確認 — 修正オプション提示 -->

If issues were found, use `AskUserQuestion` to confirm with the user:

```markdown
---

### Fix Options

**X issues found. How would you like to proceed?**

1. **Fix all** — automatically apply all recommended fixes
2. **Fix individually** — review and apply each fix one by one
3. **Skip** — exit without changes
```

### Step 5: Apply Fixes

<!-- 修正適用 — ユーザー選択に応じて修正実行 -->

Apply fixes based on user selection.

**"Fix all" selected:**

Apply all fixes in order, displaying progress:

```markdown
## Applying fixes...

- [1/X] verify-<name1>: `path/to/file.ts` fixed
- [2/X] verify-<name2>: `path/to/file.tsx` fixed

X fixes applied.
```

**"Fix individually" selected:**

For each issue, show the fix content and use `AskUserQuestion` to confirm approval.

### Step 6: Re-verify After Fixes

<!-- 修正後再検証 — Before/After比較 -->

If fixes were applied, re-run only the skills that had issues and compare Before/After:

```markdown
## Post-fix Re-verification

Re-running skills that had issues...

| Verify Skill | Before | After |
|-------------|--------|-------|
| verify-<name1> | X issues | PASS |
| verify-<name2> | Y issues | PASS |

All verifications passed!
```

**If issues remain:**

```markdown
### Remaining Issues

| # | Skill | File | Problem |
|---|-------|------|---------|
| 1 | verify-<name> | `path/to/file.ts:42` | Cannot auto-fix — manual review needed |

Resolve manually, then run `/verify-implementation` again.
```

---

## Exceptions

<!-- 例外 — 問題ではないケース -->

The following are **NOT problems**:

1. **Projects with no registered skills** — display a guidance message and exit, not an error
2. **Skill-specific exceptions** — patterns defined in each verify skill's Exceptions section are not reported as issues
3. **verify-implementation itself** — does not include itself in the execution target list
4. **manage-skills** — does not start with `verify-` so is not included in execution targets
5. **SKILL.md parse errors** — one skill failing to parse does not abort other skill executions

## Related Files

| File | Purpose |
|------|---------|
| `.claude/skills/manage-skills/SKILL.md` | Skill maintenance (creates/updates verify skills) |
| `CLAUDE.md` | Project guidelines |
| `registry.md` | Asset registry for the Skill & Agent Factory |
