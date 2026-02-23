# ============================================================
# Skill & Agent Factory — Makefile
# ============================================================
# 使い方:
#   make install    → ~/.claude/ へシンボリックリンクを作成
#   make lint       → スキル・エージェントの品質チェック
#   make lint-strict→ 警告もエラーとして扱う厳格モード
#   make sync       → registry.md と README.md を自動更新
#   make graph      → 依存関係ツリーを表示
#   make check      → 依存関係の問題をチェック
#   make validate   → lint + sync + check を一括実行
#   make help       → このヘルプを表示

SHELL := /bin/bash
PYTHON := python3
SCRIPTS := scripts

.PHONY: install lint lint-strict sync graph check validate help

# ── インストール ────────────────────────────────────────────
install:
	@echo "🔗 Installing skills and agents to ~/.claude/ ..."
	@bash install.sh

# ── Lint ───────────────────────────────────────────────────
lint:
	@$(PYTHON) $(SCRIPTS)/lint-skills.py

lint-strict:
	@$(PYTHON) $(SCRIPTS)/lint-skills.py --strict

# ── Registry 同期 ───────────────────────────────────────────
sync:
	@$(PYTHON) $(SCRIPTS)/sync-registry.py

# ── 依存グラフ ──────────────────────────────────────────────
graph:
	@$(PYTHON) $(SCRIPTS)/dep-graph.py

check:
	@$(PYTHON) $(SCRIPTS)/dep-graph.py --check

# ── 一括バリデーション ──────────────────────────────────────
validate: lint sync check
	@echo ""
	@echo "✅  validate complete"

# ── ヘルプ ─────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Skill & Agent Factory — Available commands"
	@echo ""
	@echo "  make install      Install skills/agents to ~/.claude/"
	@echo "  make lint         Check skill/agent quality"
	@echo "  make lint-strict  Lint with warnings as errors"
	@echo "  make sync         Update registry.md and README.md"
	@echo "  make graph        Show full dependency tree"
	@echo "  make check        Check dependency issues only"
	@echo "  make validate     Run lint + sync + check"
	@echo "  make help         Show this message"
	@echo ""
