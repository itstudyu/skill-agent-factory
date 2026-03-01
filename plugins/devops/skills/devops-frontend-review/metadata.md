---
name: devops-frontend-review
category: devops
tags: [review, frontend, ui, pixel-perfect, screenshot, design-match]
model: sonnet
allowed-tools: Read, Glob, Bash
version: v1.1
use-when: >
  Run after frontend code is written as part of devops-pipeline. User provides a screenshot, image, or Figma link to compare against ALREADY IMPLEMENTED code. This is a post-implementation visual review — NOT code generation. For Figma-to-code generation, use the figma plugin. Triggers: "pixel perfect", "UI 확인", "화면 비교", "디자인 맞춰", "compare screenshot", "フロントエンドレビュー", "UI 검토"
---
