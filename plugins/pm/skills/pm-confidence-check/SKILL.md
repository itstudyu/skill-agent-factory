---
name: pm-confidence-check
version: v1.0
description: Pre-implementation confidence assessment. Evaluates readiness across 5 dimensions before starting work. Prevents wrong-direction execution by gating implementation behind a confidence threshold.
tags: [pm, confidence, pre-check, assessment, quality-gate]
allowed-tools: Read, Grep, Glob
---

# Pre-Implementation Confidence Check

<!-- 実装前の信頼度チェック — 作業開始前に5つの観点で準備状況を評価する -->

実装を始める前に「本当にこれで進めて大丈夫か？」を確認するゲート。

---

## Confidence Levels & Actions

| Level | Score | Action |
|-------|-------|--------|
| **HIGH** | ≥ 90% | Proceed immediately with implementation |
| **MEDIUM** | 70–89% | Present alternatives to user, ask which approach |
| **LOW** | < 70% | STOP. Ask clarifying questions. Do NOT implement. |

---

## 5-Dimension Assessment

<!-- 5次元評価 — 各観点25〜15%の重みで信頼度スコアを算出 -->

### Dimension 1: No Duplicate Implementations (25%)

```
Grep: [function/class/module name] across codebase
Glob: similar file names in project
```

- Search for existing code that already solves this problem
- Check project dependencies for built-in solutions
- Verify no helper functions already provide this functionality
- **PASS**: No duplicates found, confirmed via codebase search
- **FAIL**: Similar implementation exists — reuse or extend it instead

### Dimension 2: Architecture Compliance (25%)

```
Read: CLAUDE.md → check tech stack and coding standards
Read: project-context/structure.md → existing architecture patterns
```

- Verify solution uses the project's existing tech stack
- Check alignment with established patterns (naming, structure, conventions)
- Confirm no reinvention of provided functionality
- **Examples**:
  - Vert.x project → Use EventBus patterns, not custom messaging
  - React + Figma project → Use design tokens, not hardcoded styles
  - Existing API pattern → Follow same controller/service structure

### Dimension 3: Official Documentation Verified (20%)

- Has the relevant official documentation been read?
- Are API signatures, configuration options, and limitations understood?
- Is the approach based on documented behavior (not guesses)?
- **PASS**: Official docs consulted, approach matches documented patterns
- **FAIL**: Proceeding based on assumption without doc verification

### Dimension 4: Working Reference Found (15%)

- Is there a working OSS implementation or reference to follow?
- Has a similar pattern been verified in another project?
- Are community best practices available for this approach?
- **PASS**: Reference implementation found and analyzed
- **FAIL**: No reference — higher risk of wrong approach

### Dimension 5: Root Cause Identified (15%)

<!-- 根本原因の特定 — バグ修正・問題解決時のみ適用 -->

*Applies to bugfix/problem-solving tasks. For new features, auto-pass.*

- Is the root cause pinpointed (not guessing)?
- Does the proposed solution address the root cause (not symptoms)?
- Has the fix been verified against official docs or OSS patterns?
- **PASS**: Root cause clearly identified with evidence
- **FAIL**: Still guessing — continue investigation

---

## Execution Steps

### Step 1: Identify Task Type

```
NEW_FEATURE  → Dimensions 1-4 apply, Dimension 5 auto-pass
BUGFIX       → All 5 dimensions apply
REFACTOR     → Dimensions 1-3 apply, Dimensions 4-5 relaxed
PATCH        → Dimensions 1-2 apply, others auto-pass
```

### Step 2: Run Each Dimension Check

For each applicable dimension:
1. Execute the check (read files, grep codebase, verify docs)
2. Record result: PASS / FAIL with evidence
3. Calculate weighted score

### Step 3: Calculate Total Confidence Score

```
Score = (Dim1 × 0.25) + (Dim2 × 0.25) + (Dim3 × 0.20) + (Dim4 × 0.15) + (Dim5 × 0.15)
```

Each dimension: 1.0 = PASS, 0.0 = FAIL

### Step 4: Report & Gate Decision

```markdown
## Confidence Report

| Dimension | Weight | Result | Evidence |
|-----------|--------|--------|----------|
| No Duplicates | 25% | ✅/❌ | [what was found] |
| Architecture | 25% | ✅/❌ | [what was checked] |
| Official Docs | 20% | ✅/❌ | [what was read] |
| Reference Found | 15% | ✅/❌ | [what was found] |
| Root Cause | 15% | ✅/❌ | [evidence] |

**Total: XX%** → [HIGH/MEDIUM/LOW] → [Proceed/Present Options/Stop]
```

---

## Integration with DevOps Pipeline

<!-- DevOpsパイプラインとの統合 — STEP_0の後、STEP_MODEの前に実行 -->

This skill runs as **STEP_CONFIDENCE** in the devops-pipeline:

```
STEP_0 (project-context check)
    ↓
STEP_CONFIDENCE ← this skill
    ↓
STEP_MODE (mode detection)
    ↓
... rest of pipeline
```

If confidence is LOW (< 70%), pipeline halts and asks the user for clarification before proceeding.

---

## Token Budget

- Assessment: 100–200 tokens
- ROI: 25–250× token savings when stopping wrong-direction work early

---

## Output Format

```yaml
confidence_score: 0.XX
level: HIGH | MEDIUM | LOW
action: PROCEED | PRESENT_OPTIONS | STOP
dimensions:
  no_duplicates: { score: X, evidence: "..." }
  architecture: { score: X, evidence: "..." }
  official_docs: { score: X, evidence: "..." }
  reference_found: { score: X, evidence: "..." }
  root_cause: { score: X, evidence: "..." }
recommendations:
  - "..." # if MEDIUM or LOW
```
