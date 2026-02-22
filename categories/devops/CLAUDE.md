# DevOps Category — Context & Conventions

> This CLAUDE.md is auto-read when working inside the `devops/` directory.
> It provides DevOps and infrastructure context for creating skills and agents.

---

## Category Scope

Assets in this category target **DevOps and infrastructure** tasks:
- CI/CD pipeline configuration (GitHub Actions, GitLab CI, CircleCI, Jenkins)
- Docker and container management (Dockerfile, docker-compose, image optimization)
- Kubernetes manifests (Deployment, Service, Ingress, ConfigMap, Secret)
- Infrastructure as Code (Terraform, Pulumi, AWS CDK)
- Deployment scripts and automation
- Monitoring and alerting setup (Prometheus, Grafana, PagerDuty)
- Log aggregation and analysis (ELK, Loki, CloudWatch)
- Security scanning (SAST, DAST, dependency vulnerabilities)
- Environment configuration management

---

## Common Tools & Platforms

When creating skills/agents for this category:
- **Cloud**: AWS, GCP, Azure
- **Container**: Docker, Podman, containerd
- **Orchestration**: Kubernetes, Docker Swarm, ECS
- **IaC**: Terraform, Pulumi, CloudFormation, Bicep
- **CI/CD**: GitHub Actions, GitLab CI, CircleCI, Jenkins, ArgoCD

---

## Development Pipeline (MANDATORY)

All DevOps skills are organized as a **sequential pipeline** that runs for every development request.

| Step | Skill File | Purpose |
|------|-----------|---------|
| 1 | `skills/devops-requirements/` | Requirements gathering — hard gate |
| 2 | `skills/devops-safety-check/` | Lightweight security scan |
| 3 | `skills/devops-code-review/` | Logic, memory, performance |
| 4 | `skills/devops-japanese-comments/` | Enforce Japanese comments |
| 5 | `skills/devops-frontend-review/` | Pixel-perfect UI check (conditional) |
| 6 | `skills/devops-version-check/` | Version & deprecated API check |
| 7 | `skills/devops-test-gen/` | Auto-generate unit tests |
| 8 | `skills/devops-git-commit/` | Branch strategy + Japanese commit |

Orchestrated by: `agents/devops-pipeline.md`

> All skills and agents live in the root `skills/` and `agents/` directories (not in this category folder).

---

## Directory Layout

```
skill-agent-factory/
├── skills/
│   ├── devops-requirements/SKILL.md
│   ├── devops-safety-check/SKILL.md
│   ├── devops-code-review/SKILL.md
│   ├── devops-japanese-comments/SKILL.md
│   ├── devops-frontend-review/SKILL.md
│   ├── devops-version-check/SKILL.md
│   ├── devops-test-gen/SKILL.md
│   └── devops-git-commit/SKILL.md
└── agents/
    └── devops-pipeline.md
```

---

## Conventions for DevOps Assets

### Skills should:
- Specify the target platform/tool (e.g., "GitHub Actions", "Kubernetes", "AWS")
- Include working configuration examples
- Add security best practices (no hardcoded secrets, use secrets management)
- Reference idempotency requirements

### Agents should:
- Include dry-run / plan steps before applying changes
- Define rollback procedures for deployments
- Require confirmation before destructive infrastructure changes
- Log all actions taken

---

## Safety Rules

> **IMPORTANT for all DevOps agents and skills:**
> - Never hardcode secrets, credentials, or API keys
> - Always use environment variables or secrets managers
> - Include `--dry-run` or `plan` step before applying infrastructure changes
> - Document rollback procedures for every deployment

---

## Related Docs
- `../../_docs/skills.md` — Skill format reference
- `../../_docs/sub-agents.md` — Agent format reference
- `../../_docs/hooks.md` — Hooks for CI/CD automation
- `../../_docs/mcp.md` — MCP for infrastructure tools
- `../../registry.md` — All assets registry

*Category: devops | Last updated: 2026-02-21*
