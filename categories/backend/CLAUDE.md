# Backend Category — Context & Conventions

> This CLAUDE.md is auto-read when working inside the `backend/` directory.
> It provides backend-specific context for creating skills and agents.

---

## Category Scope

Assets in this category target **backend development** tasks:
- Server-side API development (REST, GraphQL, gRPC)
- Business logic implementation
- Authentication & authorization systems
- Database interaction layers (ORM, query builders, raw SQL)
- Background jobs & task queues
- Caching (Redis, in-memory)
- Logging & error handling
- Testing (unit, integration, e2e for APIs)

---

## Common Tech Stacks

When creating skills/agents for this category, consider these common stacks:
- **Node.js**: Express, Fastify, NestJS, Hono
- **Python**: FastAPI, Django, Flask
- **Go**: Gin, Echo, Fiber
- **Java/Kotlin**: Spring Boot
- **Ruby**: Rails

---

## Directory Layout

```
plugins/backend/                ← future plugin
├── plugin.json
├── agents/                     ← Agents for backend workflows
│   └── {agent-name}.md
└── skills/                     ← Skills for backend tasks
    └── {skill-name}/
        ├── metadata.md         ← Tier 1: routing (always loaded)
        └── SKILL.md            ← Tier 2: full instructions
```

---

## Conventions for Backend Assets

### Skills should:
- Specify which backend language/framework they target (or state "framework-agnostic")
- Include code examples in the instruction body
- Reference common patterns: repository pattern, service layer, middleware

### Agents should:
- Have access to `Read`, `Grep`, `Glob`, `Bash` tools at minimum
- Include validation steps (run tests, check types)
- Define clear output format (summary of changes, files modified)

---

## Related Docs
- `../../_docs/skills.md` — Skill format reference
- `../../_docs/sub-agents.md` — Agent format reference
- `../../registry.md` — All assets registry

*Category: backend | Last updated: 2026-02-21*
