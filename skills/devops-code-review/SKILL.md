---
name: devops-code-review
description: Code quality and logic review. Run after code is written. Verifies AI-generated code has no bugs, logic errors, memory leaks, or performance issues. Checks that the implementation matches the original request.
allowed-tools: Read, Grep, Glob
---

# Code Quality & Logic Review (Step 3 of Pipeline)

AIが書いたコードに問題がないか確認する。

---

## Review Checklist

### 1. Logic Correctness
- [ ] Does the code actually do what the user requested?
- [ ] Are all edge cases handled? (null, empty, undefined, 0, negative numbers)
- [ ] Are error cases handled properly? (try/catch, error responses)
- [ ] Are async operations awaited correctly? (no floating promises)
- [ ] Are loops and recursions bounded? (no infinite loops)

### 2. Memory Efficiency
- [ ] No unnecessary data copying (large arrays/objects cloned without reason)
- [ ] Event listeners are properly removed when components unmount
- [ ] Streams/file handles/DB connections are closed after use
- [ ] No memory leaks in long-running processes (timers, intervals, listeners)
- [ ] Large datasets use pagination or streaming instead of loading all at once

### 3. Performance & Load
- [ ] No N+1 query problems (loop + individual DB queries)
- [ ] Expensive operations are not repeated unnecessarily — cache where appropriate
- [ ] Heavy computations are not blocking the event loop (use async/worker if needed)
- [ ] API calls inside loops → batch them instead
- [ ] Indexes exist for frequently queried DB fields (flag if missing)

### 4. Code Quality
- [ ] No dead code (unreachable code, unused variables, commented-out blocks)
- [ ] Functions do one thing (Single Responsibility)
- [ ] No magic numbers — use named constants
- [ ] Return types/error types are explicit and correct

### 5. Global Coding Standards (from root CLAUDE.md)
- [ ] **File header**: First line of every source file is a one-line Japanese summary comment
  - e.g., `// ユーザー認証サービス — JWTトークンの発行・検証を担当`
  - If missing → add it
- [ ] **Function length**: No function/method exceeds 30 lines (excluding blanks and comments)
  - If exceeded → split into smaller focused functions
  - Exception: only if logically unavoidable (e.g., long switch) — add a comment explaining why
- [ ] **File responsibility**: Each file handles one feature/concern
  - If a file mixes unrelated concerns → flag it for splitting

---

## Output Format

```
## 🔍 Code Review

### ✅ Correct
- Logic matches the requirements
- Error handling is in place

### ⚠️ Issues Found

| Priority | Issue | File | Line | Fix |
|----------|-------|------|------|-----|
| HIGH | N+1 query in loop | services/user.ts | 78 | Batch with findMany |
| MED | Missing null check | utils/format.ts | 12 | Add `if (!value) return` |
| LOW | Unused variable `temp` | api/handler.ts | 34 | Remove |
```

Fix all HIGH and MED issues before proceeding. LOW issues are optional.
