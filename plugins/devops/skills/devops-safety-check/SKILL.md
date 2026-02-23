---
name: devops-safety-check
version: v1.0
description: Lightweight code security check. Run after code is written. Checks for secrets, vulnerable dependencies, SQL injection, XSS patterns. Keeps token usage minimal — scan and report only critical issues.
tags: [devops, security, safety, secrets, vulnerability]
allowed-tools: Grep, Read, Glob, Bash
---

# Code Safety Check (Step 2 of Pipeline)

セキュリティチェック — 軽量スキャン、重大な問題のみ報告。

## Rules
- Keep it SHORT. No verbose explanations.
- Report only CRITICAL and WARNING level issues.
- Do NOT rewrite code here — just flag issues for the next step.

---

## Scan 1 — Secrets & Env Variables

```bash
# Search for hardcoded secrets in changed files
grep -rn "api_key\|apikey\|secret\|password\|token\|passwd\|private_key" --include="*.ts" --include="*.js" --include="*.py" --include="*.env" .
```

**Check:**
- [ ] No hardcoded API keys, passwords, tokens in source code
- [ ] `.env` files are in `.gitignore`
- [ ] No credentials in comments

---

## Scan 2 — Dependency Vulnerabilities (Quick)

If `package.json` exists → Check only recently added packages against known CVE patterns:
```bash
# Check for known vulnerable versions
cat package.json | grep -E '"(lodash|axios|express|moment|node-fetch)"'
```

If `requirements.txt` or `pyproject.toml` exists → Same quick check.

**Flag:** Any package pinned to a version known to have CVEs (e.g., lodash < 4.17.21).

---

## Scan 3 — Injection Patterns

```bash
# SQL Injection patterns
grep -rn "query\s*+\s*\|execute(\s*f\"\|format(" --include="*.py" --include="*.ts" --include="*.js" .

# XSS patterns
grep -rn "innerHTML\s*=\|dangerouslySetInnerHTML\|document\.write(" --include="*.ts" --include="*.tsx" --include="*.js" .
```

---

## Output Format (Keep Short)

```
## 🔒 Safety Check

| Level | Issue | File | Line |
|-------|-------|------|------|
| 🔴 CRITICAL | Hardcoded API key | src/api.ts | 23 |
| 🟡 WARNING | innerHTML usage | components/Card.tsx | 45 |

✅ No issues found  (if clean)
```

Pass result to devops-code-review step.
