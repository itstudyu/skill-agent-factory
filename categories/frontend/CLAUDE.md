# Frontend Category — Context & Conventions

> This CLAUDE.md is auto-read when working inside the `frontend/` directory.
> It provides frontend-specific context for creating skills and agents.

---

## Category Scope

Assets in this category target **frontend development** tasks:
- UI component creation and refactoring
- State management (Redux, Zustand, Pinia, etc.)
- Styling (CSS, Tailwind, CSS-in-JS, SCSS)
- Responsive design implementation
- Accessibility (ARIA, a11y best practices)
- Performance optimization (lazy loading, bundle size, Core Web Vitals)
- Testing (unit with Vitest/Jest, e2e with Playwright/Cypress)
- Build tooling (Vite, Webpack, ESBuild)

---

## Common Tech Stacks

When creating skills/agents for this category, consider these common stacks:
- **React**: Next.js, Remix, Vite
- **Vue**: Nuxt, Vite
- **Angular**: Angular CLI
- **Svelte**: SvelteKit
- **Vanilla**: HTML/CSS/JS

---

## Directory Layout

```
plugins/frontend/               ← future plugin
├── plugin.json
├── agents/                     ← Agents for frontend workflows
│   └── {agent-name}.md
└── skills/                     ← Skills for frontend tasks
    └── {skill-name}/
        ├── metadata.md         ← Tier 1: routing (always loaded)
        └── SKILL.md            ← Tier 2: full instructions
```

---

## Conventions for Frontend Assets

### Skills should:
- Specify which framework they target (or state "framework-agnostic")
- Include component code examples when helpful
- Reference design system conventions if applicable
- Address accessibility requirements

### Agents should:
- Include visual validation steps where applicable
- Define how to verify UI changes (screenshot, test run, etc.)
- Specify styling approach clearly

---

## Related Docs
- `../../_docs/skills.md` — Skill format reference
- `../../_docs/sub-agents.md` — Agent format reference
- `../../registry.md` — All assets registry

*Category: frontend | Last updated: 2026-02-21*
