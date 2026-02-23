---
name: figma-responsive-validator
version: v1.0
description: Validates responsive design compliance of frontend code across Mobile, Tablet, and Desktop breakpoints. Performs static code analysis to detect layout issues, overflow risks, typography problems, and navigation gaps. Generates detailed reports with auto-fix code suggestions. Used by figma-to-code agent in a validate-fix loop until all breakpoints pass. Triggers on requests like "반응형 검증", "check responsive", "breakpoint validation", "모바일 확인".
tags: [figma, responsive, validate, mobile, layout, breakpoint]
allowed-tools: Read, Grep, Glob
---

# Figma Responsive Validator — レスポンシブデザイン検証・自動修正提案

生成されたフロントエンドコードのレスポンシブ対応を全ブレークポイントで検証する。
問題を検出し、修正コードを提案するスキル。

---

## Trigger Conditions

- User says "반응형 검증", "check responsive", "breakpoint validation", "모바일 확인"
- After frontend code is generated (used by figma-to-code agent automatically)
- User wants to verify existing code for responsive issues

---

## Breakpoint Definitions

| Name | Alias | Width Range | Representative Devices |
|------|-------|-------------|----------------------|
| xs | Mobile S | 320px – 374px | iPhone SE |
| sm | Mobile | 375px – 767px | iPhone 12/13/14, Galaxy S |
| md | Tablet | 768px – 1023px | iPad, Galaxy Tab |
| lg | Desktop | 1024px – 1279px | MacBook 13", small laptops |
| xl | Desktop L | 1280px – 1535px | MacBook 16", standard monitors |
| 2xl | Desktop XL | 1536px+ | Large monitors, 4K |

**Minimum required:** sm (Mobile), md (Tablet), lg (Desktop)

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Frontend code files | Yes | HTML/CSS/JS, React (TSX), Vue (SFC), Angular, PrimeFaces (XHTML) |
| Target breakpoints | No | Specific breakpoints (default: sm, md, lg) |
| Figma design reference | No | For visual comparison if available |

---

## Step 1 — Parse Code Structure

```
1. Detect technology stack from file extensions:
   - .html / .css → Plain HTML/CSS
   - .tsx / .jsx → React
   - .vue → Vue SFC
   - .component.ts + .html → Angular
   - .xhtml → PrimeFaces / JSF

2. Detect CSS framework from class names or imports:
   - Tailwind: className="flex justify-between" etc.
   - Bootstrap: class="row col-md-6" etc.
   - PrimeFlex: class="col-12 md:col-6" etc.
   - Custom CSS: look for media queries in .css/.scss files

3. Extract all layout-related code:
   - CSS Grid definitions
   - Flexbox rules
   - Media queries (@media)
   - Responsive utility classes
   - Fixed px dimensions
   - Viewport-relative units (vw, vh, %)
```

---

## Step 2 — Static Analysis per Breakpoint

Run all 7 checks for each breakpoint:

### Check 1: Overflow

```
⚠️ Look for:
- Elements with fixed width > viewport width
  Pattern: width: [6-9][0-9][0-9]px | width: [0-9]{4}px
- Images without max-width: 100%
  Pattern: <img without max-width
- Tables without overflow handling
  Pattern: <table without overflow-x: auto

🔍 Grep patterns:
  width:\s*[6-9]\d{2,}px
  <img[^>]+(?!max-width)
```

### Check 2: Layout

```
⚠️ Look for:
- Multi-column layouts that don't stack on mobile
  Tailwind: grid-cols-{2,3,4,5,6} without sm:/md: prefix
  Bootstrap: col-{sm,md,lg}- prefix missing for mobile
  CSS: grid-template-columns with fixed values, no @media fallback
- Sidebar without mobile collapse
  Pattern: sidebar or aside with fixed width, no @media hide/overlay

🔍 Grep patterns:
  grid-cols-[2-9](?!\s+(?:sm|md|lg):)
  position:\s*fixed.*width:\s*\d+px
```

### Check 3: Typography

```
⚠️ Look for:
- Font sizes < 12px (too small for mobile)
  Pattern: font-size:\s*([0-9]|1[01])px
- Fixed font-size without responsive scaling
  Pattern: font-size:\s*\d+px (without rem or responsive class)
- Line length > 75ch on mobile
  Pattern: max-width not set on text containers

🔍 Grep patterns:
  font-size:\s*([0-9]|1[01])px
  text-(xs|sm|base)(?!\s+(?:sm|md|lg):)
```

### Check 4: Spacing

```
⚠️ Look for:
- Padding/margin values too large for mobile (> 48px fixed)
  Pattern: padding:\s*[5-9][0-9]px | margin:\s*[5-9][0-9]px
- Touch targets < 44px
  Pattern: height:\s*(1[0-9]|2[0-9]|3[0-9]|4[0-3])px on interactive elements

🔍 Grep patterns:
  padding:\s*[5-9]\d+px
  height:\s*[1-3]\dpx.*button|button.*height:\s*[1-3]\dpx
```

### Check 5: Navigation

```
⚠️ Look for:
- Desktop nav without mobile hamburger menu
  Pattern: <nav or <ul.nav without mobile toggle button
- Horizontal menu that overflows on mobile
  Pattern: <ul with display:flex without flex-wrap or mobile hide

🔍 Grep patterns:
  <nav(?![^>]*hamburger|[^>]*mobile|[^>]*toggle)
  flex.*overflow.*hidden(?!.*@media)
```

### Check 6: Media

```
⚠️ Look for:
- Images without responsive sizing
  Pattern: <img without width="100%" or max-width: 100%
- Videos without aspect ratio
  Pattern: <video or <iframe without aspect-ratio or padding-bottom trick
- Missing srcset for responsive images

🔍 Grep patterns:
  <img(?![^>]*responsive|[^>]*w-full|[^>]*max-w)
  <video(?![^>]*aspect)
```

### Check 7: Touch / Interaction

```
⚠️ Look for:
- Hover-only interactions without touch fallback
  Pattern: :hover without corresponding :active or :focus
- Click targets too close together (< 8px gap)
  Pattern: gap:\s*[1-7]px on button containers
- Missing pointer: cursor for touch

🔍 Grep patterns:
  :hover(?!.*:active|.*:focus)
  gap:\s*[1-7]px.*button|button.*gap:\s*[1-7]px
```

---

## Step 3 — Generate Validation Report

```markdown
# Responsive Validation Report

> Validated: {date} | Files: {fileList}

## Summary
| Metric | Count |
|--------|-------|
| Total issues | {total} |
| 🔴 Critical (must fix) | {critical} |
| 🟡 Warning (should fix) | {warning} |
| 🔵 Info (nice to fix) | {info} |

## Breakpoint Status
| Breakpoint | Status | Critical | Warning | Info |
|------------|--------|----------|---------|------|
| Mobile sm (375px) | ❌ FAIL | 2 | 1 | 0 |
| Tablet md (768px) | ⚠️ WARN | 0 | 2 | 1 |
| Desktop lg (1024px) | ✅ PASS | 0 | 0 | 1 |

---

## 🔴 Critical Issues

### 1. Data table overflows on mobile
- **Breakpoint:** sm (375px) | **Category:** overflow
- **File:** src/components/UserTable.tsx | **Line:** 24
- **Issue:** DataTable has a fixed width of 900px — causes horizontal scroll on mobile

**Current code:**
```css
.user-table { width: 900px; }
```

**Fix:**
```css
.user-table {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
```

---

### 2. Navigation does not collapse on mobile
- **Breakpoint:** sm (375px) | **Category:** navigation
- **File:** src/components/AppHeader.tsx | **Line:** 8
- **Issue:** `<nav>` renders full horizontal bar, overflows viewport on mobile

**Fix (Tailwind):**
```tsx
{/* ハンバーガーボタン — モバイルのみ表示 */}
<button className="md:hidden p-2" onClick={() => setMenuOpen(!menuOpen)}>
  <span>☰</span>
</button>

{/* ナビゲーション — PC: flex, モバイル: 折りたたみ */}
<nav className={`${menuOpen ? 'flex' : 'hidden'} md:flex flex-col md:flex-row`}>
  {/* nav items */}
</nav>
```

---

## 🟡 Warnings

### 3. Grid does not stack on mobile
- **Breakpoint:** sm (375px) | **Category:** layout
- **File:** src/components/StatsRow.tsx | **Line:** 5
- **Issue:** `grid-cols-4` renders 4 columns on all screens

**Fix (Tailwind):**
```diff
- <div className="grid grid-cols-4 gap-4">
+ <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
```

---

## 🔵 Info

### 4. Consider responsive images
- **File:** src/components/HeroBanner.tsx
- **Suggestion:** Add `srcset` for better performance on mobile (not critical)

---

## Overall Verdict

**❌ FAIL** — 2 critical issues must be resolved before release.

Fix critical issues → re-run this skill → verify all breakpoints PASS.
```

---

## Repeat Loop Protocol

```
This skill reports issues and suggests fixes.
The calling agent (figma-to-code) applies fixes and re-runs this skill.

Max iterations: 3 loops before escalating to user.

Loop logic:
1. Run validation → generate report
2. If FAIL → apply fix suggestions → go to 1
3. If PASS → exit loop ✅
4. If 3 iterations and still FAIL → report to user with remaining issues
```

---

## Validation Score

| Score | Status | Meaning |
|-------|--------|---------|
| 0 critical + 0 warning | ✅ PASS | Ready for release |
| 0 critical + 1+ warning | ⚠️ WARN | Acceptable for MVP, fix before release |
| 1+ critical | ❌ FAIL | Must fix before any deployment |

---

*Skill: figma-responsive-validator | Category: figma | Version: v1.0 | Last updated: 2026-02-21*
