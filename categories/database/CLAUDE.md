# Database Category — Context & Conventions

> This CLAUDE.md is auto-read when working inside the `database/` directory.
> It provides database-specific context for creating skills and agents.

---

## Category Scope

Assets in this category target **database-related** tasks:
- Schema design and documentation
- Migration file creation
- Query optimization (EXPLAIN, index analysis)
- ORM model generation (Prisma, TypeORM, SQLAlchemy, ActiveRecord, GORM)
- Seed data generation
- Database backup and restore procedures
- ERD diagram creation (Mermaid, PlantUML)
- Data validation and constraints
- Stored procedures and functions

---

## Supported Databases

When creating skills/agents, consider these common databases:
- **Relational**: PostgreSQL, MySQL, SQLite, SQL Server, Oracle
- **NoSQL**: MongoDB, Redis, DynamoDB, Firestore
- **Time-series**: InfluxDB, TimescaleDB
- **Search**: Elasticsearch, OpenSearch

---

## Directory Layout

```
database/
├── CLAUDE.md              ← This file
├── skills/                ← Skills for database tasks
│   └── {skill-name}/
│       └── SKILL.md
└── agents/                ← Agents for database workflows
    └── {agent-name}.md
```

---

## Conventions for Database Assets

### Skills should:
- Specify which database system they target (or state "SQL-agnostic")
- Include SQL examples when appropriate
- Handle safety concerns (no DROP without confirmation, backup reminders)
- Reference schema documentation patterns

### Agents should:
- Use read-only tools by default for analysis agents
- Include confirmation steps before destructive operations
- Define rollback procedures when applicable

---

## Safety Rules

> **IMPORTANT for all database agents and skills:**
> - Never execute DROP TABLE / DELETE without explicit user confirmation
> - Always recommend backups before schema migrations
> - Use transactions for multi-step operations
> - Validate SQL before execution when possible

---

## Related Docs
- `../../_docs/skills.md` — Skill format reference
- `../../_docs/sub-agents.md` — Agent format reference
- `../../_docs/mcp.md` — MCP for database connections
- `../../registry.md` — All assets registry

*Category: database | Last updated: 2026-02-21*
