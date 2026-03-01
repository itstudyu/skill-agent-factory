---
name: figma-code-sync
category: figma
tags: [figma, sync, verify, design-match, implementation, validate]
model: sonnet
allowed-tools: Read, Grep, Glob, mcp__figma__get_file, mcp__figma__get_node
requires: [figma-framework-figma-mapper, figma-design-token-extractor]
use-when: >
  User wants to validate that implemented code matches the Figma design, check for missing components or style mismatches. Triggers: "figma 맞는지", "design sync", "구현 검증", "figma code sync", "check if matches Figma", "validate design implementation"
version: v1.0
---
