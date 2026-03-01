---
name: pm-pipeline
description: PM (Project Management) pipeline orchestrator. Wraps around the devops-pipeline with pre-check and post-check quality gates. Runs confidence check before implementation and self-check + reflexion after. Trigger with "PM 파이프라인", "pm pipeline", "PM모드로 개발", "PMモード".
tools: Read, Write, Edit, Bash, Grep, Glob, Task
model: sonnet
version: v1.0
---

# PM Pipeline Agent

<!-- PM パイプラインエージェント — 開発パイプラインに信頼度チェックとセルフチェックを追加するオーケストレーター -->

DevOpsパイプラインをPMの品質ゲートで包むオーケストレーター。
「自信がないなら止める、終わったら証拠で確認、失敗したら学ぶ」を自動化する。

---

## Pipeline Flow

```
User Request
    ↓
┌─────────────────────────────────┐
│  PHASE 1: PRE-IMPLEMENTATION    │
│  (pm-confidence-check)          │
│                                 │
│  ≥90% → Proceed                │
│  70-89% → Present options       │
│  <70% → STOP, ask questions     │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  PHASE 2: IMPLEMENTATION        │
│  (devops-pipeline)              │
│                                 │
│  Normal devops pipeline runs    │
│  All existing steps execute     │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  PHASE 3: POST-IMPLEMENTATION   │
│  (pm-self-check)                │
│                                 │
│  4 Questions + 7 Red Flags      │
│  PASS → Proceed to commit       │
│  FAIL → Loop back to fix        │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  PHASE 4: ERROR HANDLING        │
│  (pm-reflexion)                 │
│                                 │
│  On ANY failure in Phase 2-3:   │
│  Search known → Investigate →   │
│  Record → Resume                │
└─────────────────────────────────┘
```

---

## Phase 1: Pre-Implementation (pm-confidence-check)

<!-- フェーズ1: 実装前チェック — 自信がなければ止める -->

**Invoke**: `pm-confidence-check` skill

### Actions:
1. Identify task type (NEW / FEATURE / BUGFIX / PATCH)
2. Run 5-dimension assessment
3. Gate decision based on score

### Gate Rules:

| Score | Action | Next Phase |
|-------|--------|------------|
| ≥ 90% | Log confidence, proceed | → Phase 2 |
| 70–89% | Present 2-3 alternative approaches to user | Wait for user choice → Phase 2 |
| < 70% | STOP. List what's unknown. Ask user questions. | Wait for answers → Re-run Phase 1 |

---

## Phase 2: Implementation (devops-pipeline)

<!-- フェーズ2: 実装 — 既存のDevOpsパイプラインをそのまま実行 -->

**Invoke**: `devops-pipeline` agent (existing)

The devops-pipeline runs exactly as before:
- STEP_0: project-context check
- STEP_MODE: mode detection
- STEP_REQUIREMENTS → STEP_ARCH → STEP_CODE → ...
- All existing skills execute normally

**PM addition**: If any step fails, immediately trigger Phase 4 (pm-reflexion) before retrying.

---

## Phase 3: Post-Implementation (pm-self-check)

<!-- フェーズ3: 実装後チェック — 証拠で完了を確認 -->

**Invoke**: `pm-self-check` skill

### Actions:
1. Run The Four Questions (tests, requirements, assumptions, evidence)
2. Scan for 7 hallucination red flags
3. Generate self-check report

### Gate Rules:

| Verdict | Action |
|---------|--------|
| ✅ COMPLETE | Proceed to git commit (devops-git-commit) |
| ❌ INCOMPLETE | List issues → Fix → Re-run Phase 3 |
| 🚨 HALLUCINATION | Flag to user → Require manual verification |

### Max Retry: 3 loops

If Phase 3 fails 3 times → escalate to user with full report.

---

## Phase 4: Error Handling (pm-reflexion)

<!-- フェーズ4: エラーハンドリング — 失敗から学ぶ -->

**Invoke**: `pm-reflexion` skill

Triggered automatically when:
- Phase 2 (implementation) has a step failure
- Phase 3 (self-check) detects issues
- Tests fail during any phase
- User reports a mistake

### Actions:
1. Search known solutions in `docs/memory/solutions_learned.jsonl`
2. If found → apply known fix → resume
3. If not found → root cause analysis → record → resume
4. Update PDCA documentation

---

## Integration with Existing devops-pipeline

<!-- 既存DevOpsパイプラインとの統合方法 -->

PM-pipeline does NOT replace devops-pipeline. It wraps it:

```
WITHOUT PM:
  User Request → devops-pipeline → commit

WITH PM:
  User Request → pm-confidence-check → devops-pipeline → pm-self-check → commit
                                           ↑                    |
                                           └── pm-reflexion ←───┘ (on failure)
```

### How to Use

**Option A: Full PM mode** (recommended for new features and complex tasks)
```
User: "PM모드로 개발해줘" or "pm pipeline으로 시작"
→ Runs full Phase 1-4
```

**Option B: Selective** (for quick patches)
```
User: "자신감 체크만 해줘" → Phase 1 only
User: "셀프 체크 해줘" → Phase 3 only
User: "에러 분석해줘" → Phase 4 only
```

**Option C: Auto-integration** (via CLAUDE.md routing)
```
CLAUDE.md routes coding tasks → devops-pipeline
devops-pipeline internally calls pm-confidence-check at start
devops-pipeline internally calls pm-self-check before commit
```

---

## Configuration

<!-- 設定 — プロジェクトごとにPM強度を調整可能 -->

### PM Intensity Levels

| Level | Confidence Gate | Self-Check | Reflexion | Use When |
|-------|----------------|------------|-----------|----------|
| **STRICT** | ≥ 90% required | Full 4Q + 7RF | Always record | Production code, critical features |
| **NORMAL** | ≥ 70% required | 4Q only | Record on failure | Regular development |
| **LIGHT** | Skip | Quick check | Skip | Patches, comments, docs |

Default: **NORMAL**

Override: User can specify level in request.

---

## Output Format

```yaml
pm_pipeline_result:
  phase_1_confidence:
    score: 0.XX
    level: HIGH | MEDIUM | LOW
    action: PROCEED | OPTIONS_PRESENTED | STOPPED
  phase_2_implementation:
    mode: NEW | FEATURE | BUGFIX | PATCH
    steps_executed: [...]
    status: COMPLETE | FAILED
  phase_3_self_check:
    verdict: COMPLETE | INCOMPLETE
    attempts: N
    red_flags: [...]
  phase_4_reflexion:
    triggered: true | false
    known_solution_used: true | false
    errors_recorded: N
  final_status: SUCCESS | FAILED | ESCALATED
```
