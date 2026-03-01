---
name: pm-self-check
version: v1.0
description: Post-implementation evidence-based validation. Prevents hallucination by requiring proof for every claim. Runs 4 mandatory questions and 7 hallucination red-flag detections.
tags: [pm, self-check, validation, post-check, evidence, hallucination]
allowed-tools: Read, Grep, Glob, Bash
---

# Post-Implementation Self-Check Protocol

<!-- 実装後のセルフチェック — 証拠ベースの検証でハルシネーションを防止する -->

実装が終わったら「本当に完了したのか？」を証拠で確認する。
推測禁止 — 必ずテスト結果・ファイル変更・ログで証明する。

---

## The Four Questions (MANDATORY)

<!-- 4つの必須質問 — 全て証拠付きで回答する必要がある -->

### Q1: Are All Tests Passing?

```bash
# Run actual tests — do NOT claim "tests pass" without output
[project test command] 2>&1
```

- Execute tests and capture ACTUAL output
- Show real pass/fail results with numbers
- If any test fails → implementation is NOT complete
- **RED FLAG**: Claiming "tests pass" without showing output

### Q2: Are All Requirements Met?

```
Compare: original request vs actual implementation
```

For each requirement from the user's request:
- ✅ **Met**: Evidence of implementation (file path, line number)
- ❌ **Missing**: Not yet implemented
- ⚠️ **Partial**: Partially implemented, needs more work

If ANY requirement is ❌ → implementation is NOT complete

### Q3: No Assumptions Without Verification?

<!-- 検証なしの仮定がないか確認 -->

Review all decisions made during implementation:
- Was each decision based on official documentation?
- Were any "I think this works" assumptions made?
- Were API behaviors verified (not guessed)?
- Were edge cases tested (not assumed to work)?

If unverified assumptions exist → flag them for verification

### Q4: Is There Evidence?

Three types of evidence required:

| Evidence Type | What to Show | How to Get |
|---------------|-------------|------------|
| **Test Results** | Actual test output with pass/fail | `bash: run tests` |
| **Code Changes** | List of files modified/created | `bash: git diff --name-only` |
| **Validation** | Lint, typecheck, build results | `bash: run linter/build` |

If ANY evidence type is missing → cannot claim "complete"

---

## 7 Hallucination Red Flags

<!-- 7つのハルシネーション危険信号 — 検出時は即座に停止 -->

| # | Red Flag | Detection |
|---|----------|-----------|
| 1 | "Tests pass" without showing output | Claims pass but no test output shown |
| 2 | "Everything works" without evidence | No file changes, no test results |
| 3 | "Implementation complete" with failing tests | Status says done but tests fail |
| 4 | Skipping error messages | Errors in output but not addressed |
| 5 | Ignoring warnings | Warnings present but dismissed |
| 6 | Hiding failures | Selective reporting of results |
| 7 | "Probably works" language | Uses maybe/probably/should work |

When ANY red flag is detected:
1. **STOP** — do not proceed
2. **FLAG** — report the red flag to the user
3. **FIX** — address the issue with evidence

---

## Execution Steps

### Step 1: Collect Implementation Summary

```
- What was the original request?
- What files were created/modified?
- What approach was taken?
```

### Step 2: Run The Four Questions

Execute Q1–Q4 in order. Collect evidence for each.

### Step 3: Scan for Hallucination Red Flags

Check all 7 red flags against the implementation claims.

### Step 4: Generate Self-Check Report

```markdown
## Self-Check Report

### Q1: Tests Passing?
Status: ✅ PASS / ❌ FAIL
Evidence:
```
[actual test output here]
```

### Q2: Requirements Met?
- ✅ Requirement A: [evidence]
- ❌ Requirement B: [what's missing]

### Q3: Unverified Assumptions?
- None found / [list assumptions that need verification]

### Q4: Evidence Provided?
- Test Results: ✅/❌
- Code Changes: ✅/❌
- Validation: ✅/❌

### Hallucination Scan
- Red Flags Detected: 0 / [list detected flags]

### Verdict: ✅ COMPLETE / ❌ INCOMPLETE
[If incomplete: list what needs to be done]
```

---

## Integration with DevOps Pipeline

<!-- DevOpsパイプラインとの統合 — 全ステップ完了後、コミット前に実行 -->

This skill runs as **STEP_SELF_CHECK** in the devops-pipeline:

```
... implementation steps ...
    ↓
STEP_SELF_CHECK ← this skill
    ↓
STEP_GIT_COMMIT (only if self-check passes)
```

If self-check FAILS, pipeline loops back to fix issues before commit.

---

## Token Budget

- Validation: 200–2,500 tokens (complexity-dependent)
- Detection rate: 94% (hallucination prevention)

---

## Output Format

```yaml
verdict: COMPLETE | INCOMPLETE
questions:
  tests_passing: { status: PASS|FAIL, evidence: "..." }
  requirements_met: { status: PASS|FAIL, unmet: [...] }
  assumptions_verified: { status: PASS|FAIL, unverified: [...] }
  evidence_provided: { status: PASS|FAIL, missing: [...] }
red_flags: []  # list of detected hallucination flags
action: COMMIT | FIX_AND_RECHECK
```
