---
name: figma-framework-figma-mapper
version: v1.0
description: Maps UI framework components to Figma design components. Supports PrimeFaces as a preset (with Figma UI Kit). Also supports custom frameworks via name + documentation URL. Uses Figma MCP to read design files and generates a component mapping table linking framework components to their Figma counterparts with confidence scores. Triggers on requests like "맵핑", "컴포넌트 맵핑", "map components", "framework mapping".
tags: [figma, framework, component, mapping, ui-kit]
requires: [figma-design-token-extractor]
allowed-tools: Read, Write, Glob, WebFetch, mcp__figma__get_file, mcp__figma__get_components
---

# Figma Framework-Figma Mapper — フレームワーク・Figmaコンポーネントマッピング

フレームワークコンポーネントとFigmaデザインコンポーネントの対応表を生成する。
コードとデザインの橋渡しをする中核スキル。

---

## Trigger Conditions

- User says "맵핑", "컴포넌트 맵핑", "map components", "framework mapping"
- Starting a Figma-to-code or code-to-Figma workflow
- An agent needs to know which framework component corresponds to a Figma element

---

## Presets

### PrimeFaces (Built-in Preset)

PrimeFaces has an official Figma UI Kit — high-accuracy direct mapping available.

| Category | Components |
|----------|------------|
| Form | InputText, InputTextarea, InputNumber, Password, Dropdown, MultiSelect, AutoComplete, Calendar, Checkbox, RadioButton, ToggleButton, SelectButton, Slider, Rating, ColorPicker, Chips |
| Data | DataTable, DataView, DataScroller, TreeTable, Tree, OrderList, PickList, Paginator, Timeline |
| Panel | Panel, Accordion, TabView, Fieldset, Card, Toolbar, ScrollPanel, Splitter |
| Overlay | Dialog, ConfirmDialog, Sidebar, OverlayPanel, Tooltip |
| Menu | Menu, Menubar, MegaMenu, TieredMenu, ContextMenu, Breadcrumb, Steps, TabMenu |
| Button | Button, SplitButton, SpeedDial |
| Message | Messages, Toast, InlineMessage |
| Media | Image, Galleria, Carousel, Avatar, Badge, Tag, Chip |
| Misc | ProgressBar, ProgressSpinner, BlockUI, ScrollTop |

### Custom Framework Support

User provides:
- Framework name (e.g., "Material UI", "Ant Design", "shadcn/ui", "Vuetify")
- Documentation URL
- Figma file/page information

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Framework | Yes | "PrimeFaces" (preset) or custom name + doc URL |
| Figma file URL | Yes | Figma file key or URL |
| Figma page | No | Specific page to scan (default: all pages) |
| context.md | No | Output from figma-project-context |

---

## Step 1 — Identify Framework Components

```
IF preset == "PrimeFaces":
  → Load built-in component list (see preset table above)
  → Include each component's available props and variants

ELSE (custom framework):
  1. Fetch documentation from provided URL (WebFetch)
  2. Extract component list from docs navigation/sidebar
  3. For each component: name, props, variants, categories
  4. Build a component catalog
```

---

## Step 2 — Scan Figma Design Components

```
Using Figma MCP:
1. Open the specified Figma file
2. Navigate to target page (or scan all pages)
3. List all Components and Component Sets
4. For each component:
   - Component name and parent set name
   - Variants and properties (size, state, type, etc.)
   - Visual characteristics (dimensions, colors used, structure)
   - Description (if documented in Figma)
5. Build a Figma component catalog
```

---

## Step 3 — Perform Component Matching

For each Figma component, calculate a match score against framework components:

```
Scoring weights:
- Name similarity (40%):
  Exact match "Button" ↔ "Button" → 100%
  Partial match "DataTable" ↔ "Table" → 70%
  Fuzzy match "InputText" ↔ "Text Field" → 50%

- Structure similarity (30%):
  Compare child layers, variant properties, hierarchy depth

- Purpose/category similarity (30%):
  Form input vs form input, data display vs data display

Thresholds:
- confidence ≥ 80% → MAPPED (high confidence)
- 60% ≤ confidence < 80% → MAPPED (medium confidence)
- 40% ≤ confidence < 60% → NEEDS REVIEW
- confidence < 40% → UNMAPPED
```

---

## Step 4 — Generate Mapping Table

```markdown
# Component Mapping: {Framework} ↔ Figma

Generated: {date} | Framework: {name} | Figma file: {file}

## ✅ Mapped Components ({count}/{total})

| Figma Component | Framework Component | Confidence | Variants Mapped | Notes |
|-----------------|---------------------|------------|-----------------|-------|
| Button/Primary | Button (variant="primary") | 95% | primary, secondary, outlined, text | Direct match |
| Input Field | InputText | 92% | default, error, disabled | — |
| Data Table | DataTable | 90% | striped, paginated, sortable | Includes sorting/filtering |
| Dropdown | Dropdown / Select | 88% | single, multi | Use Dropdown for single |
| Modal | Dialog | 85% | default, fullscreen | — |
| Card | Card | 82% | default, with-header, with-footer | — |
| Tabs | TabView | 80% | top, scrollable | — |
| Date Picker | Calendar | 78% | inline, popup, range | — |
| Sidebar | Sidebar | 75% | left, right, bottom | — |
| Toast | Toast | 90% | success, error, warn, info | — |

## ⚠️ Needs Review ({count})

| Figma Component | Possible Match | Confidence | Issue |
|-----------------|----------------|------------|-------|
| Info Panel | Panel or Fieldset | 55% | Both could apply |
| Status Badge | Badge or Tag | 52% | Visual ambiguity |
| Toggle Switch | ToggleButton or InputSwitch | 48% | Need to check design intent |

## ❌ Unmapped ({count})

### Figma components with no framework equivalent (need custom implementation)
| Figma Component | Category | Suggestion |
|-----------------|----------|------------|
| Custom Chart Widget | Data | Use Chart.js / ECharts with wrapper |
| Activity Timeline | Data | Build custom component |

### Framework components with no Figma design (available but not designed)
| Framework Component | Category |
|--------------------|----------|
| DataScroller | Data |
| Terminal | Misc |

## 📊 Coverage Summary
- Figma components: {total}
- Mapped: {mapped} ({mappedPct}%)
- Needs review: {review}
- Unmapped: {unmapped}
```

---

## Step 5 — Save Output

```
Save mapping table as:
- figma-mapping.md (markdown, for human review)
- figma-mapping.json (JSON, for agent consumption)

JSON format:
{
  "framework": "PrimeFaces",
  "generatedAt": "2026-02-21",
  "mappings": [
    {
      "figmaComponent": "Button/Primary",
      "frameworkComponent": "Button",
      "confidence": 95,
      "variants": { "primary": "severity=null", "secondary": "severity=secondary" },
      "status": "mapped"
    }
  ]
}
```

---

*Skill: figma-framework-figma-mapper | Category: figma | Version: v1.0 | Last updated: 2026-02-21*
