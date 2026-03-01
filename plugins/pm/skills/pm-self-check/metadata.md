---
name: pm-self-check
category: pm
tags: [pm, self-check, validation, post-check, evidence, hallucination]
model: sonnet
allowed-tools: Read, Grep, Glob, Bash
version: v1.0
use-when: >
  Run AFTER implementation is complete. Validates work with evidence-based checks to prevent hallucination.
  Triggers: "셀프 체크", "self check", "구현 확인", "완료 확인", "セルフチェック", "is it done", "다 됐어?"
---
