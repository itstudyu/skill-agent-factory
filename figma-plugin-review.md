# Figma Plugin 평가 리포트

> 평가일: 2026-03-01 | 대상: `plugins/figma/` (v1.0.0)

---

## 총평: ⭐⭐⭐⭐ (4/5) — 설계 우수, 실전 검증 필요

전체적으로 **아키텍처 설계가 탄탄하고, 스킬 간 파이프라인이 잘 정의**되어 있다. 3-tier 구조(metadata → SKILL.md → resources)를 충실히 따르고 있으며, 의존성 그래프 기반의 실행 순서 해결도 잘 되어 있다. 다만 몇 가지 빈틈과 개선점이 보인다.

---

## 1. 구조 & 아키텍처 (★★★★★)

**좋은 점:**
- 5개 스킬 + 1개 에이전트가 명확한 역할 분리로 구성됨
- `requires:` 필드를 통한 의존성 체인이 깔끔함: `token-extractor → mapper → analyzer`
- `figma-to-code` 에이전트가 오케스트레이터 역할을 하면서, 각 스킬의 `requires:`를 동적으로 읽어 실행 순서를 결정하는 설계가 유연함
- plugin.json의 teams 분리가 합리적 (review-team: validator, feature-team: 나머지)
- category CLAUDE.md에 전체 워크플로우 흐름도가 잘 정리됨

**파이프라인 흐름:**
```
token-extractor → mapper → analyzer → [코드 생성] → code-sync → responsive-validator
```
이 흐름이 논리적으로 타당하고 각 단계의 입출력이 맞물림.

---

## 2. 개별 스킬 평가

### figma-design-token-extractor ⭐⭐⭐⭐
- **강점:** 4가지 출력 포맷(CSS, SCSS, Tailwind, JSON W3C) 지원이 실용적. 토큰 카테고리 분류가 체계적.
- **약점:**
  - Dark mode / 테마 변환 토큰 미지원 — Figma Variables의 mode(Light/Dark) 처리 로직이 없음
  - `tokens.json`이 W3C Design Token Community Group 포맷이라고 하면서 `$type: "dimension"` 같은 최신 스펙 반영이 미흡 (composite token, alias 등 미지원)

### figma-framework-figma-mapper ⭐⭐⭐⭐⭐
- **강점:** PrimeFaces 프리셋이 매우 상세함. confidence score 기반 매칭(40/30/30 가중치)이 체계적. JSON + MD 이중 출력이 에이전트/사람 모두에게 유용.
- **약점:** 거의 없음. 다만 커스텀 프레임워크 지원 시 WebFetch로 문서 크롤링하는데, 대형 문서의 경우 토큰 한계에 걸릴 수 있음.

### figma-design-analyzer ⭐⭐⭐⭐
- **강점:** ASCII 다이어그램 + 스크린샷 캡처 + 컴포넌트 계층 트리 + 빌드 순서까지 종합적. blueprint-template.md 리소스도 있음.
- **약점:**
  - `allowed-tools`에 `mcp__figma__export_node`가 있지만, 실제 스크린샷 저장/관리 워크플로우가 불명확 (어디에 저장? 상대경로?)
  - 리소스 파일 `blueprint-template.md`가 SKILL.md 본문과 상당히 중복됨

### figma-responsive-validator ⭐⭐⭐⭐
- **강점:** 7개 체크 카테고리(Overflow/Layout/Typography/Spacing/Navigation/Media/Touch)가 체계적. Grep 패턴까지 구체적으로 제시. 3회 반복 루프 프로토콜이 실용적.
- **약점:**
  - `model: haiku`로 설정되어 있는데, CSS 패턴 분석은 정확도가 중요하므로 `sonnet`이 더 적합할 수 있음
  - CSS-in-JS (styled-components, emotion) 패턴 미지원 — className 기반만 분석

### figma-code-sync ⭐⭐⭐⭐
- **강점:** 4가지 검증 축(Component Coverage / Token Usage / Props Alignment / Figma Snapshot)이 체계적. Sync Score 기준이 명확.
- **약점:**
  - `requires: [figma-framework-figma-mapper]`만 명시했지만 실제로는 `figma-design-token-extractor`도 필수 (Step 2에서 토큰 파일 로드). requires에 추가 필요
  - metadata.md에 `allowed-tools`가 없음 (SKILL.md에만 있음)

---

## 3. figma-to-code 에이전트 ⭐⭐⭐⭐

**강점:**
- Phase 1~5의 단계가 명확하고, devops-pipeline과의 통합이 잘 설계됨
- `requires:` 필드를 동적으로 읽어 실행 순서를 결정하는 설계가 유연 (하드코딩 의존 X)
- 프레임워크별 코드 생성 예시가 구체적

**약점:**
- `model: opus`로 설정 — 비용이 높음. Phase 2(분석)는 개별 스킬이 sonnet/haiku로 처리하므로, 에이전트 자체는 sonnet으로 충분할 수 있음
- CLAUDE.md에 언급된 `figma-project-context`와 `figma-component-inventory` 스킬이 실제로 존재하지 않음 (category CLAUDE.md에 있지만 구현 안 됨)
- `figma-designer` 에이전트도 category에 언급되지만 실제 파일 없음

---

## 4. 발견된 문제점 (버그/불일치)

| # | 심각도 | 내용 |
|---|--------|------|
| 1 | 🔴 HIGH | `figma-project-context` 스킬이 category CLAUDE.md에 "최초 실행 필수"로 명시되어 있지만 **실제 구현이 없음**. 워크플로우 흐름도의 [1]번 단계가 동작 불가 |
| 2 | 🔴 HIGH | `figma-component-inventory` 스킬도 CLAUDE.md 스킬 일람에 있지만 **구현 없음** |
| 3 | 🔴 HIGH | `figma-designer` 에이전트도 CLAUDE.md에 있지만 **파일 없음** |
| 4 | 🟡 MED | `figma-code-sync`의 `requires:`에 `figma-design-token-extractor` 누락 |
| 5 | 🟡 MED | `figma-code-sync` metadata.md에 `allowed-tools` 누락 |
| 6 | 🟢 LOW | `figma-design-analyzer`의 resources/blueprint-template.md와 SKILL.md 본문 중복 |
| 7 | 🟢 LOW | `figma-responsive-validator`가 haiku 모델 — 정확도 검증 필요 |

---

## 5. 개선 제안

### 즉시 수정 (Quick Wins)
1. **`figma-code-sync` requires 수정** — `[figma-framework-figma-mapper, figma-design-token-extractor]`로 변경
2. **`figma-code-sync` metadata.md에 allowed-tools 추가** — `Read, Grep, Glob`
3. **category CLAUDE.md에서 미구현 스킬 표시** — `figma-project-context`, `figma-component-inventory`에 `(TODO — 미구현)` 명시하거나, 구현 필요

### 중기 개선
4. **`figma-project-context` 스킬 구현** — 프로젝트 구조/프레임워크/규약을 `context.md`로 생성하는 스킬. 다른 스킬들이 이걸 참조하게 설계되어 있으므로 있으면 좋음
5. **Dark mode 토큰 지원** — `figma-design-token-extractor`에 Figma Variables mode 처리 추가
6. **`figma-responsive-validator` 모델 업그레이드 검토** — haiku → sonnet, 또는 정확도 비교 eval 수행

### 장기 개선
7. **`figma-component-inventory` 스킬 구현** — 대규모 Figma 파일의 컴포넌트 카탈로그화
8. **CSS-in-JS 지원** — responsive-validator와 code-sync에 styled-components/emotion 패턴 추가
9. **Eval 테스트 세트 구축** — 각 스킬의 출력 품질을 정량적으로 측정할 수 있는 테스트 케이스

---

## 6. 요약 스코어카드

| 평가 항목 | 점수 | 코멘트 |
|-----------|------|--------|
| 아키텍처 설계 | ⭐⭐⭐⭐⭐ | 의존성 체인, 파이프라인 구조 우수 |
| 스킬 품질 (평균) | ⭐⭐⭐⭐ | 개별 스킬 완성도 높음 |
| 문서 정합성 | ⭐⭐⭐ | category CLAUDE.md와 실제 구현 사이 괴리 |
| 실전 준비도 | ⭐⭐⭐ | 미구현 스킬 3개 해결 필요 |
| 확장성 | ⭐⭐⭐⭐⭐ | 커스텀 프레임워크 지원, 팀 설정 유연 |

**종합: 4.0 / 5.0** — 설계 철학이 훌륭하고 구현된 부분의 품질도 높지만, 문서에 명시된 3개 에셋(figma-project-context, figma-component-inventory, figma-designer)이 미구현인 점이 가장 큰 갭.

---

*Reviewed: 2026-03-01 | Reviewer: Claude*
