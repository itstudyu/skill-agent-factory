---
name: figma-design-analyzer
version: v1.0
description: Analyzes Figma designs to produce a frontend implementation blueprint before coding begins. Captures screenshots of each screen/section, breaks down the page structure, recommends specific framework components for each UI element, and generates a detailed implementation plan with build order. Bridges the gap between design and code. Triggers on requests like "디자인 분석", "구현 계획", "analyze design", "implementation plan", "어떻게 만들어?".
tags: [figma, design, analyze, blueprint, frontend, planning]
requires: [figma-design-token-extractor, figma-framework-figma-mapper]
allowed-tools: Read, Write, Glob, mcp__figma__get_file, mcp__figma__get_node, mcp__figma__export_node
---

# Figma Design Analyzer — デザイン分析・実装Blueprint生成

コーディング前にFigmaデザインを分析し、実装Blueprint（設計書）を生成する。
「デザインを見る」から「コードを書く」への橋渡しをする計画スキル。

---

## Trigger Conditions

- User says "디자인 분석", "구현 계획", "analyze design", "implementation plan"
- User asks "이 디자인 어떻게 만들어?", "어떤 컴포넌트 써야해?"
- figma-to-code agent needs a structured breakdown before code generation

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Figma file URL or key | Yes | The Figma file to analyze |
| Figma page / frame | No | Specific page or frame (default: ask user) |
| Target framework | No | Framework for recommendations (default: detect from context.md) |
| figma-mapping.md | No | Output from figma-framework-figma-mapper |
| context.md | No | Output from figma-project-context |

---

## Output

- `implementation-blueprint.md` — Full implementation plan
- `screenshots/` — Captured screenshots of each screen and section
- Component recommendation table
- Page structure breakdown with ASCII diagram
- Implementation priority and build order

---

## Phase 1 — Visual Capture

### Step 1.1: List Screens

```
Using Figma MCP:
1. Open the Figma file
2. Navigate to the target page
3. List all top-level frames → these are typically screens/pages
4. Present list to agent for selection (or process all)
```

### Step 1.2: Full-Page Screenshots

```
For each top-level frame (screen):
1. Export a screenshot at 1x resolution
2. Save as: screenshots/{FrameName}-full.png
3. Record:
   - Frame dimensions (width × height)
   - Frame name
```

### Step 1.3: Section Screenshots

```
Identify major sections within each frame:
- Header / Topbar (navigation, logo, search, user menu)
- Sidebar / Navigation panel
- Hero / Banner
- Content area (cards, tables, forms, charts)
- Footer
- Modals / Overlays (capture if visible)

For each section:
→ Export screenshot: screenshots/{FrameName}-{SectionName}.png
```

### Step 1.4: Component Close-ups

```
For elements that need special attention:
- Complex custom components
- Interactive elements (dropdown menus, date pickers, modals)
- Tables with specific column configurations
- Elements with multiple states (hover, active, error, disabled)

→ Save as: screenshots/{FrameName}-{ComponentName}-detail.png
```

---

## Phase 2 — Structure Analysis

### Step 2.1: Layout Detection

```
Analyze the overall page structure:

1. Layout Type:
   ☐ Sidebar + Content area (admin dashboards, portals)
   ☐ Top Nav + Full Width (landing pages, marketing)
   ☐ Header + Multi-Column (e-commerce, media)
   ☐ Single Column (forms, articles, onboarding)
   ☐ Grid Layout (galleries, card views)

2. Grid System:
   - Column count (12 / 16 / 24 column grid)
   - Gutter sizes
   - Page margins (left/right)

3. Build ASCII Page Skeleton:
┌──────────────────────────────────────┐
│              Header (64px)            │
├─────────┬────────────────────────────┤
│         │                            │
│ Sidebar │      Main Content          │
│ (240px) │    ┌──────┐ ┌──────┐      │
│         │    │ Card │ │ Card │      │
│         │    └──────┘ └──────┘      │
│         │                            │
├─────────┴────────────────────────────┤
│              Footer                  │
└──────────────────────────────────────┘
```

### Step 2.2: Section-by-Section Breakdown

For each section, analyze and document:

```json
{
  "section": "Header",
  "screenshot": "screenshots/Dashboard-header.png",
  "dimensions": { "width": "100%", "height": "64px" },
  "layout": "flex, justify-between, align-center",
  "children": [
    { "element": "Logo", "type": "image", "position": "left" },
    { "element": "Search Bar", "type": "input", "position": "center", "width": "320px" },
    { "element": "Notification Bell", "type": "icon-button", "position": "right" },
    { "element": "User Avatar + Menu", "type": "dropdown", "position": "right" }
  ],
  "tokens": {
    "background": "#FFFFFF",
    "borderBottom": "1px solid #E5E7EB",
    "padding": "0 24px",
    "shadow": "0 1px 3px rgba(0,0,0,0.1)"
  }
}
```

---

## Phase 3 — Component Recommendations

### Step 3.1: Map Elements to Framework Components

```
For each UI element:

IF figma-mapping.md exists:
  → Look up the Figma component name in the mapping table
  → Use the mapped framework component

ELSE:
  → Recommend based on visual analysis and framework knowledge

For each element determine:
- Primary component: the main framework component
- Sub-components: supporting pieces needed
- Key props to set
- Custom CSS needed beyond the component
```

### Step 3.2: Component Recommendation Table

| Section | UI Element | Framework Component | Key Props / Config | Custom CSS | Priority |
|---------|-----------|--------------------|--------------------|------------|----------|
| Header | Logo | `<img>` / `<Image>` | src, alt, height=32 | cursor: pointer | High |
| Header | Search | `<InputText>` + icon | placeholder, icon="pi pi-search" | width: 320px | High |
| Header | User Menu | `<Avatar>` + `<Menu>` | image, shape="circle", popup model | — | Medium |
| Sidebar | Navigation | `<PanelMenu>` | model=navItems | active highlight | High |
| Content | Stats | `<Card>` × N | — | custom inner layout | High |
| Content | Data Table | `<DataTable>` | paginator, rows=10, sortable | striped | High |
| Footer | Links | `<a>` tags | href | flex layout | Low |

### Step 3.3: Identify Custom Components

| Element | Description | Implementation Approach | Effort |
|---------|-------------|------------------------|--------|
| KPI Gauge | Circular progress + number | SVG or Chart.js doughnut | Medium |
| Activity Timeline | Vertical timeline with icons | Custom HTML + CSS | Medium |

---

## Phase 4 — Implementation Blueprint

### Step 4.1: Component Hierarchy Tree

```
DashboardPage
├── AppHeader
│   ├── Logo
│   ├── SearchBar (InputText + Button)
│   └── UserMenu (Avatar + Menu)
├── AppSidebar
│   └── NavigationMenu (PanelMenu)
├── MainContent
│   ├── StatsRow
│   │   └── StatCard × 4 (Card + custom inner)
│   ├── DataSection
│   │   ├── SectionHeader (h2 + Button)
│   │   └── UserTable (DataTable)
│   └── ActivitySection
│       └── ActivityTimeline (custom)
└── AppFooter
```

### Step 4.2: Implementation Build Order

| # | Component | Depends On | Estimated Effort |
|---|-----------|-----------|-----------------|
| 1 | Page layout shell (HTML structure) | — | XS |
| 2 | AppHeader | Logo, SearchBar | S |
| 3 | AppSidebar + NavigationMenu | — | S |
| 4 | StatCard (template) | Design tokens | S |
| 5 | StatsRow | StatCard | S |
| 6 | UserTable (DataTable + columns) | DataTable config | M |
| 7 | KPIGauge (custom) | Chart.js setup | M |
| 8 | ActivityTimeline (custom) | — | M |
| 9 | AppFooter | — | XS |
| 10 | Responsive adjustments | All above | M |

### Step 4.3: Responsive Behavior Plan

| Section | Desktop (≥1024px) | Tablet (768-1023px) | Mobile (<768px) |
|---------|-------------------|---------------------|-----------------|
| Sidebar | Fixed 240px | Collapsible overlay | Hidden + hamburger |
| Stats Row | 4 cards in row | 2×2 grid | Single column stack |
| Data Table | Full columns visible | Horizontal scroll | Card view or limited cols |
| Header Search | Visible 320px input | Icon → expand on click | Icon → fullscreen overlay |

---

## Output: Save Blueprint

Save `implementation-blueprint.md` to the project root or a `docs/` folder.

Include all screenshots inline:

```markdown
# Implementation Blueprint: {ScreenName}

## Overview
- Design: {FigmaFrameName}
- Framework: {framework}
- Layout: {layoutType}
- Total components: {total} ({frameworkCount} framework, {customCount} custom)

## Screenshots
| Screen | File |
|--------|------|
| Full page | screenshots/{name}-full.png |
| Header | screenshots/{name}-header.png |
...

## Page Structure
{ASCII diagram}

## Section Breakdown
{per section JSON + screenshot}

## Component Recommendations
{table}

## Custom Components
{table}

## Build Order
{table}

## Responsive Plan
{table}
```

---

*Skill: figma-design-analyzer | Category: figma | Version: v1.0 | Last updated: 2026-02-21*
