# Skill Agent Factory — 동작 흐름 정리

> 전체 에이전트 4개 + 스킬 15개가 어떻게 연결되어 움직이는지를 단계별로 설명합니다.
> 최종 업데이트: 2026-02-23

---

## 전체 구조 한눈에 보기

```
사용자 요청
    │
    ▼
┌─────────────────────────────────────────┐
│   skill-router  (PRIMARY ENTRY POINT)   │
│   Step 0: model-strategy.md 읽기        │
│   Phase 1: registry.md 빠른 필터        │
│   Phase 2: SKILL.md 정밀 매칭           │
│   Phase 3: requires: 의존성 해결        │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼──────────────────┐
    │            │                  │
    ▼            ▼                  ▼
devops-     figma-to-code    project-
pipeline      (에이전트)      onboarding
(에이전트)                    (에이전트)
    │
15개 스킬
```

**에이전트 4개**

| 에이전트 | 역할 | 모델 |
|---------|------|------|
| `skill-router` | 모든 요청의 진입점, 라우팅 | sonnet |
| `devops-pipeline` | 개발 파이프라인 오케스트레이터 | sonnet |
| `figma-to-code` | Figma → 프로덕션 코드 변환 | opus |
| `project-onboarding` | 프로젝트 최초 1회 초기화 | sonnet |

**스킬 15개**

| 카테고리 | 스킬 |
|---------|------|
| devops (10개) | requirements, safety-check, code-review, arch-review, japanese-comments, frontend-review, version-check, test-gen, git-commit, skill-eval |
| figma (5개) | design-token-extractor, framework-figma-mapper, design-analyzer, code-sync, responsive-validator |

---

## 1. 프로젝트 시작 — project-onboarding

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

## 2. 요청 라우팅 — skill-router

**모든 요청의 첫 번째 관문. devops-pipeline, figma-to-code를 직접 호출하지 말 것.**

```
Step 0-1: _docs/model-strategy.md 읽기
    └── 태스크 타입별 최적 모델 파악
        (Figma→코드: opus / 코드작업: sonnet / 경량: haiku)

Step 0-2: project-context 존재 체크 (코딩 요청인 경우만)
    ├── project-context/structure.md 있음 → 정상 진행
    └── 없음 → 사용자에게 선택지 제시
        A) project-onboarding 실행 후 재개 (추천)
        B) 그냥 진행

Phase 1: registry.md Tags 빠른 필터
    └── 요청에서 인텐트 태그 추출 → SKILL.md의 tags: 와 교집합 계산
        교집합 1개↑ → 후보 / 교집합 없으면 description 폴백
        목표: 후보 3~5개로 좁힘
        ※ 자연어 description 매칭보다 정밀 → 스킬 50개↑에서도 충돌 없음

Phase 2: SKILL.md 정밀 매칭
    └── 각 후보의 SKILL.md를 직접 읽어 스코어 계산
        tags 교집합 +3 / "Use when..." 일치 +4 / 카테고리 일치 +2
        7점↑ → 실행 / 4~6점 → 보조 / 4점↓ → 제외

Phase 3: requires: 의존성 해결
    └── 선택된 스킬의 requires: 필드 확인
        → 의존 순서대로 실행 (순환 의존 감지 시 중단)

Step 4: 실행 플랜 표시 → 즉시 실행 (사용자 확인 불필요)

Step 5: 실행
    ├── 코딩 작업 → 引き継ぎ情報 블록에 推定 MODE 포함 → devops-pipeline
    ├── Figma 작업 → figma-to-code
    ├── 프로젝트 초기화 → project-onboarding
    └── 비코딩 작업 → 스킬만 실행
```

**MODE 推定 (skill-router가 인계 시 포함):**

| 시그널 | 추정 MODE |
|--------|---------|
| "새로", "처음", "create", "implement" | NEW |
| "추가", "확장", "add", "extend" | FEATURE |
| "버그", "고쳐", "fix", "error" | BUGFIX |
| "주석", "설정", "typo", "rename" | PATCH |

---

## 3. 개발 파이프라인 — devops-pipeline

**skill-router에서 인계받거나, 사용자가 명시적으로 파이프라인을 언급할 때만 직접 실행.**

### MODE 감지 (우선순위 순)

```
① skill-router 引き継ぎ情報 블록이 있으면 → 재분석 없이 바로 STEP_PLAN
② 사용자가 "mode: new/feature/bugfix/patch" 명시 → 그대로 사용
③ 위 둘 다 없을 때 → 키워드 자동 감지
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
  → project-context/structure.md의 ## Main Module 확인 (없으면 사용자에게 1번 질문 → 추가)
  → 폴더 구조/파일 책임/명명/중복/try-catch/로그 레벨 검사
STEP_JAPANESE   → 영어 주석 → 일본어 변환
STEP_FRONTEND   → Figma: figma-code-sync + responsive-validator / 스크린샷: frontend-review
STEP_VERSION    → deprecated API / 의존성 안정성
STEP_TESTS      → NEW/FEATURE: 해피패스+에러+엣지케이스 / BUGFIX: 회귀 테스트
STEP_COMMIT     → 반드시 사용자 확인 후 커밋 (feature/{번호}/{이름} 브랜치)
```

---

## 4. Figma → 코드 변환 — figma-to-code

**언제:** skill-router가 Figma 시그널 감지 시 라우팅, 또는 devops-pipeline FIGMA_PREFLIGHT가 위임

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

## 5. 스킬 품질 관리 — devops-skill-eval

**언제:** 새 스킬 만들거나 수정한 후 배포 전 검증

```
3개 시나리오 테스트
  - 해피패스 / 엣지케이스 / 오트리거 방지

5차원 채점 (총 100점, 75점 이상 → 배포 OK)
  - 트리거 정확도 30% / 스텝 커버리지 25%
  - 출력 형식 20% / requires 준수 15% / 오트리거 없음 10%
```

---

## 6. 자동화 유틸리티

```bash
python3 scripts/sync-registry.py
# skills/*/SKILL.md + agents/*.md 전체 스캔
# registry.md 테이블 + README.md 통계 자동 갱신
# install.sh 실행 시 자동으로 함께 실행됨
```

```bash
./install.sh
# 스킬/에이전트 심링크를 ~/.claude/skills/, ~/.claude/agents/ 에 생성
# 고아 심링크 자동 정리: skills/ 에서 삭제된 스킬의 심링크를 ~/.claude/skills/ 에서도 제거
# install.sh를 다시 실행하면 고아 심링크 제거 + 최신 목록으로 동기화
```

```bash
python3 scripts/lint-skills.py
# 스킬/에이전트 품질 자동 검사 (install.sh 실행 시 자동 포함)
# 검사 항목:
#   ✗ ERROR  — frontmatter 누락 (name/description), 존재하지 않는 requires 참조, 순환 참조
#   ⚠ WARN   — 스텝 정의 누락, deprecated 스킬, 삭제된 파일 경로 참조, 의존 체인 깊이 3↑
# --strict 옵션: 경고도 에러로 처리 → CI/CD 환경에서 merge 블로킹 가능
```

```bash
python3 scripts/dep-graph.py
# 전체 의존성 트리 출력 (requires: 관계 시각화)

python3 scripts/dep-graph.py --reverse <skill-name>
# 역방향 조회: 이 스킬을 삭제/변경하면 어떤 스킬이 영향받는지

python3 scripts/dep-graph.py --check
# 문제 있는 의존 관계만 요약 출력 (존재하지 않는 참조, deprecated 의존, 깊은 체인)
```

---

## 7. 전체 흐름 예시 — "유저 인증 API 새로 만들어줘"

```
① skill-router
   Step 0: model-strategy.md 읽기 → sonnet (코드 생성)
   Phase 1: "API / auth / 새로" → tags 추출 [code, requirements, feature, planning]
           → registry.md tags 교집합: devops-requirements(3개), devops-arch-review(1개) 후보
   Phase 2: devops-requirements SKILL.md 정밀 매칭 (score 11)
   引き継ぎ情報: MODE = NEW, Figma = なし

② devops-pipeline (引き継ぎ情報 수신 → STEP_PLAN으로 바로 이동)
   STEP_REQUIREMENTS
     → project-context/structure.md 읽기 (기존 파일 스코프 확인)
     → project-context/instruction.md 읽기 (명명 패턴 확인)
     → "JWT 방식? 세션 방식?" 사용자에게 확인

   Development → JWT 인증 코드 작성

   STEP_SAFETY → JWT 시크릿 하드코딩 없음 ✅
   STEP_CODE_REVIEW → 토큰 만료 처리 누락 발견 → 수정
   STEP_ARCH (NEW)
     → project-context/structure.md의 ## Main Module 확인
     → 아키텍처 검토 3건 수정
   STEP_JAPANESE → 영어 주석 12개 → 일본어 변환
   STEP_VERSION → 문제 없음 ✅
   STEP_TESTS → 로그인 성공/토큰 만료/잘못된 비번 → 8개 생성
   STEP_COMMIT
     → 브랜치: feature/AUTH-001/user-auth
     → 사용자에게 커밋 내용 보여줌 → 확인 후 커밋
```

---

## 8. 파일 구조

```
skill-agent-factory/
├── agents/
│   ├── skill-router.md         ← PRIMARY ENTRY POINT
│   ├── devops-pipeline.md      ← 개발 파이프라인
│   ├── figma-to-code.md        ← Figma → 코드
│   └── project-onboarding.md  ← 프로젝트 초기화 (최초 1회)
├── skills/
│   ├── devops-*/               ← devops 스킬 10개
│   └── figma-*/                ← figma 스킬 5개
├── standards/
│   └── CODING-STANDARDS.md    ← 글로벌 코딩 규칙 (Rules 1~10)
├── project-context/            ← 프로젝트별 컨텍스트 (온보딩 후 생성)
│   ├── structure.md            ← 폴더 구조 + 기존 파일 목록 + Main Module
│   └── instruction.md         ← 발견된 코드 패턴 (관찰, 규칙 아님)
├── _docs/
│   ├── model-strategy.md       ← 태스크 타입별 최적 모델 정의
│   └── how-it-works.md        ← 이 파일
├── scripts/
│   └── sync-registry.py       ← 레지스트리 자동 동기화
└── registry.md                 ← 전체 스킬/에이전트 목록 (19개)
```

---

*Last updated: 2026-02-23 (①~⑧, A~F 수정 반영)*
