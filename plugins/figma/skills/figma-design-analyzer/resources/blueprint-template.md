# Implementation Blueprint: {ScreenName}

> Load this template when producing the final design analysis output.
> Reference in SKILL.md: `Read: plugins/figma/skills/figma-design-analyzer/resources/blueprint-template.md`
> Fill each `{placeholder}` with data collected in Phases 1–4 of the analyzer skill.

---

## Overview

| Item | Value |
|------|-------|
| Design | {FigmaFrameName} |
| Framework | {framework} |
| Layout Type | {layoutType} |
| Total Components | {total} ({frameworkCount} framework, {customCount} custom) |
| Generated | {date} |

---

## Screenshots

| Screen | File |
|--------|------|
| Full page | screenshots/{name}-full.png |
| Header | screenshots/{name}-header.png |
| Sidebar | screenshots/{name}-sidebar.png |
| Content | screenshots/{name}-content.png |
| Footer | screenshots/{name}-footer.png |

> Add or remove rows based on actual sections detected.

---

## Page Structure

```
{ASCII diagram from Phase 2, Step 2.1}

Example:
┌──────────────────────────────────────┐
│              Header (64px)            │
├─────────┬────────────────────────────┤
│         │                            │
│ Sidebar │      Main Content          │
│ (240px) │                            │
│         │                            │
├─────────┴────────────────────────────┤
│              Footer                  │
└──────────────────────────────────────┘
```

---

## Section Breakdown

> Repeat this block for each section (Header, Sidebar, Content, Footer, etc.)

### {SectionName}

| Property | Value |
|----------|-------|
| Screenshot | screenshots/{name}-{section}.png |
| Dimensions | {width} × {height} |
| Layout | {flex/grid, direction, alignment} |

**Children:**

| Element | Type | Position | Key Props |
|---------|------|----------|-----------|
| {element} | {type} | {position} | {props} |

**Tokens Used:**

| Token Category | Value |
|----------------|-------|
| Background | {token reference} |
| Border | {token reference} |
| Padding | {token reference} |
| Shadow | {token reference} |

---

## Component Recommendations

| Section | UI Element | Framework Component | Key Props / Config | Custom CSS | Priority |
|---------|-----------|--------------------|--------------------|------------|----------|
| {section} | {element} | {component} | {props} | {css} | {High/Med/Low} |

---

## Custom Components (no framework equivalent)

| Element | Description | Implementation Approach | Effort |
|---------|-------------|------------------------|--------|
| {element} | {description} | {approach} | {XS/S/M/L/XL} |

---

## Component Hierarchy

```
{PageComponent}
├── {HeaderComponent}
│   ├── {Child}
│   └── {Child}
├── {SidebarComponent}
│   └── {Child}
├── {MainContentComponent}
│   ├── {SectionA}
│   │   └── {Child}
│   └── {SectionB}
│       └── {Child}
└── {FooterComponent}
```

---

## Build Order

| # | Component | Depends On | Estimated Effort |
|---|-----------|-----------|-----------------|
| 1 | Page layout shell | — | XS |
| 2 | {component} | {deps} | {effort} |

---

## Responsive Behavior Plan

| Section | Desktop (≥1024px) | Tablet (768–1023px) | Mobile (<768px) |
|---------|-------------------|---------------------|-----------------|
| {section} | {behavior} | {behavior} | {behavior} |

---

## Design Tokens Referenced

| Token | Value | Usage |
|-------|-------|-------|
| --color-primary-500 | {value} | {where used} |
| --font-size-base | {value} | {where used} |
| --spacing-4 | {value} | {where used} |
