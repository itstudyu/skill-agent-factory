---
name: devops-requirements
description: Development requirements gathering. Use at the START of every development request before writing any code. Triggers on requests like "implement X", "create feature", "build API", "add function", "develop", "make a component", "integrate with API", or any feature development task.
allowed-tools: Read, Glob, Grep
---

# Requirements Gathering (Step 1 of Pipeline)

開発を始める前に、必要な情報を必ず収集すること。

## Purpose
Ensure Claude fully understands the requirements before writing a single line of code. If anything is unclear, **STOP and ask the user**. Never assume.

---

## Checklist — Gather All Before Coding

### 1. Understand What to Build
- What is the feature/function doing exactly?
- What is the expected input and output?
- Are there edge cases to handle?

**If unclear → Ask the user immediately.**

### 2. API / External Service Integration
If connecting to an external API:
- [ ] What is the API endpoint URL?
- [ ] What HTTP method? (GET / POST / PUT / PATCH / DELETE)
- [ ] What does the request payload look like? (body, headers, params)
- [ ] What does the response look like? (schema, status codes)
- [ ] Is there authentication? (API key, OAuth, Bearer token)
- [ ] Is there an API reference document? (ask user to provide if available)
- [ ] Are there rate limits?

**If the user hasn't provided an API reference → Ask them to share it.**

### 3. Tech Stack Context
- [ ] What language and framework is being used?
- [ ] What version? (e.g., Node 20, Python 3.11, React 18)
- [ ] Are there existing patterns in the codebase to follow?
- [ ] Any libraries/packages already being used for similar tasks?

**Read existing code first using Glob/Read tools to understand patterns before asking.**

### 4. Acceptance Criteria
- What does "done" look like?
- Is there a design or screenshot? (frontend)
- Are there specific performance requirements?

---

## Decision Rule

| Situation | Action |
|-----------|--------|
| All information is clear | Proceed to development |
| Anything is unclear or ambiguous | Ask the user — list each unclear point as a numbered question |
| API reference not provided | Ask: "Could you share the API documentation or an example request/response?" |
| Task too vague (e.g., "make it work") | Ask for specifics before starting |

---

## Output Format When Asking Questions

```
開発を始める前に確認させてください：

1. [具体的な質問1]
2. [具体的な質問2]
3. [具体的な質問3]

上記をご確認いただけますか？
```

---

## After Requirements Are Clear

Summarize what you understood before starting:

```
## 実装内容の確認

- 機能: [what will be built]
- 技術スタック: [language/framework/version]
- API: [endpoint and method if applicable]
- 完了条件: [what done looks like]

上記の理解で実装を開始します。
```

Then proceed to development.
