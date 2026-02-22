# API Reference Category — Context & Conventions

> This CLAUDE.md is auto-read when working inside the `api-reference/` directory.
> It provides API documentation and integration context for creating skills and agents.

---

## Category Scope

Assets in this category target **API documentation and integration** tasks:
- OpenAPI/Swagger spec generation and validation
- API documentation writing (endpoint descriptions, request/response examples)
- SDK and client generation
- API testing (Postman collections, REST client files)
- Webhook integration implementation
- Rate limiting and retry logic
- API versioning strategies
- Third-party API integration patterns

---

## Common API Styles

When creating skills/agents for this category:
- **REST**: OpenAPI 3.x, Swagger 2.x
- **GraphQL**: Schema definition, resolvers, queries
- **gRPC**: Protobuf definitions
- **WebSocket**: Event definitions and protocols
- **Webhook**: Payload specs and security (HMAC, signature verification)

---

## Directory Layout

```
api-reference/
├── CLAUDE.md              ← This file
├── skills/                ← Skills for API documentation & integration
│   └── {skill-name}/
│       └── SKILL.md
└── agents/                ← Agents for API workflows
    └── {agent-name}.md
```

---

## Conventions for API Reference Assets

### Skills should:
- Specify the API style (REST, GraphQL, etc.)
- Include example request/response payloads
- Define expected output format (markdown, JSON, YAML)
- Reference OpenAPI spec conventions where applicable

### Agents should:
- Define which API spec format to work with
- Include validation steps (spec linting, example testing)
- Generate both human-readable docs and machine-readable specs

---

## Related Docs
- `../../_docs/skills.md` — Skill format reference
- `../../_docs/sub-agents.md` — Agent format reference
- `../../_docs/mcp.md` — MCP for API connections
- `../../registry.md` — All assets registry

*Category: api-reference | Last updated: 2026-02-21*
