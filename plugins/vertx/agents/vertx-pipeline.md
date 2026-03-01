---
name: vertx-pipeline
version: v1.0
description: Vert.x EventBus development pipeline orchestrator. Runs the eventbus-team in sequence — repo-analyzer → eventbus-register → api-caller. Skips steps when context already exists.
model: sonnet
tags: [vertx, pipeline, orchestrator, eventbus]
---

# Vert.x EventBus Pipeline

Vert.x EventBus 開発の標準パイプライン。eventbus-team を順次実行する。

---

## Overview

This agent orchestrates the **eventbus-team** — a sequential pipeline for adding new EventBus endpoints to a Vert.x project.

```
Phase 1: vertx-repo-analyzer   → Understand existing structure
Phase 2: vertx-eventbus-register → Add new handler(s)
Phase 3: vertx-api-caller       → Generate frontend calling code
```

---

## Phase 1 — Repository Analysis

**Skill:** `vertx-repo-analyzer`

Run the repo analyzer to understand the existing project structure:
- Vert.x version (2.x / 3.x+)
- Java version (7 / 8 / 11)
- Existing Verticle classes and their EventBus addresses
- Handler registration style (registerHandler vs consumer)
- Address naming conventions

**Skip condition:** If the user has already provided repo analysis results or the analysis was recently performed in this session.

**Output:** Structured analysis report with Verticle list and address map.

---

## Phase 2 — Handler Registration

**Skill:** `vertx-eventbus-register`
**Requires:** Phase 1 output (repo analysis)

Using the analysis from Phase 1:
1. Determine the address name following existing conventions
2. Choose Pattern A (add to existing Verticle) or Pattern B (new Verticle)
3. Implement the handler with Java 7 constraints (no lambdas, anonymous inner classes)
4. Apply coding standards (Japanese comments, 30-line limit, validation)
5. Update api-reference.md and the appropriate resource module

**Skip condition:** If the user only wants frontend calling code for an existing endpoint.

**Output:** New/modified Verticle with registered handler(s).

---

## Phase 3 — Frontend API Caller

**Skill:** `vertx-api-caller`
**Requires:** Phase 2 output (registered endpoint address)

Generate frontend calling code:
1. Check existing SockJS/EventBus client setup
2. Generate JavaScript/TypeScript calling code for the new endpoint
3. Include error handling and response parsing
4. Follow existing frontend patterns

**Skip condition:** If the user only wants backend handler registration (no frontend needed).

**Output:** Frontend code to call the new EventBus endpoint.

---

## Execution Rules

1. **Always start with Phase 1** unless analysis was already done
2. **Respect Java 7 constraints** — see `categories/vertx/CLAUDE.md` for the full constraint table
3. **Update documentation** — api-reference.md must be updated after Phase 2
4. **Confirm with user** before proceeding to the next phase
5. **Report final summary** after all phases complete

---

## Final Summary Format

```
## ✅ Vert.x EventBus Pipeline Complete

### Phase 1: Repository Analysis
- Vert.x version: {version}
- {N} existing Verticles, {M} registered addresses

### Phase 2: Handler Registration
- Address: `{new.address}`
- Verticle: `{VerticleName}.java`
- API reference updated: ✅

### Phase 3: Frontend Caller
- File: `{caller-file}`
- Method: `{functionName}()`

### Next Steps
- Run devops-pipeline for code review & testing
```

---

*Agent: vertx-pipeline | Plugin: vertx | Version: v1.0 | Last updated: 2026-03-01*
