# Skill & Agent Factory

> **ALWAYS READ THIS FILE FIRST.**
> Plugin-based workspace for Claude Code skills and agents. 3-tier architecture: `metadata.md` → `SKILL.md` → `resources/`.

---

## Quick Reference

| Need | File |
|------|------|
| How to add a skill / agent / plugin | `_docs/how-it-works.md` |
| Skill format (metadata.md, SKILL.md fields) | `_docs/skills.md` |
| Agent format | `_docs/sub-agents.md` |
| Agent Teams setup & registration | `_docs/agent-teams.md` |
| DevOps pipeline steps (full) | `plugins/devops/agents/devops-pipeline.md` |
| Registry of all assets | `registry.md` |

---

## Routing

```
User Request
    ↓
CLAUDE.md  (this file — routing rules)
    ↓
metadata.md scan  (Tier 1: tags + use-when match)
    ↓
SKILL.md load     (Tier 2: full instructions, matched skill only)
    ↓
devops-pipeline   (quality gate — ALL coding tasks)
```

- **Single-skill request** → invoke directly via metadata.md tag match
- **Figma request** → devops-pipeline → figma-to-code agent
- **ANY coding task** → devops-pipeline **always** runs. No exceptions.

---

## Coding Standards (MANDATORY — every file)

1. **File header** — first line of every source file: one-line Japanese summary comment
   - e.g. `// ユーザー認証サービス — JWTトークンの発行・検証を担当`
2. **Function max 30 lines** — split if exceeded; comment if logically unavoidable
3. **One file, one responsibility** — no unrelated logic in the same file
4. **Commit confirmation** — always show branch / files / message and wait for approval before `git commit`

Full examples → `standards/CODING-STANDARDS.md`

---

## Active Teams

| Team | Execution | Purpose |
|------|-----------|---------|
| `review-team` | Parallel | Code quality, security, architecture |
| `quality-team` | Sequential | Tests, Japanese comments, version check |
| `commit-team` | Sequential | Git commit — final step |
| `feature-team` | Gated | Requirements confirmed → design → implementation |
| `eventbus-team` | Sequential | Vert.x: repo-analyze → register → api-caller |

New team → add row here + `_docs/agent-teams.md` + `KNOWN_TEAMS` in `scripts/lint-skills.py`

---

## Verification Skills (kimoring-ai-skills)

Session-based verification framework. Skills are auto-discovered via glob — no manual registry needed.

| Skill | Purpose | When to Run |
|-------|---------|-------------|
| `manage-skills` | Analyze session changes, create/update verify skills, manage CLAUDE.md | After implementation, before PR |
| `verify-implementation` | Sequentially run all verify skills, produce integrated report | After implementation, during review |

**How it works:**

```
Code changes → /manage-skills → discover .claude/skills/verify-*/ via glob
    → gap analysis → create/update verify skills
    → /verify-implementation → run all checks → integrated report
```

Verify skills are dynamically discovered from `.claude/skills/verify-*/SKILL.md`. No triple-sync needed.

**Verification covers ALL project assets (14 categories):**

| # | Category | Asset | What it checks |
|---|----------|-------|---------------|
| 1 | Skill Structure | `lint-skills.py` | Frontmatter, required fields, circular deps |
| 2 | Dependency Graph | `dep-graph.py` | Circular references, deep chains |
| 3 | Registry Sync | `sync-registry.py` | registry.md / README.md up to date |
| 4 | Security | `devops-safety-check` | Secrets, injection, vulnerabilities |
| 5 | Code Quality | `devops-code-review` | Logic, performance, N+1, dead code |
| 6 | Architecture | `devops-arch-review` | Structure, naming, duplication, SRP |
| 7 | Japanese Comments | `devops-japanese-comments` | All comments/logs in Japanese |
| 8 | Coding Standards | `CODING-STANDARDS.md` | 10 global rules |
| 9 | Version Compat | `devops-version-check` | Language/library version |
| 10 | Tests | `devops-test-gen` | Test coverage |
| 11 | Frontend | `devops-frontend-review` + figma | UI, responsive, design tokens |
| 12 | Vert.x | vertx skills | EventBus, API, repo structure |
| 13 | Git | `devops-git-commit` | Branch strategy, commit format |
| 14 | Custom | `.claude/skills/verify-*` | User-created verify skills |

---

## After Any Change

```bash
make validate   # lint + sync registry.md + README.md auto-update
./install.sh    # re-run after adding new skills or agents
```

---

## Communication

- **Korean** with user — **English** for all asset files
- Always confirm before overwriting existing assets
- Always ask when requirements are unclear — never assume

---

*Last updated: 2026-03-01*
*Project: Skill & Agent Factory v2.3 (3-tier skills + Agent Teams + Makefile + vertx plugin + kimoring verification)*
