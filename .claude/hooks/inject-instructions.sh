#!/bin/bash
# inject-instructions.sh
# Injects the project's CLAUDE.md instructions into Claude's context.
# Triggered by SessionStart hook (on startup and after compaction).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"

if [ -f "$CLAUDE_MD" ]; then
  echo "=== [SKILL & AGENT FACTORY — PROJECT INSTRUCTIONS RELOADED] ==="
  echo ""
  cat "$CLAUDE_MD"
  echo ""
  echo "=== [END OF PROJECT INSTRUCTIONS] ==="
else
  echo "WARNING: CLAUDE.md not found at $CLAUDE_MD" >&2
fi
