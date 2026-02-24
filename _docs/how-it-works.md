# Skill Agent Factory — 동작 흐름 정리

> Plugin 기반 구조, 3-Tier 스킬 아키텍처, Agent Teams 패턴이 어떻게 연결되어 움직이는지를 단계별로 설명합니다.
> 최종 업데이트: 2026-02-23

---

## 전체 구조 한눈에 보기

```
사용자 요청
    │
    ▼
┌──────────────────────────────────────────────┐
│   CLAUDE.md (PRIMARY ENTRY POINT)            │
│   • 모든 개발 요청을 devops-pipeline으로 라우팅  │
│   • registry.md/metadata.md로 스킬 자동 선택   │
└────────────────┬─────────────────────────────┘
                 │
    ┌────────────┼──────────────────┐
    │            │                  │
    ▼            ▼                  ▼
devops-     figma-to-code    project-
pipeline      (에이전트)      onboarding
(에이전트)                    (에이전트)
    │
    ├── review-team   (병렬)
    ├── quality-team  (순차)
    ├── commit-team   (순차)
    └── feature-team  (게이트)
```

**에이전트 3개**

| 에이전트 | 역할 | 모델 | 플러그인 |
|---------|------|------|---------|
| `devops-pipeline` | 개발 파이프라인 오케스트레이터 | sonnet | devops |
| `figma-to-code` | Figma → 프로덕션 코드 변환 | opus | figma |
| `project-onboarding` | 프로젝트 최초 1회 초기화 | sonnet | project |

**스킬 18개 (3개 플러그인)**

| 플러그인 | 스킬 |
|---------|------|
| devops (10개) | requirements, safety-check, code-review, arch-review, japanese-comments, frontend-review, version-check, test-gen, git-commit, skill-eval |
| figma (5개) | design-token-extractor, framework-figma-mapper, design-analyzer, code-sync, responsive-validator |
| vertx (3개) | vertx-repo-analyzer, vertx-eventbus-register, vertx-api-caller |

---

## 1. 플러그인 구조 — plugins/

모든 스킬과 에이전트는 플러그인 단위로 그룹화됩니다.

```
plugins/
├── devops/
│   ├── plugin.json              ← 플러그인 메타 + 팀 멤버 선언
│   ├── agents/devops-pipeline.md
│   └── skills/
│       └── devops-code-review/
│           ├── metadata.md      ← Tier 1: 라우팅용 (항상 로드)
│           ├── SKILL.md         ← Tier 2: 전체 지침 (선택 시 로드)
│           └── resources/       ← Tier 3: 체크리스트/템플릿 (요청 시)
├── figma/
│   ├── plugin.json
│   ├── agents/figma-to-code.md
│   └── skills/...
└── project/
    ├── plugin.json
    └── agents/project-onboarding.md
```

### 3-Tier 스킬 아키텍처

| Tier | 파일 | 로드 시점 | 내용 |
|------|------|---------|------|
| **Tier 1** | `metadata.md` | **항상** — 경량 라우팅 (~10줄) | tags, use-when, model, version |
| **Tier 2** | `SKILL.md` | 스킬 선택 시만 | 전체 지침, STEP 정의 |
| **Tier 3** | `resources/` | 필요 시 on-demand | 체크리스트, 템플릿, 예시 |

이 방식으로 Claude는 필요한 것만 읽어 컨텍스트를 최소화합니다.

---

## 2. 라우팅 방식

### CLAUDE.md 직접 라우팅 (구 방식: agent 기반 라우팅은 제거됨)

`CLAUDE.md`가 직접 라우팅 규칙을 담습니다:

```
모든 개발 요청
    → devops-pipeline (자동)

Figma URL 포함 요청
    → devops-pipeline 내 FIGMA_PREFLIGHT
    → figma-to-code 에이전트에 위임

프로젝트 초기화 (project-context/ 없을 때)
    → project-onboarding (한 번만 실행)
```

스킬 선택은 `metadata.md`의 `tags:` 와 `use-when:` 필드를 기반으로 자동 매칭됩니다.

---

## 3. 프로젝트 시작 — project-onboarding

**언제:** 새 프로젝트에서 처음 한 번만 실행

```
STEP 0: project-context/structure.md가 이미 있으면 → 즉시 스킵 (캐시)
    │
    ▼
STEP 1: 코드 파일 자동 감지
    ├── 코드 파일 있음 → EXISTING 판단
    └── 코드 파일 없음 → NEW 판단
    │   사용자에게 1번만 확인
    ▼
┌──────────────────────┬───────────────────────┐
│    기존 프로젝트 (2A)  │    신규 프로젝트 (2B)   │
│ git ls-files로        │ 언어/프레임워크 확인     │
│ 기존 파일 스코프 기록   │ CODING-STANDARDS.md   │
│ 명명/import/에러처리  │ 기반 폴더 구조 제안      │
│ 패턴 코드에서 분석     │ 사용자 확인             │
└──────────┬───────────┴───────────────────────┘
           ▼
STEP 3: project-context/ 생성
    ├── structure.md  → 폴더 구조 + 기존 파일 목록 + ## Main Module
    └── instruction.md → 발견된 코드 패턴 (규칙 아님, 관찰한 패턴)
```

**핵심 포인트:**
- `instruction.md` = "이 프로젝트는 camelCase를 씀" 같은 **관찰**
- `CODING-STANDARDS.md` = try/catch 방법, 로그 레벨 등 **글로벌 규칙**
- 두 파일은 내용 중복 없음

---

## 4. 개발 파이프라인 — devops-pipeline

**모든 개발 요청의 실행 엔진. CLAUDE.md가 자동으로 위임합니다.**

### MODE 감지 (우선순위 순)

```
① 사용자가 "mode: new/feature/bugfix/patch" 명시 → 그대로 사용
② 위 없을 때 → 키워드 자동 감지
   "새로", "처음", "create", "implement" → NEW
   "추가", "확장", "add", "extend"       → FEATURE
   "버그", "고쳐", "fix", "error"        → BUGFIX
   "주석", "설정", "typo", "rename"      → PATCH
```

### 모드별 실행 스텝

```
스텝                    NEW    FEATURE   BUGFIX   PATCH
─────────────────────────────────────────────────────
STEP_REQUIREMENTS       ✅      ✅        ⏭️       ⏭️
FIGMA_PREFLIGHT         조건    조건      ⏭️       ⏭️
Development             ✅      ✅        ✅       ✅
STEP_SAFETY             ✅      ✅        ✅       ✅
STEP_CODE_REVIEW        ✅      ✅        ✅       ⏭️
STEP_ARCH               ✅      ⏭️        ⏭️       ⏭️
STEP_JAPANESE           ✅      ✅        ✅       ✅
STEP_FRONTEND           조건    조건      ⏭️       ⏭️
STEP_VERSION            ✅      ✅        ✅       ⏭️
STEP_TESTS              ✅      ✅        ✅       ⏭️
STEP_COMMIT             ✅      ✅        ✅       ✅
```

### 각 스텝 상세

```
STEP_REQUIREMENTS
  ① project-context/structure.md 읽기 (기존 파일 스코프, 언어/프레임워크)
  ② project-context/instruction.md 읽기 (명명/import/에러처리 패턴)
  ③ 불명확한 점 사용자에게 확인
  [Gate] 요건 확정 전 코드 작성 안 함

FIGMA_PREFLIGHT (Figma URL 있을 때만)
  → figma-to-code 에이전트에 위임 (직접 Figma 스킬 실행 안 함)
  → figma-to-code Phase 1~4 완료 후 STEP_SAFETY부터 재개

STEP_SAFETY     → 시크릿/취약점/인젝션 스캔 (CRITICAL만 즉시 수정)
STEP_CODE_REVIEW → 로직 정확성/엣지케이스/메모리 누수/N+1
STEP_ARCH (NEW만)
  → project-context/structure.md의 ## Main Module 확인
  → 폴더 구조/파일 책임/명명/중복/try-catch/로그 레벨 검사
STEP_JAPANESE   → 영어 주석 → 일본어 변환
STEP_FRONTEND   → Figma: figma-code-sync + responsive-validator / 스크린샷: frontend-review
STEP_VERSION    → deprecated API / 의존성 안정성
STEP_TESTS      → NEW/FEATURE: 해피패스+에러+엣지케이스 / BUGFIX: 회귀 테스트
STEP_COMMIT     → 반드시 사용자 확인 후 커밋 (feature/{번호}/{이름} 브랜치)
```

---

## 5. Agent Teams 패턴

스킬들은 **팀** 단위로 그룹화되어 조율 실행됩니다. 팀 멤버십은 각 `plugin.json`에 선언됩니다.

### 4가지 팀

| 팀 | 실행 방식 | 용도 |
|----|---------|------|
| `review-team` | **Parallel** (병렬) | 코드 품질 다각도 검토 |
| `quality-team` | **Sequential** (순차) | 테스트/일본어/버전 체크 |
| `commit-team` | **Sequential** (순차) | 커밋 처리 |
| `feature-team` | **Gated** (게이트) | 기능 개발 전 요건/설계 확인 |

### plugin.json 선언 방식

```json
{
  "name": "devops",
  "teams": {
    "review-team":  ["devops-code-review", "devops-arch-review", "devops-safety-check"],
    "quality-team": ["devops-test-gen", "devops-japanese-comments", "devops-version-check"],
    "commit-team":  ["devops-git-commit"],
    "feature-team": ["devops-requirements", "devops-frontend-review"]
  }
}
```

**`make lint`** 가 잘못된 팀명이나 존재하지 않는 스킬 참조를 자동 검출합니다.

**`make sync`** 가 plugin.json의 teams: 정보를 읽어 README.md 의 Agent Teams 테이블을 자동 업데이트합니다.

---

## 6. Figma → 코드 변환 — figma-to-code

**언제:** devops-pipeline의 FIGMA_PREFLIGHT가 위임, 또는 Figma URL이 포함된 요청

```
Phase 1: 프레임워크 확인 (React/Vue/PrimeFaces/Next.js 등)

Phase 2: 디자인 분석 (requires: 필드 기반 순서 결정)
  ① figma-design-token-extractor  (requires: 없음 → 최초 실행)
       → tokens.css, tailwind.config 생성
  ② figma-framework-figma-mapper  (requires: [token-extractor])
       → 컴포넌트 매핑표 생성
  ③ figma-design-analyzer         (requires: [token-extractor, mapper])
       → 구현 순서 포함 blueprint.md 생성

Phase 3: 코드 생성 (blueprint.md 순서대로)
  - 매핑된 프레임워크 컴포넌트 우선, 커스텀 최소화
  - 디자인 토큰 사용 (하드코딩 금지)
  - 일본어 주석, 파일 헤더 필수

Phase 4: 검증 루프 (최대 3회)
  - figma-code-sync → 구현 vs 매핑 일치 확인
  - figma-responsive-validator → Mobile/Tablet/Desktop 반응형 검증
  - FAIL/WARN 있으면 수정 → 재검증

Phase 5: devops-pipeline 연동
  STEP_SAFETY → STEP_CODE_REVIEW → STEP_JAPANESE
  → STEP_VERSION → STEP_TESTS → STEP_COMMIT
```

---

## 7. 스킬 품질 관리 — devops-skill-eval

**언제:** 새 스킬 만들거나 수정한 후 배포 전 검증

```
3개 시나리오 테스트
  - 해피패스 / 엣지케이스 / 오트리거 방지

5차원 채점 (총 100점, 75점 이상 → 배포 OK)
  - 트리거 정확도 30% / 스텝 커버리지 25%
  - 출력 형식 20% / requires 준수 15% / 오트리거 없음 10%
```

---

## 8. 자동화 유틸리티

모든 명령은 **`make`** 로 실행합니다:

```bash
make install      # symlink skills/agents to ~/.claude/
make lint         # 스킬/에이전트 품질 검사 (frontmatter, teams, dep chains)
make lint-strict  # 경고도 에러로 처리
make sync         # registry.md + README.md (Skills + Teams 테이블) 자동 갱신
make graph        # 전체 의존성 트리 출력
make check        # 의존성 문제만 요약
make validate     # lint + sync + check 일괄 실행 (커밋 전 반드시)
```

### sync-registry.py 가 자동 업데이트하는 항목

```
registry.md
  └── ## Registry Table       ← 전체 스킬/에이전트 목록 테이블

README.md
  ├── ## Current Skills & Agents ← 플러그인별 스킬/에이전트 테이블
  └── ## Agent Teams             ← plugin.json teams: 집약 테이블
      (<!-- TEAMS_TABLE_START/END --> 마커 사이 자동 교체)
```

### lint-skills.py 검사 항목

```
✗ ERROR  — frontmatter 누락 (name/description), 존재하지 않는 requires 참조,
           순환 참조, 잘못된 팀명, 미존재 스킬의 팀 등록
⚠ WARN   — 스텝 정의 누락, deprecated 스킬 의존, 깊은 dep 체인 (3단계↑)
           tags 미설정, description/use-when 미설정
```

### dep-graph.py 사용법

```bash
python3 scripts/dep-graph.py              # 전체 의존성 트리
python3 scripts/dep-graph.py --reverse <skill>  # 이 스킬 삭제 시 영향 범위
python3 scripts/dep-graph.py --check            # 문제 있는 의존 관계만 요약
```

---

## 9. 전체 흐름 예시 — "유저 인증 API 새로 만들어줘"

```
① CLAUDE.md 라우팅
   → 개발 요청 감지 → devops-pipeline 자동 위임
   → MODE 감지: "새로" → NEW

② devops-pipeline (feature-team 게이트 진입)
   STEP_REQUIREMENTS
     → project-context/structure.md 읽기 (기존 파일 스코프 확인)
     → project-context/instruction.md 읽기 (명명 패턴 확인)
     → "JWT 방식? 세션 방식?" 사용자에게 확인

   Development → JWT 인증 코드 작성

③ review-team (병렬 실행)
   STEP_SAFETY     → JWT 시크릿 하드코딩 없음 ✅
   STEP_CODE_REVIEW → 토큰 만료 처리 누락 발견 → 수정
   STEP_ARCH (NEW)  → 아키텍처 검토 3건 수정

④ quality-team (순차 실행)
   STEP_JAPANESE → 영어 주석 12개 → 일본어 변환
   STEP_VERSION  → 문제 없음 ✅
   STEP_TESTS    → 로그인 성공/토큰 만료/잘못된 비번 → 8개 생성

⑤ commit-team (순차 실행)
   STEP_COMMIT
     → 브랜치: feature/AUTH-001/user-auth
     → 사용자에게 커밋 내용 보여줌 → 확인 후 커밋
```

---

## 10. 파일 구조

```
skill-agent-factory/
├── CLAUDE.md              ← 포인터 파일 + 라우팅 규칙 (상세는 _docs/ 참조)
├── README.md              ← 자동 업데이트 (make sync)
├── Makefile               ← Dev commands
├── registry.md            ← 자동 업데이트 (make sync)
├── install.sh             ← 심링크 생성 + 고아 심링크 정리
├── plugins/               ← 모든 스킬 & 에이전트
│   ├── devops/
│   │   ├── plugin.json        ← 팀 멤버십 선언
│   │   ├── agents/devops-pipeline.md
│   │   └── skills/{name}/
│   │       ├── metadata.md    ← Tier 1 (항상 로드)
│   │       ├── SKILL.md       ← Tier 2 (선택 시 로드)
│   │       └── resources/     ← Tier 3 (요청 시 로드)
│   ├── figma/
│   │   ├── plugin.json
│   │   ├── agents/figma-to-code.md
│   │   └── skills/{name}/
│   ├── project/
│   │   ├── plugin.json
│   │   └── agents/project-onboarding.md
│   └── vertx/
│       ├── plugin.json
│       ├── resources/api-reference/   ← API docs (공유 리소스)
│       └── skills/{name}/
├── scripts/
│   ├── sync-registry.py   ← registry.md + README.md 자동 갱신
│   ├── lint-skills.py     ← 품질 검사 (frontmatter, teams, deps)
│   └── dep-graph.py       ← 의존성 트리 + 역방향 조회
├── standards/
│   └── CODING-STANDARDS.md
└── _docs/
    ├── how-it-works.md    ← 이 파일
    ├── skills.md
    ├── sub-agents.md
    ├── hooks.md
    ├── plugins.md
    ├── mcp.md
    ├── output-styles.md
    └── agent-teams.md
```

---

## 11. 기능 추가 가이드

> 새 스킬·에이전트·플러그인·팀을 추가할 때의 체크리스트입니다.
> 순서를 지키면 `make validate`가 자동으로 문제를 잡아줍니다.

---

### A. 스킬 하나 추가하기

```
1. 디렉토리 생성
   mkdir -p plugins/{plugin}/skills/{plugin}-{name}

2. metadata.md 작성 (Tier 1 — 필수)
   ---
   name: {plugin}-{name}
   version: v1.0
   description: 무엇을 하는 스킬인지 한 줄 설명
   tags: [domain, action, ...]
   use-when: >
     언제 이 스킬을 써야 하는지 자연어로 설명
   model: sonnet
   allowed-tools: Read, Grep, Glob
   ---

3. SKILL.md 작성 (Tier 2 — 필수)
   ---
   name: {plugin}-{name}
   version: v1.0
   description: ...
   tags: [...]
   requires: []          # 의존 스킬이 있으면 여기에 추가
   allowed-tools: ...
   ---
   # 스킬 제목
   ## 지침 (Step-by-step)
   ...

4. resources/ 추가 (Tier 3 — 선택)
   mkdir -p plugins/{plugin}/skills/{plugin}-{name}/resources
   # 체크리스트, 템플릿, 예시 파일 등을 배치

5. plugin.json 의 teams: 에 추가 (해당 팀이 있으면)
   "review-team": ["...", "{plugin}-{name}"]

6. 검증
   make validate
   # ✅ 에러 없으면 완료
```

---

### B. 에이전트 추가하기

```
1. 파일 생성
   touch plugins/{plugin}/agents/{plugin}-{agent-name}.md

2. 프론트매터 작성
   ---
   name: {plugin}-{agent-name}
   version: v1.0
   description: 이 에이전트가 하는 일
   tools: Read, Write, Edit, Bash, Grep, Glob
   model: sonnet          # 복잡한 오케스트레이션은 opus
   ---

3. 지침 본문 작성
   ## 역할
   ## 실행 단계
   ## 제약사항

4. 검증
   make validate && make sync
   # sync 후 README.md Agent 테이블이 자동 갱신됨
```

---

### C. 새 플러그인 추가하기 (예: backend)

```
1. 디렉토리 구조 생성
   mkdir -p plugins/backend/skills
   mkdir -p plugins/backend/agents

2. plugin.json 작성
   {
     "name": "backend",
     "version": "1.0.0",
     "description": "Backend development skills and agents",
     "teams": {
       "review-team":  [],
       "quality-team": [],
       "commit-team":  [],
       "feature-team": []
     }
   }

3. categories/backend/CLAUDE.md 의 Directory Layout 업데이트

4. 스킬·에이전트를 위 A/B 가이드대로 추가

5. 검증
   make validate
```

---

### D. Agent Teams 구현하기 (현재: 선언만 존재, 오케스트레이터 미구현)

**현재 상태:**
- `plugin.json` 의 `teams:` 필드로 멤버십은 선언됨
- `make lint` 가 팀 정합성 자동 검증
- **실제 팀 오케스트레이터 에이전트는 아직 없음**

**구현 로드맵:**

```
Step 1 — 팀 오케스트레이터 에이전트 작성
   touch plugins/devops/agents/devops-team-runner.md

   역할: plugin.json의 teams: 를 읽어
         해당 팀의 스킬들을 지정 방식으로 실행

   review-team  → Task 툴로 병렬 서브에이전트 실행
   quality-team → 스킬 순서대로 순차 실행
   commit-team  → 순차 실행 + 사용자 확인 게이트
   feature-team → 첫 스킬 완료 후 다음 스킬 실행 (게이트)

Step 2 — CLAUDE.md 라우팅에 팀 실행 트리거 추가
   예: "전체 리뷰 돌려줘" → review-team 실행
   예: "코드 품질 체크" → quality-team 실행

Step 3 — make validate 에 팀 실행 테스트 추가
   devops-skill-eval 스킬로 팀 단위 시나리오 테스트

예시 — review-team 오케스트레이터:
─────────────────────────────────
---
name: devops-team-runner
description: Runs Agent Teams by reading plugin.json teams declaration.
  Invoke with "run {team-name}" to execute all member skills.
model: sonnet
tools: Read, Task
---

## 実行手順

1. `plugins/devops/plugin.json` を読み込み、指定された team のメンバー一覧を取得
2. チームタイプに応じて実行方式を決定:
   - review-team  → Task ツールで全メンバーを並列実行
   - quality-team → メンバーを順次実行
   - commit-team  → 順次実行 → ユーザー確認 → コミット
   - feature-team → Gate: 前スキル完了後に次スキル実行
3. 各スキルの結果を集約してサマリー出力
─────────────────────────────────
```

---

### E. 既存スキルに resources/ を追加する

```
1. ディレクトリ生成
   mkdir -p plugins/{plugin}/skills/{skill-name}/resources

2. ファイル配置 (例)
   resources/checklist.md    ← 확인 항목 목록
   resources/template.md     ← 출력 템플릿
   resources/examples/       ← 입력/출력 예시 모음

3. SKILL.md 본문에서 on-demand 로드 지시 추가
   ## 리소스 활용
   필요 시 `resources/checklist.md` 를 읽어 항목별로 검사한다.
   (항상 읽지 않음 — 사용자가 요청하거나 해당 단계에 도달했을 때만)

4. 검증
   make lint   # Tier 3 파일은 lint 대상 아님, 이상 없으면 OK
```

---

### F. 어떤 변경이 make validate 에서 자동으로 잡히나?

| 실수 | 잡히는 체크 |
|------|------------|
| `requires:` 에 존재하지 않는 스킬명 기재 | ✗ ERROR — 의존성 참조 오류 |
| `teams:` 에 존재하지 않는 스킬명 기재 | ✗ ERROR — Teams 정합성 |
| `teams:` 에 정의되지 않은 팀명 사용 | ✗ ERROR — 미정의 팀명 |
| 순환 의존 (A→B→A) | ✗ ERROR — 순환 참조 |
| 의존 체인 3단계 이상 | ⚠ WARN — dep 체인 깊이 |
| `name:` / `description:` 누락 | ✗ ERROR — frontmatter 필수 필드 |
| 문서에 `skill-router` 참조 잔존 | ✗ ERROR — Doc Drift |
| 문서에 구 `skills/*/` 경로 잔존 | ✗ ERROR — Doc Drift |
| README.md Skills/Agents 테이블 outdated | 자동수정 — `make sync` |
| README.md Teams 테이블 outdated | 자동수정 — `make sync` |

**→ 새 기능을 추가한 후 `make validate` 가 통과하면 병합 준비 완료입니다.**

---

## 12. 설치 방법 (Usage Scope)

| 방법 | 명령 | 적용 범위 |
|------|------|---------|
| `./install.sh` | `~/.claude/skills/` 에 심링크 생성 | **User-level** — 모든 프로젝트, git clone 후 1회 실행 |
| Git submodule + `pluginDirs` | 프로젝트 내 embed | **Project-level** — repo에 번들, 팀 공유 가능 |
| `--plugin-dir` flag | 세션/프로젝트에 직접 지정 | **Project-level** — embedding 없이 간단하게 로드 |

**스킬/에이전트를 추가한 후에는 반드시 `./install.sh` 를 다시 실행하세요.**

---

## 13. 에셋 생성·업데이트 워크플로

새 에셋(스킬/에이전트/플러그인)을 만들 때 따르는 순서:

### Step 1 — 에셋 타입 분류

| 타입 | 언제 |
|------|------|
| **Skill** | Claude가 자동 또는 on-demand로 반복 수행할 작업 |
| **Agent** | 특정 도구와 워크플로를 가진 end-to-end 자율 작업 |
| **Plugin** | 여러 스킬/에이전트/hooks의 묶음 — 프로젝트 간 공유 |
| **Hook** | 라이프사이클 이벤트에서 결정론적으로 실행되는 명령 |
| **MCP Server** | 외부 API·도구와의 통합 |

### Step 2 — 레지스트리 중복 확인

```
1. registry.md 열기
2. 유사한 에셋 검색
3. 유사 존재 → 업데이트 제안, 사용자 확인 후 적용
4. 신규 → 생성 진행
```

### Step 3 — 관련 _docs/ 파일 먼저 읽기

| 만들 것 | 참조 파일 |
|---------|---------|
| Skill | `_docs/skills.md` |
| Agent | `_docs/sub-agents.md` |
| Plugin | `_docs/plugins.md` |
| Hook | `_docs/hooks.md` |
| MCP Server | `_docs/mcp.md` |
| Agent Team | `_docs/agent-teams.md` |

### Step 4 — 에셋 생성

위 A~E 가이드(스킬/에이전트/플러그인/resources 추가) 참조.

### Step 5 — 레지스트리 자동 동기화

```bash
make validate
# lint + registry.md 자동 갱신 + README.md 자동 갱신
```

`metadata.md`의 의미있는 변경 시 버전 수동 bump: `v1.0 → v1.1`

### Step 6 — install.sh 재실행 안내

새 스킬/에이전트 추가 후 사용자에게 반드시 알리기:
> "`./install.sh` 를 다시 실행해 주세요!"

---

## 14. 버저닝 전략

모든 에셋(`metadata.md`, `SKILL.md`, agent 파일)은 `version:` 필드를 가집니다.

### 버전 형식: `vMAJOR.MINOR`

| 변경 종류 | 버전 올리기 | 예시 | 기준 |
|---------|-----------|------|------|
| Breaking — 이름 변경, 단계 삭제, 출력 형식 변경 | **MAJOR** | v1.0 → v2.0 | 기존 사용자가 적응 필요 |
| Non-breaking — 새 단계 추가, 지침 개선, 태그 추가 | **MINOR** | v1.0 → v1.1 | 하위 호환 |
| 오타/주석/포맷만 수정 | **없음** | v1.0 유지 | 동작 변화 없음 |

### 작업 순서

```
1. 스킬/에이전트 내용 수정
2. metadata.md (+ SKILL.md) 의 version: bump
3. make validate  ← registry.md 자동 반영
4. git commit -m "feat: devops-code-review v1.0 → v1.1"
```

### 개별 CHANGELOG 불필요

`registry.md` 가 중앙 버전 원장 역할. `sync-registry.py` 실행 시 **Last Modified** 컬럼 자동 갱신.
외부 공개 스킬이 아닌 한 `CHANGELOG.md` 개별 관리는 불필요.

---

*Last updated: 2026-02-25 — plugins/ 구조, 3-tier, Agent Teams, Makefile, 자동화, Usage Scope, Versioning, Workflow 반영*
