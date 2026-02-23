---
name: devops-frontend-review
description: Frontend pixel-perfect review. Run after frontend code is written. Compares implementation against provided screenshots or Figma designs. Use when user provides a screenshot, image, or Figma link for UI implementation.
tags: [devops, review, frontend, ui, pixel-perfect, screenshot]
allowed-tools: Read, Glob, Bash
---

# Frontend Visual Review (Step 5 of Pipeline)

フロントエンドの実装がデザインと一致しているか確認する。

**Only run this step if:** the user provided a screenshot, image file, or Figma link as the design reference.

---

## Input Types

### A. User-Provided Screenshot
The user shared a screenshot/image of the expected UI.

### B. Figma Design
The user shared a Figma URL or used Figma MCP to provide design specs.

---

## Review Checklist

### Layout & Structure
- [ ] Page/component layout matches the design (flex direction, grid, alignment)
- [ ] Spacing matches (margin, padding — check against design values)
- [ ] Element order matches (DOM order = visual order)

### Typography
- [ ] Font sizes match the design
- [ ] Font weights (bold, regular, etc.) are correct
- [ ] Text colors match
- [ ] Line heights and letter spacing are consistent

### Colors & Visual
- [ ] Background colors match
- [ ] Border colors, border-radius match
- [ ] Shadows match
- [ ] Icons are the correct ones

### Components
- [ ] All UI elements present in the design are implemented
- [ ] No extra elements that don't exist in the design
- [ ] Interactive states handled (hover, focus, disabled) if shown in design

### Responsive (if design shows multiple breakpoints)
- [ ] Mobile layout matches mobile design
- [ ] Desktop layout matches desktop design

---

## When Using Figma MCP

If Figma MCP is available:
1. Extract exact design tokens (colors, spacing, font sizes) from the Figma file
2. Compare extracted values against the implemented CSS/Tailwind classes
3. List any mismatches with exact values:
   - Design: `color: #3B82F6` → Implementation: `text-blue-400` (wrong, should be `text-blue-500`)

---

## When Using Screenshot

1. Read the screenshot carefully
2. Compare each visible element against the code
3. List visual discrepancies

---

## Output Format

```
## 🎨 Frontend Visual Review

### ✅ Matches
- Layout structure correct
- Typography matches

### ❌ Discrepancies

| Element | Design | Implementation | Fix |
|---------|--------|----------------|-----|
| Button color | #3B82F6 | #60A5FA | Change to `bg-blue-500` |
| Card padding | 24px | 16px | Change to `p-6` |
| Missing element | User avatar | Not implemented | Add `<Avatar>` component |
```

Fix all discrepancies before proceeding.
