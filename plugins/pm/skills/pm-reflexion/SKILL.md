---
name: pm-reflexion
version: v1.0
description: Error learning and prevention through reflexion pattern. Records mistakes with root cause analysis, searches for known solutions before investigating, and maintains a knowledge base of lessons learned. Implements PDCA documentation cycle.
tags: [pm, reflexion, error-learning, mistake, prevention, pdca]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Reflexion — Error Learning & Prevention

<!-- リフレクション — エラー学習と再発防止のパターン -->

エラーが発生したら「過去に同じ問題があったか？」をまず確認し、
なければ根本原因を分析して記録する。同じ失敗を二度と繰り返さない。

---

## Core Principle

```
Error detected
    ↓
Check known solutions (cache hit → 0 tokens, instant fix)
    ↓
No match → Investigate root cause (1-2K tokens)
    ↓
Record solution for future reuse
    ↓
Error recurrence rate: < 10%
Solution reuse rate: > 90%
```

---

## Step 1: Search Known Solutions

<!-- 既知の解決策検索 — まずローカル知識ベースを確認 -->

Before investigating, check if this error has been seen before:

```bash
# Search local solutions log
grep -i "[error keyword]" docs/memory/solutions_learned.jsonl 2>/dev/null

# Search mistake records
grep -ri "[error keyword]" docs/mistakes/ 2>/dev/null

# Search pattern library
grep -ri "[error keyword]" docs/patterns/ 2>/dev/null
```

**If match found** → Apply known solution immediately (0 tokens saved)
**If no match** → Proceed to Step 2

---

## Step 2: Root Cause Analysis

<!-- 根本原因分析 — 5つの質問で原因を特定 -->

Ask these 5 questions systematically:

| # | Question | Purpose |
|---|----------|---------|
| 1 | **What happened?** | Exact error message, stack trace, behavior |
| 2 | **What was expected?** | Correct behavior that should have occurred |
| 3 | **Why did it happen?** | Technical root cause (not symptoms) |
| 4 | **Why was it missed?** | What check/process failed to catch it |
| 5 | **How to prevent?** | Concrete prevention steps |

---

## Step 3: Record Solution

### 3a: Append to Solutions Log

```
File: docs/memory/solutions_learned.jsonl
Format: One JSON object per line (append-only)
```

```json
{
  "timestamp": "2026-03-01T12:00:00",
  "error_type": "TypeError",
  "error_message": "Cannot read property 'id' of undefined",
  "context": "vertx-api-caller processing response",
  "root_cause": "API response missing expected field when status is 404",
  "solution": "Add null check before accessing response.data.id",
  "prevention": "Always validate API response shape before accessing nested fields",
  "tags": ["vertx", "api", "null-check"]
}
```

### 3b: Create Mistake Document (for significant errors)

```
File: docs/mistakes/[feature]-[YYYY-MM-DD].md
```

```markdown
# Mistake Record: [feature name]

**Date**: YYYY-MM-DD
**Error Type**: [error type]
**Severity**: HIGH | MEDIUM | LOW

---

## What Happened (現象)
[Exact description of the error]

## Root Cause (根本原因)
[Why it happened — technical root cause]

## Why Missed (なぜ見逃したか)
[What check or process should have caught this]

## Fix Applied (修正内容)
[Concrete solution that was applied]

## Prevention Checklist (防止策)
- [ ] [Step 1 to prevent recurrence]
- [ ] [Step 2 to prevent recurrence]

## Lesson Learned (教訓)
[Key takeaway for future work]
```

---

## Step 4: Update Knowledge Base

<!-- 知識ベースの更新 — 成功パターンと失敗パターンを蓄積 -->

Based on the error and its resolution:

### If pattern discovered → Create Pattern Document

```
File: docs/patterns/[pattern-name].md
```

Move from temporary trial-and-error to formal reusable knowledge.

### If global rule needed → Update CLAUDE.md

Add new rules or strengthen existing ones in project CLAUDE.md when a mistake reveals a gap in coding standards.

---

## PDCA Documentation Cycle

<!-- PDCA文書サイクル — 仮説→実験→評価→改善 -->

Reflexion follows the PDCA (Plan-Do-Check-Act) cycle:

| Phase | Japanese | Action | Output |
|-------|----------|--------|--------|
| **Plan** | 仮説 | Define what to implement and why | `docs/temp/hypothesis-YYYY-MM-DD.md` |
| **Do** | 実験 | Execute, record trial-and-error | `docs/temp/experiment-YYYY-MM-DD.md` |
| **Check** | 評価 | Evaluate: what worked, what failed | `docs/temp/lessons-YYYY-MM-DD.md` |
| **Act** | 改善 | Success → `docs/patterns/`, Failure → `docs/mistakes/` | Formal documentation |

### Documentation Flow

```
docs/temp/ (temporary, raw notes)
    ↓
Success → docs/patterns/[name].md (formal, reusable)
Failure → docs/mistakes/[name]-[date].md (prevention-focused)
    ↓
Accumulate → Extract best practices → CLAUDE.md
```

### Cleanup Rules

- `docs/temp/` files older than 7 days → move or delete
- `docs/mistakes/` — keep permanently (prevention reference)
- `docs/patterns/` — keep and update with "Last Verified" dates

---

## Directory Structure

```
docs/
├── temp/                    # Temporary trial-and-error notes
│   ├── hypothesis-*.md      # Plan phase
│   ├── experiment-*.md      # Do phase
│   └── lessons-*.md         # Check phase
├── patterns/                # Verified successful patterns
│   └── [pattern-name].md
├── mistakes/                # Error records with prevention
│   └── [feature]-[date].md
└── memory/
    └── solutions_learned.jsonl  # Append-only solutions log
```

---

## Integration with DevOps Pipeline

<!-- DevOpsパイプラインとの統合 — エラー発生時に自動起動 -->

This skill is triggered automatically when:
- Any pipeline step FAILS
- Tests produce errors
- Build/lint produces errors
- User reports a mistake

```
Pipeline step fails
    ↓
pm-reflexion auto-invoked
    ↓
Search known solutions → fix or investigate
    ↓
Record solution → resume pipeline
```

---

## Statistics Tracking

```yaml
total_errors_recorded: N
errors_with_solutions: N
solution_reuse_rate: XX%  # target: > 90%
error_recurrence_rate: XX%  # target: < 10%
```

---

## Output Format

```yaml
action: KNOWN_SOLUTION | NEW_INVESTIGATION | RECORDED
known_solution:  # if cache hit
  source: "docs/mistakes/xxx.md"
  solution: "..."
  confidence: HIGH
investigation:  # if new error
  root_cause: "..."
  solution: "..."
  prevention: "..."
  files_created:
    - docs/mistakes/xxx.md
    - docs/memory/solutions_learned.jsonl (appended)
```
