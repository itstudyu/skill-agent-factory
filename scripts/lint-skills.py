#!/usr/bin/env python3
"""
lint-skills.py — スキル・エージェント品質チェッカー

新しいスキルの追加・既存スキルの変更後に自動実行され、
一貫性・参照整合性・規約準拠を検証する。

install.sh から自動呼び出し、または単独実行:
  python3 scripts/lint-skills.py
  python3 scripts/lint-skills.py --strict   # 警告もエラー扱い
"""

import os
import re
import sys
from pathlib import Path

# ============================================================
# 設定
# ============================================================
FACTORY_ROOT = Path(__file__).parent.parent
SKILLS_DIR   = FACTORY_ROOT / "skills"
AGENTS_DIR   = FACTORY_ROOT / "agents"
STRICT_MODE  = "--strict" in sys.argv

# 実行時に生成されるパスは存在チェックから除外
RUNTIME_PATH_PREFIXES = (
    "project-context/",
    ".skill-factory-context",
)

# ── ANSI カラー ──────────────────────────────────────────
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
BLUE   = "\033[34m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):   print(f"  {GREEN}✓{RESET}  {msg}")
def warn(msg): print(f"  {YELLOW}⚠{RESET}  {msg}")
def err(msg):  print(f"  {RED}✗{RESET}  {msg}")


# ============================================================
# フロントマターパーサー (sync-registry.py と共通ロジック)
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


def read_body(filepath: Path) -> str:
    """フロントマターを除いた本文を返す"""
    try:
        text = filepath.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

    if not text.startswith("---"):
        return text

    end = text.find("\n---", 3)
    if end == -1:
        return text

    return text[end + 4:].strip()


# ============================================================
# チェック関数
# ============================================================
def check_skill(skill_dir: Path, all_skill_names: set) -> tuple[int, int]:
    """単一スキルをチェック。(errors, warnings) を返す"""
    errors = 0
    warnings = 0
    skill_md = skill_dir / "SKILL.md"
    dir_name = skill_dir.name

    # ── SKILL.md 存在チェック ──────────────────────────
    if not skill_md.exists():
        err(f"[{dir_name}] SKILL.md が存在しない")
        return 1, 0

    fm = parse_frontmatter(skill_md)
    body = read_body(skill_md)

    # ── フロントマター: name ────────────────────────────
    if "name" not in fm:
        err(f"[{dir_name}] frontmatter に name: がない")
        errors += 1
    elif fm["name"] != dir_name:
        warn(f"[{dir_name}] name: '{fm['name']}' がディレクトリ名と不一致")
        warnings += 1

    # ── フロントマター: description ─────────────────────
    if "description" not in fm:
        err(f"[{dir_name}] frontmatter に description: がない")
        errors += 1
    elif len(fm["description"]) < 20:
        warn(f"[{dir_name}] description が短すぎる ({len(fm['description'])} 文字) — トリガー精度が下がる可能性")
        warnings += 1

    # ── フロントマター: status=deprecated チェック ───────
    if fm.get("status") == "deprecated":
        warn(f"[{dir_name}] status: deprecated — このスキルは削除予定")
        warnings += 1
        return errors, warnings  # deprecated は以降チェックをスキップ

    # ── フロントマター: requires 参照整合性 ──────────────
    if "requires" in fm:
        requires_raw = fm["requires"]
        # YAML inline array [a, b] または カンマ区切り 両対応
        requires_raw = requires_raw.strip("[]")
        required_skills = [r.strip() for r in requires_raw.split(",") if r.strip()]
        for req in required_skills:
            if req not in all_skill_names:
                err(f"[{dir_name}] requires: '{req}' — skills/ に存在しないスキルを参照")
                errors += 1

    # ── 本文: 空チェック ────────────────────────────────
    if not body:
        err(f"[{dir_name}] SKILL.md の本文が空")
        errors += 1
        return errors, warnings

    # ── 本文: ステップ定義チェック ───────────────────────
    # STEP_ / ## Step N / ## Phase N / ## Scan N / ### N. / ## .+ Checklist のいずれか
    has_step = bool(
        re.search(r"STEP_[A-Z_]+", body) or
        re.search(r"##\s+\w+\s+\d", body) or           # ## Step 1, ## Scan 2, ## Phase 3 など
        re.search(r"##\s+STEP_[A-Z_]+", body) or
        re.search(r"###\s+\d+\.", body) or              # ### 1. 形式
        re.search(r"###\s+[A-Z]\.", body) or            # ### A. 形式
        re.search(r"##\s+\w+\s+Checklist", body, re.IGNORECASE)  # ## Review Checklist など
    )
    if not has_step:
        warn(f"[{dir_name}] ステップ定義が見当たらない (STEP_XXX / ## Step N / ## Scan N 形式)")
        warnings += 1

    # ── 本文: ファイルパス参照チェック ───────────────────
    # Read: path/to/file パターンを抽出して実在確認
    file_refs = re.findall(r"(?:Read|Glob):\s+([\w./\-*{}]+)", body)
    for ref in file_refs:
        # ワイルドカードは除外
        if "*" in ref or "{" in ref:
            continue
        # 絶対パスは無視 (/ 始まり)
        if ref.startswith("/"):
            continue
        # 実行時に生成されるパスは除外
        if any(ref.startswith(prefix) for prefix in RUNTIME_PATH_PREFIXES):
            continue
        ref_path = FACTORY_ROOT / ref
        if not ref_path.exists():
            warn(f"[{dir_name}] '{ref}' を参照しているが、ファイルが存在しない")
            warnings += 1

    return errors, warnings


def check_agent(agent_file: Path, all_skill_names: set) -> tuple[int, int]:
    """単一エージェントをチェック。(errors, warnings) を返す"""
    errors = 0
    warnings = 0
    file_name = agent_file.stem

    fm = parse_frontmatter(agent_file)
    body = read_body(agent_file)

    # ── description チェック ────────────────────────────
    if not body:
        err(f"[agent:{file_name}] ファイルが空")
        return 1, 0

    # エージェントは frontmatter ではなく description: フィールドで識別
    if "description" not in fm:
        # frontmatter なしでも description: フィールドが本文にあるか確認
        if not re.search(r"^description:", body, re.MULTILINE):
            warn(f"[agent:{file_name}] description: フィールドがない — ルーティングに影響する可能性")
            warnings += 1

    # ── 本文: 存在スキル参照チェック ─────────────────────
    # バッククォートやコードブロック内のスキル名のみチェック (説明文の誤検知を防ぐ)
    # 例: `devops-git-commit` や devops-git-commit agent のみ対象
    skill_calls = re.findall(
        r"`((?:devops|figma)-[a-z\-]+)`",
        body
    )
    for skill_ref in set(skill_calls):
        # エージェント名自身は除外
        if skill_ref == file_name:
            continue
        # エージェント名リストにあるなら除外
        if (AGENTS_DIR / f"{skill_ref}.md").exists():
            continue
        if skill_ref not in all_skill_names:
            warn(f"[agent:{file_name}] `{skill_ref}` を参照しているが skills/ にも agents/ にも存在しない")
            warnings += 1

    return errors, warnings


MAX_DEP_DEPTH = 3  # これ以上深い依存チェーンは警告


def _build_deps() -> dict[str, list[str]]:
    """requires: フィールドから依存グラフを構築"""
    deps: dict[str, list[str]] = {}
    if not SKILLS_DIR.exists():
        return deps
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = parse_frontmatter(skill_md)
        if "requires" in fm:
            raw = fm["requires"].strip("[]")
            deps[skill_dir.name] = [r.strip() for r in raw.split(",") if r.strip()]
        else:
            deps[skill_dir.name] = []
    return deps


def check_circular_requires(all_skill_names: set) -> int:
    """requires: の循環参照を検出。エラー数を返す"""
    errors = 0
    deps = _build_deps()

    # DFS で循環検出
    def has_cycle(node: str, visited: set, stack: set) -> bool:
        visited.add(node)
        stack.add(node)
        for neighbor in deps.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, stack):
                    return True
            elif neighbor in stack:
                return True
        stack.discard(node)
        return False

    visited: set = set()
    for skill in deps:
        if skill not in visited:
            if has_cycle(skill, visited, set()):
                err(f"requires: に循環参照が検出された (関連: {skill})")
                errors += 1

    return errors


def check_dep_depth(all_skill_names: set) -> int:
    """依存チェーンが MAX_DEP_DEPTH 以上のスキルを警告。警告数を返す"""
    warnings = 0
    deps = _build_deps()

    def depth(node: str, visited: set) -> int:
        if node in visited or node not in deps:
            return 0
        children = deps[node]
        if not children:
            return 0
        return 1 + max(depth(c, visited | {node}) for c in children)

    for skill in sorted(deps.keys()):
        d = depth(skill, set())
        if d >= MAX_DEP_DEPTH:
            warn(
                f"[{skill}] 依存チェーン深さ {d} (推奨: {MAX_DEP_DEPTH} 未満) "
                f"— 'python3 scripts/dep-graph.py' で詳細確認"
            )
            warnings += 1

    return warnings


# ============================================================
# メイン
# ============================================================
def main() -> int:
    total_errors   = 0
    total_warnings = 0

    print()
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}{BLUE}  skill-agent-factory — Lint チェック{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print()

    # ── スキル一覧を収集 ────────────────────────────────
    all_skill_names: set[str] = set()
    if SKILLS_DIR.exists():
        for d in SKILLS_DIR.iterdir():
            if d.is_dir():
                all_skill_names.add(d.name)

    # ── Skills チェック ─────────────────────────────────
    print(f"{BOLD}📦 Skills ({len(all_skill_names)} 個){RESET}")
    if SKILLS_DIR.exists():
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if not skill_dir.is_dir():
                continue
            e, w = check_skill(skill_dir, all_skill_names)
            if e == 0 and w == 0:
                ok(skill_dir.name)
            total_errors   += e
            total_warnings += w
    else:
        warn("skills/ ディレクトリが見つからない")
        total_warnings += 1

    print()

    # ── Agents チェック ─────────────────────────────────
    agent_files = sorted(AGENTS_DIR.glob("*.md")) if AGENTS_DIR.exists() else []
    print(f"{BOLD}🤖 Agents ({len(agent_files)} 個){RESET}")
    for agent_file in agent_files:
        e, w = check_agent(agent_file, all_skill_names)
        if e == 0 and w == 0:
            ok(agent_file.stem)
        total_errors   += e
        total_warnings += w

    print()

    # ── 循環参照チェック ────────────────────────────────
    print(f"{BOLD}🔄 循環参照チェック{RESET}")
    cycle_errors = check_circular_requires(all_skill_names)
    if cycle_errors == 0:
        ok("循環参照なし")
    total_errors += cycle_errors

    print()

    # ── 依存チェーン深さチェック ─────────────────────────
    print(f"{BOLD}📏 依存チェーン深さチェック (推奨: {MAX_DEP_DEPTH} 未満){RESET}")
    depth_warnings = check_dep_depth(all_skill_names)
    if depth_warnings == 0:
        ok(f"全チェーン深さ {MAX_DEP_DEPTH} 未満")
    total_warnings += depth_warnings

    print()

    # ── サマリー ────────────────────────────────────────
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    effective_errors = total_errors + (total_warnings if STRICT_MODE else 0)

    if total_errors == 0 and total_warnings == 0:
        print(f"{GREEN}{BOLD}  ✅  すべてのチェックをパス!{RESET}")
    elif effective_errors == 0:
        print(f"{YELLOW}{BOLD}  ⚠  警告 {total_warnings} 件 (エラーなし){RESET}")
        if STRICT_MODE:
            print(f"{RED}  --strict モード: 警告をエラーとして扱います{RESET}")
    else:
        print(f"{RED}{BOLD}  ❌  エラー {total_errors} 件 / 警告 {total_warnings} 件{RESET}")
        if STRICT_MODE and total_warnings > 0:
            print(f"{RED}  --strict モード: 警告もエラーとして扱います{RESET}")

    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print()

    return 1 if effective_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
