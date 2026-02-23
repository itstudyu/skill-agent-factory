#!/usr/bin/env python3
"""
dep-graph.py — スキル依存関係グラフ

requires: フィールドを元に依存ツリーを可視化し、
削除・変更時の影響範囲を即座に把握できる。

使い方:
  python3 scripts/dep-graph.py                          # 全依存ツリー表示
  python3 scripts/dep-graph.py --reverse <skill-name>   # 逆引き: このスキルに依存するもの
  python3 scripts/dep-graph.py --check                  # 問題のある依存のみ表示
"""

import re
import sys
from pathlib import Path

# ============================================================
# 設定
# ============================================================
FACTORY_ROOT = Path(__file__).parent.parent
PLUGINS_DIR  = FACTORY_ROOT / "plugins"

# ── ANSI カラー ──────────────────────────────────────────
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

MAX_DEPTH_WARN = 3   # これ以上深いチェーンは警告


# ============================================================
# フロントマターパーサー (共通ロジック)
# ============================================================
def parse_frontmatter(filepath: Path) -> dict:
    try:
        text = filepath.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm_block = text[3:end].strip()
    result = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if key and val:
            result[key] = val
    return result


# ============================================================
# 依存グラフの構築
# ============================================================
def build_dep_graph() -> tuple[dict[str, list[str]], dict[str, bool]]:
    """
    plugins/*/skills/*/metadata.md (fallback: SKILL.md) をスキャンして依存グラフを構築。
    returns:
      deps:       { skill_name: [required_skill, ...] }
      deprecated: { skill_name: True/False }
    """
    deps: dict[str, list[str]] = {}
    deprecated: dict[str, bool] = {}

    if not PLUGINS_DIR.exists():
        return deps, deprecated

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            continue

        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            # metadata.md 優先、なければ SKILL.md にフォールバック
            meta_md  = skill_dir / "metadata.md"
            skill_md = skill_dir / "SKILL.md"
            source = meta_md if meta_md.exists() else (skill_md if skill_md.exists() else None)
            if source is None:
                continue

            fm   = parse_frontmatter(source)
            name = fm.get("name", skill_dir.name)
            deprecated[name] = (fm.get("status") == "deprecated")

            if "requires" in fm:
                raw = fm["requires"].strip("[]")
                deps[name] = [r.strip() for r in raw.split(",") if r.strip()]
            else:
                deps[name] = []

    return deps, deprecated


def build_reverse_graph(deps: dict[str, list[str]]) -> dict[str, list[str]]:
    """逆依存グラフ: { skill: [このスキルを requires している他スキル, ...] }"""
    rev: dict[str, list[str]] = {k: [] for k in deps}
    for skill, requires in deps.items():
        for req in requires:
            if req not in rev:
                rev[req] = []
            rev[req].append(skill)
    return rev


# ============================================================
# ツリー表示
# ============================================================
def print_tree(
    node: str,
    deps: dict[str, list[str]],
    deprecated: dict[str, bool],
    prefix: str = "",
    is_last: bool = True,
    visited: set | None = None,
    depth: int = 0,
) -> int:
    """依存ツリーを再帰的に表示。最大深さを返す"""
    if visited is None:
        visited = set()

    connector = "└── " if is_last else "├── "
    child_prefix = prefix + ("    " if is_last else "│   ")

    # ノード表示
    dep_marker = ""
    if deprecated.get(node):
        dep_marker = f" {YELLOW}[deprecated]{RESET}"
    depth_marker = ""
    if depth >= MAX_DEPTH_WARN:
        depth_marker = f" {RED}⚠ depth={depth}{RESET}"

    print(f"{prefix}{connector}{CYAN}{node}{RESET}{dep_marker}{depth_marker}")

    if node in visited:
        print(f"{child_prefix}{DIM}(circular — already visited){RESET}")
        return depth

    visited = visited | {node}
    children = deps.get(node, [])
    max_depth = depth

    for i, child in enumerate(children):
        child_is_last = (i == len(children) - 1)
        d = print_tree(child, deps, deprecated, child_prefix, child_is_last, visited, depth + 1)
        max_depth = max(max_depth, d)

    return max_depth


def print_reverse_tree(
    node: str,
    rev: dict[str, list[str]],
    deprecated: dict[str, bool],
    prefix: str = "",
    is_last: bool = True,
    visited: set | None = None,
) -> None:
    """逆依存ツリー表示"""
    if visited is None:
        visited = set()

    connector = "└── " if is_last else "├── "
    child_prefix = prefix + ("    " if is_last else "│   ")

    dep_marker = f" {YELLOW}[deprecated]{RESET}" if deprecated.get(node) else ""
    print(f"{prefix}{connector}{CYAN}{node}{RESET}{dep_marker}")

    if node in visited:
        print(f"{child_prefix}{DIM}(circular){RESET}")
        return

    visited = visited | {node}
    parents = rev.get(node, [])
    for i, parent in enumerate(parents):
        is_last_parent = (i == len(parents) - 1)
        print_reverse_tree(parent, rev, deprecated, child_prefix, is_last_parent, visited)


# ============================================================
# メインコマンド
# ============================================================
def cmd_tree(deps: dict[str, list[str]], deprecated: dict[str, bool]) -> None:
    """全スキルの依存ツリーを表示"""
    print()
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}{BLUE}  依存関係ツリー (requires: → 子スキル){RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print()

    # 依存されていないルートスキル (誰にも requires されていない)
    all_required = {req for reqs in deps.values() for req in reqs}
    roots = [s for s in deps if s not in all_required]

    # 依存あり / なし に分類
    has_deps = {s: reqs for s, reqs in deps.items() if reqs}
    no_deps   = [s for s in deps if not deps[s]]

    deep_chains: list[tuple[str, int]] = []

    if has_deps:
        print(f"{BOLD}🔗 依存あり ({len(has_deps)} 件){RESET}")
        skills_with_deps = sorted(has_deps.keys())
        for i, skill in enumerate(skills_with_deps):
            is_last = (i == len(skills_with_deps) - 1)
            connector = "└── " if is_last else "├── "
            child_prefix = "    " if is_last else "│   "
            dep_marker = f" {YELLOW}[deprecated]{RESET}" if deprecated.get(skill) else ""
            print(f"{connector}{CYAN}{skill}{RESET}{dep_marker}")
            children = deps.get(skill, [])
            for j, child in enumerate(children):
                child_is_last = (j == len(children) - 1)
                d = print_tree(child, deps, deprecated, child_prefix, child_is_last, {skill}, depth=1)
                if d >= MAX_DEPTH_WARN:
                    deep_chains.append((skill, d))
        print()

    if no_deps:
        print(f"{BOLD}🔹 依存なし ({len(no_deps)} 件){RESET}")
        for s in sorted(no_deps):
            dep_marker = f" {YELLOW}[deprecated]{RESET}" if deprecated.get(s) else ""
            print(f"  {DIM}○{RESET}  {s}{dep_marker}")
        print()

    if deep_chains:
        print(f"{YELLOW}{BOLD}⚠  深い依存チェーン (depth ≥ {MAX_DEPTH_WARN}):{RESET}")
        for skill, depth in deep_chains:
            print(f"  {skill} — 深さ {depth}")
        print()


def cmd_reverse(
    target: str,
    deps: dict[str, list[str]],
    deprecated: dict[str, bool],
) -> None:
    """特定スキルの逆依存を表示 (このスキルを削除したら何が壊れるか)"""
    rev = build_reverse_graph(deps)

    print()
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}{BLUE}  逆引き: '{target}' に依存するスキル{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print()

    if target not in deps:
        print(f"  {RED}✗{RESET}  '{target}' は skills/ に存在しません")
        print()
        print(f"  利用可能なスキル: {', '.join(sorted(deps.keys()))}")
        print()
        return

    parents = rev.get(target, [])

    dep_marker = f" {YELLOW}[deprecated]{RESET}" if deprecated.get(target) else ""
    print(f"  {CYAN}{target}{RESET}{dep_marker}")

    if not parents:
        print(f"  {GREEN}✓{RESET}  このスキルを requires しているスキルはありません")
        print(f"  {GREEN}   → 安全に削除・変更できます{RESET}")
    else:
        print(f"  {YELLOW}⚠{RESET}  以下のスキルがこのスキルに依存しています:")
        print()
        for i, parent in enumerate(sorted(parents)):
            is_last = (i == len(parents) - 1)
            connector = "└── " if is_last else "├── "
            child_prefix = "    " if is_last else "│   "
            dep_marker2 = f" {YELLOW}[deprecated]{RESET}" if deprecated.get(parent) else ""
            print(f"  {connector}{CYAN}{parent}{RESET}{dep_marker2}")
            # さらに上位の依存も表示
            grand_parents = rev.get(parent, [])
            for j, gp in enumerate(sorted(grand_parents)):
                gp_last = (j == len(grand_parents) - 1)
                print_reverse_tree(gp, rev, deprecated, "  " + child_prefix, gp_last, {parent, target})

        print()
        print(f"  {RED}→ '{target}' を削除・変更する場合は上記 {len(parents)} 件への影響を確認してください{RESET}")

    print()


def cmd_check(deps: dict[str, list[str]], deprecated: dict[str, bool]) -> None:
    """問題のある依存のみ表示 (lint-skills.py の依存特化版)"""
    print()
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}{BLUE}  依存関係チェック{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print()

    issues = 0
    all_skills = set(deps.keys())

    for skill, requires in sorted(deps.items()):
        for req in requires:
            if req not in all_skills:
                print(f"  {RED}✗{RESET}  [{skill}] requires '{req}' — 存在しないスキルを参照")
                issues += 1
            elif deprecated.get(req):
                print(f"  {YELLOW}⚠{RESET}  [{skill}] requires '{req}' — deprecatedスキルに依存")
                issues += 1

    # 深いチェーン検出
    def chain_depth(node: str, visited: set) -> int:
        if node in visited or node not in deps:
            return 0
        children = deps[node]
        if not children:
            return 0
        return 1 + max(chain_depth(c, visited | {node}) for c in children)

    for skill in sorted(deps.keys()):
        d = chain_depth(skill, set())
        if d >= MAX_DEPTH_WARN:
            print(f"  {YELLOW}⚠{RESET}  [{skill}] 依存チェーン深さ {d} (推奨: {MAX_DEPTH_WARN} 未満)")
            issues += 1

    if issues == 0:
        print(f"  {GREEN}✓{RESET}  問題のある依存関係は見つかりませんでした")
    else:
        print()
        print(f"  {YELLOW}合計 {issues} 件の問題{RESET}")

    print()


# ============================================================
# エントリポイント
# ============================================================
def main() -> int:
    args = sys.argv[1:]
    deps, deprecated = build_dep_graph()

    if not deps:
        print(f"{RED}skills/ ディレクトリが見つからないか、スキルが存在しません{RESET}")
        return 1

    if "--reverse" in args:
        idx = args.index("--reverse")
        if idx + 1 >= len(args):
            print(f"{RED}使い方: dep-graph.py --reverse <skill-name>{RESET}")
            return 1
        target = args[idx + 1]
        cmd_reverse(target, deps, deprecated)

    elif "--check" in args:
        cmd_check(deps, deprecated)

    else:
        cmd_tree(deps, deprecated)

    return 0


if __name__ == "__main__":
    sys.exit(main())
