---
name: figma-design-token-extractor
version: v1.0
description: Extracts design tokens (colors, fonts, spacing, shadows, border-radius, etc.) from Figma files via Figma MCP and converts them into code-ready variable formats — CSS custom properties, SCSS variables, Tailwind config, and JSON tokens (W3C format). Synchronizes Figma design system with project code. Triggers on requests like "토큰 추출", "디자인 토큰", "extract tokens", "design tokens", "Figma styles".
tags: [figma, design-token, colors, typography, css, extract]
allowed-tools: Read, Write, Glob, mcp__figma__get_file, mcp__figma__get_styles
---

# Figma Design Token Extractor — デザイントークン抽出・コード変換

Figmaからデザイントークンを抽出し、コードで使えるフォーマットに変換する。
デザインとコードの唯一の真実の情報源(Single Source of Truth)を確立する。

---

## Trigger Conditions

- User says "토큰 추출", "디자인 토큰", "extract tokens", "design tokens", "Figma styles to code"
- Starting a new project's design system from Figma
- Figma design was updated and tokens need refreshing
- An agent needs design tokens before code generation

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Figma file URL or key | Yes | The Figma file to extract tokens from |
| Figma page name | No | Page with design tokens (default: scan all pages) |
| Output format | No | css, scss, tailwind, json — default: all |
| Project context | No | context.md from figma-project-context |

---

## Token Categories

| Category | What is Extracted |
|----------|------------------|
| Color | Primary, secondary, accent, neutral, semantic (success/error/warning/info), surface, background |
| Typography | Font family, font size scale, font weight, line height, letter spacing |
| Spacing | Spacing scale (4px base grid) |
| Border Radius | Corner radius scale |
| Shadow | Box shadow elevation levels (sm, md, lg, xl) |
| Opacity | Opacity scale |
| Breakpoints | Responsive breakpoints (from Figma variants if available) |
| Z-Index | Layer ordering scale |

---

## Step 1 — Connect to Figma File

```
Using Figma MCP:
1. Open the specified Figma file
2. Navigate to the design tokens page (look for pages named "Design System", "Tokens", "Styles", "Variables")
3. If no dedicated token page → scan all pages for Figma Styles and Variables
```

---

## Step 2 — Extract Color Tokens

```
From Figma:
1. Read all Color Styles (Fill styles panel)
2. Read all Color Variables (if using Figma Variables beta)
3. For each color:
   - Name (e.g., "Primary/500", "Neutral/100")
   - HEX value
   - RGB/RGBA values
   - Opacity (if < 100%)
4. Organize by category:
   - Brand colors: primary, secondary, accent
   - Neutral: gray scale (50 → 950)
   - Semantic: success, error, warning, info (each: light, default, dark)
   - Surface: background, card, overlay, input
```

---

## Step 3 — Extract Typography Tokens

```
From Figma Text Styles:
1. For each text style:
   - Name (e.g., "Heading/H1", "Body/Regular", "Caption/Default")
   - Font family
   - Font size (px → converted to rem)
   - Font weight (numeric: 400, 500, 600, 700)
   - Line height (px or %)
   - Letter spacing (px → converted to em)
2. Build a type scale with semantic names (xs, sm, base, lg, xl, 2xl, 3xl, 4xl)
```

---

## Step 4 — Extract Spacing & Other Tokens

```
Spacing:
- Read Figma Variables spacing values (if available)
- If none → detect common padding/margin/gap values from components
- Standard scale: 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64 (× 4px base)

Border Radius:
- Scan component cornerRadius values
- Build scale: none(0), sm(2px), md(4px), lg(8px), xl(12px), 2xl(16px), full(9999px)

Shadows:
- Read Effect Styles (Drop Shadow, Inner Shadow)
- Map to elevation: sm, md, lg, xl, 2xl
- Extract: x-offset, y-offset, blur, spread, color

Opacity:
- Default scale: 0, 5, 10, 20, 25, 50, 75, 90, 95, 100 (as %)
```

---

## Step 5 — Generate Output Files

### CSS Custom Properties (`tokens.css`)
```css
:root {
  /* === Colors === */
  --color-primary-50: #EFF6FF;
  --color-primary-100: #DBEAFE;
  --color-primary-500: #3B82F6;
  --color-primary-900: #1E3A8A;

  --color-success: #10B981;
  --color-error: #EF4444;
  --color-warning: #F59E0B;
  --color-info: #3B82F6;

  /* === Typography === */
  --font-family-base: 'Inter', system-ui, sans-serif;
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */

  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* === Spacing === */
  --spacing-1: 0.25rem;   /* 4px */
  --spacing-2: 0.5rem;    /* 8px */
  --spacing-4: 1rem;      /* 16px */
  --spacing-6: 1.5rem;    /* 24px */
  --spacing-8: 2rem;      /* 32px */

  /* === Border Radius === */
  --radius-sm: 0.125rem;  /* 2px */
  --radius-md: 0.25rem;   /* 4px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-full: 9999px;

  /* === Shadows === */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
```

### SCSS Variables (`_tokens.scss`)
```scss
// === Colors ===
$color-primary-500: #3B82F6;
$color-success: #10B981;
$color-error: #EF4444;

// Color maps for iteration
$colors: (
  'primary-50': #EFF6FF,
  'primary-500': #3B82F6,
  'primary-900': #1E3A8A,
);

// === Typography ===
$font-family-base: 'Inter', system-ui, sans-serif;
$font-size-base: 1rem;
$font-weight-medium: 500;

// === Spacing ===
$spacing-unit: 0.25rem; // 4px base
```

### Tailwind Config Extension (`tailwind.tokens.js`)
```javascript
// tailwind.tokens.js — Figmaから自動生成 (figma-design-token-extractor)
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          500: '#3B82F6',
          900: '#1E3A8A',
        },
        success: '#10B981',
        error: '#EF4444',
        warning: '#F59E0B',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
      },
      boxShadow: {
        sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      },
    },
  },
};
```

### JSON Tokens — W3C Design Token Format (`tokens.json`)
```json
{
  "color": {
    "primary": {
      "50": { "$value": "#EFF6FF", "$type": "color" },
      "500": { "$value": "#3B82F6", "$type": "color" },
      "900": { "$value": "#1E3A8A", "$type": "color" }
    },
    "success": { "$value": "#10B981", "$type": "color" },
    "error": { "$value": "#EF4444", "$type": "color" }
  },
  "fontSize": {
    "base": { "$value": "1rem", "$type": "dimension" },
    "lg": { "$value": "1.125rem", "$type": "dimension" }
  },
  "spacing": {
    "4": { "$value": "1rem", "$type": "dimension" },
    "8": { "$value": "2rem", "$type": "dimension" }
  }
}
```

---

## Step 6 — Save Files

```
Save to project root (or tokens/ directory if it exists):
- tokens.css
- _tokens.scss
- tailwind.tokens.js
- tokens.json

If files already exist → back up as {filename}.bak before overwriting.
```

---

## Output Summary

```
## ✅ figma-design-token-extractor 完了

| カテゴリ | 抽出数 |
|---------|------|
| Colors | {count} |
| Typography | {count} |
| Spacing | {count} |
| Border Radius | {count} |
| Shadows | {count} |

生成ファイル:
- tokens.css ✅
- _tokens.scss ✅
- tailwind.tokens.js ✅
- tokens.json ✅
```

---

*Skill: figma-design-token-extractor | Category: figma | Version: v1.0 | Last updated: 2026-02-21*
