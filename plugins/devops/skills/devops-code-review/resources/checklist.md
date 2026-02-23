# Code Review Checklist

> Load this file when the user asks for a detailed checklist or when reviewing complex code.
> Reference in SKILL.md: `Read: plugins/devops/skills/devops-code-review/resources/checklist.md`

## Logic & Correctness
- [ ] Off-by-one errors in loops / array indexing
- [ ] Null / undefined dereferencing without guard
- [ ] Incorrect boolean logic (AND vs OR, negation)
- [ ] Integer overflow in arithmetic operations
- [ ] Floating point comparison (use epsilon, not `===`)

## Memory & Performance
- [ ] Unbounded loops or recursion without base case
- [ ] Large object allocation inside hot loops
- [ ] Event listener / timer not cleaned up (memory leak)
- [ ] N+1 query pattern in loops over collections
- [ ] Synchronous blocking call in async context

## Error Handling
- [ ] All `try/catch` blocks have meaningful handling (not just `console.log`)
- [ ] Async errors propagated (`.catch()` or `await` inside `try`)
- [ ] HTTP error status codes handled (4xx / 5xx)
- [ ] File / DB operations have error fallback

## Security (quick scan — full scan → devops-safety-check)
- [ ] No hardcoded secrets or tokens
- [ ] User input sanitized before DB query / HTML render
- [ ] Sensitive data not logged

## Code Quality
- [ ] Functions ≤ 30 lines (project rule)
- [ ] No duplicated logic — DRY principle
- [ ] Naming: variables/functions describe intent clearly
- [ ] Dead code removed
