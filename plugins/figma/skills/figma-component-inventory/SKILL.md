---
name: figma-component-inventory
version: v1.0
description: Scans and catalogs all components in a Figma file. Produces a comprehensive inventory with variant counts, usage statistics, and gap analysis against the codebase. Useful for large-scale Figma-to-code conversions to understand scope before starting. Triggers on requests like "컴포넌트 목록", "component inventory", "Figma 스캔", "gap analysis", "audit components".
tags: [figma, component, inventory, catalog, scan, audit]
allowed-tools: Read, Write, Glob, Grep, mcp__figma__get_file, mcp__figma__get_components
---

# Figma Component Inventory — コンポーネントカタログ・ギャップ分析

Figmaファイル内の全コンポーネントをスキャン・カタログ化し、コードベースとのギャップ分析を行う。
大規模なFigma→コード変換の前にスコープを把握するためのスキル。

---

## Trigger Conditions

- User says "컴포넌트 목록", "component inventory", "Figma 스캔", "gap analysis"
- Before a large-scale Figma-to-code conversion
- User wants to audit design system coverage
- Figma file was updated and user needs to understand what changed

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Figma file URL or key | Yes | The Figma file to scan |
| Figma page(s) | No | Specific pages to scan (default: all pages) |
| Project root | No | For gap analysis against codebase (default: cwd) |
| context.md | No | Output from figma-project-context |

---

## Step 1 — Scan Figma File

```
Using Figma MCP:
1. Open the specified Figma file
2. List all pages in the file
3. For each page, collect all Component and Component Set nodes
4. Build a raw component list
```

---

## Step 2 — Catalog Each Component

For each component or component set:

```
Extract:
1. Name (and parent component set name if a variant)
2. Description (from Figma description field)
3. Category (infer from naming convention or page location):
   - Form: inputs, selects, checkboxes, radios
   - Data: tables, lists, cards, charts
   - Navigation: menus, tabs, breadcrumbs, sidebars
   - Feedback: modals, toasts, alerts, progress
   - Layout: containers, grids, dividers, spacers
   - Media: images, avatars, icons, badges
   - Action: buttons, links, toggles
4. Variant count and variant properties:
   - e.g., Button: size={sm,md,lg}, variant={primary,secondary,ghost}, state={default,hover,disabled}
5. Instance count (how many times used across the file)
6. Dimensions (width × height of default variant)
7. Auto Layout (yes/no, direction, gap, padding)
8. Design token usage:
   - Fill colors → map to token names if possible
   - Text styles → map to typography tokens
```

---

## Step 3 — Build Category Summary

```
Group components by category and summarize:

| Category | Component Count | Variant Count | Instance Count |
|----------|----------------|---------------|----------------|
| Form | {n} | {n} | {n} |
| Data | {n} | {n} | {n} |
| Navigation | {n} | {n} | {n} |
| Feedback | {n} | {n} | {n} |
| Layout | {n} | {n} | {n} |
| Media | {n} | {n} | {n} |
| Action | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** |
```

---

## Step 4 — Gap Analysis (if project root provided)

```
Compare Figma components against codebase:

1. Scan codebase for implemented components:
   - Glob: src/components/**/*.{tsx,vue,jsx,svelte,xhtml}
   - Extract component names from filenames and exports

2. For each Figma component:
   - Search codebase for matching component (by name similarity)
   - Check if all variants are implemented
   - Mark status: ✅ Implemented | ⚠️ Partial | ❌ Missing

3. For each code component:
   - Check if it has a Figma counterpart
   - Mark: ✅ Designed | ❌ No Figma Design (code-only)
```

---

## Step 5 — Identify Issues

```
Flag potential problems:

1. Unused components (0 instances in Figma → may be deprecated)
2. Inconsistent naming (e.g., "Btn" vs "Button", "Dlg" vs "Dialog")
3. Missing variants (e.g., Button has no disabled state)
4. Orphan components (not part of any component set)
5. Deep nesting (component contains 5+ levels of nested components)
6. Duplicate components (same visual, different names)
```

---

## Step 6 — Generate Inventory Report

Save as `component-inventory.md` (and optionally `component-inventory.json`).

```markdown
# Component Inventory: {Figma File Name}

> Generated: {date} | Pages scanned: {pageList} | Total components: {total}

## Summary

| Metric | Count |
|--------|-------|
| Component Sets | {n} |
| Total Components (incl. variants) | {n} |
| Total Instances | {n} |
| Categories | {n} |

## Category Breakdown

{category summary table from Step 3}

## Full Component Catalog

### Form Components

| Component | Variants | Instances | Auto Layout | Dimensions | Status |
|-----------|----------|-----------|-------------|------------|--------|
| InputText | 3 (default, error, disabled) | 42 | ✅ Horizontal | 240×40 | ✅ Implemented |
| Dropdown | 2 (default, open) | 18 | ✅ Vertical | 240×40 | ✅ Implemented |
| Checkbox | 2 (checked, unchecked) | 31 | ❌ | 20×20 | ⚠️ Partial |

### Data Components
{...}

### Navigation Components
{...}

{...repeat for all categories}

## Gap Analysis

### Figma → Code Coverage

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Fully Implemented | {n} | {pct}% |
| ⚠️ Partially Implemented | {n} | {pct}% |
| ❌ Not Implemented | {n} | {pct}% |

### Missing from Code (need implementation)

| Figma Component | Category | Variants | Priority |
|-----------------|----------|----------|----------|
| {name} | {category} | {count} | {High/Medium/Low} |

### Code-Only (no Figma design)

| Code Component | File | Suggestion |
|----------------|------|------------|
| {name} | {path} | {Add to Figma / Deprecated?} |

## Issues Found

| # | Severity | Issue | Component | Action |
|---|----------|-------|-----------|--------|
| 1 | ⚠️ WARN | Inconsistent naming | Btn vs Button | Standardize to "Button" |
| 2 | ℹ️ INFO | Unused component (0 instances) | LegacyCard | Consider removing |

## Implementation Effort Estimate

| Category | Components to Build | Estimated Effort |
|----------|--------------------|-----------------|
| High priority (core UI) | {n} | {hours}h |
| Medium priority (secondary) | {n} | {hours}h |
| Low priority (nice to have) | {n} | {hours}h |
| **Total** | **{n}** | **{hours}h** |
```

---

## JSON Output (for agent consumption)

Save as `component-inventory.json`:

```json
{
  "generatedAt": "{date}",
  "figmaFile": "{fileKey}",
  "summary": {
    "componentSets": 0,
    "totalComponents": 0,
    "totalInstances": 0
  },
  "components": [
    {
      "name": "Button",
      "category": "Action",
      "variants": ["primary", "secondary", "ghost", "disabled"],
      "instanceCount": 87,
      "dimensions": { "width": 120, "height": 40 },
      "autoLayout": true,
      "codeStatus": "implemented",
      "codePath": "src/components/Button.tsx"
    }
  ],
  "gaps": {
    "missingFromCode": [],
    "missingFromFigma": [],
    "partialImplementation": []
  }
}
```

---

## Output Summary

```
## ✅ figma-component-inventory 完了

| 項目 | 結果 |
|------|------|
| Scanned pages | {pageList} |
| Component sets | {n} |
| Total components | {n} |
| Total instances | {n} |

### Gap Analysis
| Status | Count |
|--------|-------|
| ✅ Implemented | {n} ({pct}%) |
| ⚠️ Partial | {n} ({pct}%) |
| ❌ Missing | {n} ({pct}%) |

生成ファイル:
- component-inventory.md ✅
- component-inventory.json ✅
```

---

*Skill: figma-component-inventory | Category: figma | Version: v1.0 | Last updated: 2026-03-01*
