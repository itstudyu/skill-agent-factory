#!/bin/bash
# =============================================================================
# Skill & Agent Factory — Global Installer
# =============================================================================
# This script:
#   1. Symlinks all skills/agents into ~/.claude/skills/ and ~/.claude/agents/
#   2. Adds SessionStart hooks to ~/.claude/settings.json so Claude ALWAYS
#      reads the DevOps pipeline rules, even in other projects.
#
# Usage:
#   chmod +x install.sh
#   ./install.sh
#
# To uninstall:
#   ./install.sh --uninstall
# =============================================================================

set -e

FACTORY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
CLAUDE_AGENTS_DIR="$HOME/.claude/agents"
USER_SETTINGS="$HOME/.claude/settings.json"
HOOK_SCRIPT="$FACTORY_DIR/.claude/hooks/inject-instructions.sh"
MODE="${1:-install}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Skill & Agent Factory Installer      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

# ─────────────────────────────────────────────
# UNINSTALL MODE
# ─────────────────────────────────────────────
if [ "$MODE" = "--uninstall" ]; then
  echo -e "${YELLOW}Uninstalling Skill & Agent Factory...${NC}"
  echo ""

  removed=0

  # Remove symlinked skills
  if [ -d "$CLAUDE_SKILLS_DIR" ]; then
    for link in "$CLAUDE_SKILLS_DIR"/*/; do
      if [ -L "${link%/}" ] && [[ "$(readlink "${link%/}")" == "$FACTORY_DIR/skills/"* ]]; then
        rm "${link%/}"
        echo -e "  ${RED}✗${NC} Removed skill: $(basename "${link%/}")"
        ((removed++)) || true
      fi
    done
  fi

  # Remove symlinked agents
  if [ -d "$CLAUDE_AGENTS_DIR" ]; then
    for link in "$CLAUDE_AGENTS_DIR"/*.md; do
      if [ -L "$link" ] && [[ "$(readlink "$link")" == "$FACTORY_DIR/agents/"* ]]; then
        rm "$link"
        echo -e "  ${RED}✗${NC} Removed agent: $(basename "$link")"
        ((removed++)) || true
      fi
    done
  fi

  # Remove user-level hooks from ~/.claude/settings.json
  if [ -f "$USER_SETTINGS" ]; then
    result=$(python3 - "$USER_SETTINGS" "$HOOK_SCRIPT" << 'PYTHON'
import json, sys, os

settings_file = sys.argv[1]
hook_cmd = sys.argv[2]

with open(settings_file) as f:
    try:
        settings = json.load(f)
    except json.JSONDecodeError:
        print("skip")
        sys.exit(0)

hooks = settings.get("hooks", {})
session_start = hooks.get("SessionStart", [])

original_len = len(session_start)
session_start = [
    entry for entry in session_start
    if not any(h.get("command", "") == hook_cmd for h in entry.get("hooks", []))
]

if len(session_start) < original_len:
    hooks["SessionStart"] = session_start
    if not session_start:
        del hooks["SessionStart"]
    if not hooks:
        del settings["hooks"]
    settings["hooks"] = hooks if hooks else settings.get("hooks", {})

    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    print("removed")
else:
    print("not_found")
PYTHON
)
    if [ "$result" = "removed" ]; then
      echo -e "  ${RED}✗${NC} Removed hooks from ~/.claude/settings.json"
      ((removed++)) || true
    fi
  fi

  echo ""
  if [ "$removed" -eq 0 ]; then
    echo "  Nothing to uninstall."
  else
    echo -e "${GREEN}Done! Removed $removed item(s).${NC}"
  fi
  exit 0
fi

# ─────────────────────────────────────────────
# INSTALL MODE
# ─────────────────────────────────────────────

# Create target directories
mkdir -p "$CLAUDE_SKILLS_DIR"
mkdir -p "$CLAUDE_AGENTS_DIR"
mkdir -p "$HOME/.claude"

skill_count=0
agent_count=0
skip_count=0

# ── Link Skills ──────────────────────────────
echo -e "${BLUE}Linking skills...${NC}"

if [ -d "$FACTORY_DIR/skills" ]; then
  for skill_dir in "$FACTORY_DIR/skills"/*/; do
    [ -d "$skill_dir" ] || continue

    skill_name=$(basename "$skill_dir")
    target="$CLAUDE_SKILLS_DIR/$skill_name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo -e "  ${YELLOW}⚠${NC}  Skipped (real file exists): $skill_name"
      ((skip_count++)) || true
    elif [ -L "$target" ]; then
      rm "$target"
      ln -s "$skill_dir" "$target"
      echo -e "  ${GREEN}↻${NC}  Updated: $skill_name"
      ((skill_count++)) || true
    else
      ln -s "$skill_dir" "$target"
      echo -e "  ${GREEN}✓${NC}  Linked: $skill_name"
      ((skill_count++)) || true
    fi
  done

  if [ "$skill_count" -eq 0 ] && [ "$skip_count" -eq 0 ]; then
    echo "  (No skills found yet)"
  fi
else
  echo "  (skills/ directory not found)"
fi

echo ""

# ── Link Agents ──────────────────────────────
echo -e "${BLUE}Linking agents...${NC}"

if [ -d "$FACTORY_DIR/agents" ]; then
  for agent_file in "$FACTORY_DIR/agents"/*.md; do
    [ -f "$agent_file" ] || continue

    agent_name=$(basename "$agent_file")
    target="$CLAUDE_AGENTS_DIR/$agent_name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo -e "  ${YELLOW}⚠${NC}  Skipped (real file exists): $agent_name"
      ((skip_count++)) || true
    elif [ -L "$target" ]; then
      rm "$target"
      ln -s "$agent_file" "$target"
      echo -e "  ${GREEN}↻${NC}  Updated: $agent_name"
      ((agent_count++)) || true
    else
      ln -s "$agent_file" "$target"
      echo -e "  ${GREEN}✓${NC}  Linked: $agent_name"
      ((agent_count++)) || true
    fi
  done

  if [ "$agent_count" -eq 0 ] && [ "$skip_count" -eq 0 ]; then
    echo "  (No agents found yet)"
  fi
else
  echo "  (agents/ directory not found)"
fi

echo ""

# ── Add User-Level Hooks ──────────────────────
echo -e "${BLUE}Configuring user-level hooks (~/.claude/settings.json)...${NC}"

hook_result=$(python3 - "$USER_SETTINGS" "$HOOK_SCRIPT" << 'PYTHON'
import json, sys, os

settings_file = sys.argv[1]
hook_cmd = sys.argv[2]

# Load existing settings (or start fresh)
if os.path.exists(settings_file):
    with open(settings_file) as f:
        try:
            settings = json.load(f)
        except json.JSONDecodeError:
            settings = {}
else:
    settings = {}

# Ensure structure exists
if "hooks" not in settings:
    settings["hooks"] = {}
if "SessionStart" not in settings["hooks"]:
    settings["hooks"]["SessionStart"] = []

# Remove existing entries from this factory (idempotent — prevent duplicates)
settings["hooks"]["SessionStart"] = [
    entry for entry in settings["hooks"]["SessionStart"]
    if not any(h.get("command", "") == hook_cmd for h in entry.get("hooks", []))
]

# Add hooks for startup, compact (after context compaction), and resume
for matcher in ["startup", "compact", "resume"]:
    settings["hooks"]["SessionStart"].append({
        "matcher": matcher,
        "hooks": [{"type": "command", "command": hook_cmd}]
    })

# Write back
os.makedirs(os.path.dirname(os.path.abspath(settings_file)), exist_ok=True)
with open(settings_file, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print("ok")
PYTHON
)

if [ "$hook_result" = "ok" ]; then
  echo -e "  ${GREEN}✓${NC}  Hooks registered (startup / compact / resume)"
  echo -e "  ${GREEN}✓${NC}  DevOps pipeline rules will load in ALL projects"
else
  echo -e "  ${YELLOW}⚠${NC}  Could not update ~/.claude/settings.json (Python error)"
fi

echo ""
echo -e "${GREEN}══════════════════════════════════════════${NC}"
echo -e "${GREEN}  Install complete!${NC}"
echo -e "${GREEN}  Skills linked  : $skill_count${NC}"
echo -e "${GREEN}  Agents linked  : $agent_count${NC}"
if [ "$skip_count" -gt 0 ]; then
echo -e "${YELLOW}  Skipped        : $skip_count (conflict with existing files)${NC}"
fi
echo -e "${GREEN}══════════════════════════════════════════${NC}"
echo ""
echo "  ✅ Skills available globally in all Claude Code projects"
echo "  ✅ DevOps pipeline rules auto-loaded at every session start"
echo ""
echo "  Run this script again after adding new skills/agents to update links."
echo "  To uninstall:  ./install.sh --uninstall"
echo ""

# ── Auto-sync registry ────────────────────────
echo -e "${BLUE}Syncing registry.md and README.md...${NC}"
if command -v python3 &>/dev/null && [ -f "$FACTORY_DIR/scripts/sync-registry.py" ]; then
  python3 "$FACTORY_DIR/scripts/sync-registry.py"
else
  echo -e "  ${YELLOW}⚠${NC}  python3 not found — skipping auto-sync (run manually: python3 scripts/sync-registry.py)"
fi
echo ""
