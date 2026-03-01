---
name: pm-confidence-check
category: pm
tags: [pm, confidence, pre-check, assessment, quality-gate]
model: sonnet
allowed-tools: Read, Grep, Glob
version: v1.0
use-when: >
  Run BEFORE starting any implementation. Assesses confidence level to prevent wrong-direction work.
  Triggers: "자신감 체크", "confidence check", "실행 전 확인", "信頼度チェック", "can we do this", "이거 할 수 있어?"
---
