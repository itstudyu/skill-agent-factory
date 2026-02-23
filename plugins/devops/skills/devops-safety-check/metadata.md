---
name: devops-safety-check
category: devops
tags: [security, safety, secrets, vulnerability, sql-injection, xss]
model: haiku
allowed-tools: Grep, Read, Glob, Bash
version: v1.0
use-when: >
  Run after code is written. Quick security scan for secrets, SQL injection, XSS, vulnerable dependencies. Triggers: "보안 확인", "security check", "セキュリティチェック", "시크릿 노출", "취약점 확인", "secret leak", "vulnerability scan"
---
