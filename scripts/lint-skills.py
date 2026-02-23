#!/usr/bin/env python3
"""
lint-skills.py — スキル・エージェント品質チェッカー

新しいスキルの追加・既存スキルの変更後に自動実行され、
一貫性・参照整合性・規約準拠を検証する。

install.sh から自動呼び出し、または単独実行:
  python3 scripts/lint-skills.py
  python3 scripts/lint-skills.py --strict   # 警告もエラー扱い
"""

import json
import os
import re
import sys
from pathlib import Path

# ============================================================
# 設定
# ============================================================
FACTORY_ROOT = Path(__file__).parent.parent
PLUGINS_DIR  = FACTORY_ROOT / "plugins"
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

    # マルチライン YAML ブロックスカラー (use-when: > など) の収集
    def collect_multiline(field_name: str) -> str | None:
        lines_out = []
        in_field = False
        for line in fm_block.splitlines():
            if line.startswith(f"{field_name}:"):
                in_field = True
                val = line.partition(":")[2].strip().strip('"').strip("'").lstrip(">").strip()
                if val:
                    lines_out.append(val)
            elif in_field and (line.startswith("  ") or line.startswith("\t")):
                lines_out.append(line.strip())
            else:
                if in_field:
                    in_field = False
        return " ".join(lines_out) if lines_out else None

    for field in ("description", "use-when"):
        val = collect_multiline(field)
        if val:
            result[field] = val

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
    skill_md  = skill_dir / "SKILL.md"
    meta_md   = skill_dir / "metadata.md"
    dir_name  = skill_dir.name

    # ── SKILL.md 存在チェック ──────────────────────────
    if not skill_md.exists():
        err(f"[{dir_name}] SKILL.md が存在しない")
        return 1, 0

    # metadata.md がある場合はそちらから frontmatter を読む
    fm_source = meta_md if meta_md.exists() else skill_md
    fm   = parse_frontmatter(fm_source)
    body = read_body(skill_md)

    # ── フロントマター: name ────────────────────────────
    if "name" not in fm:
        err(f"[{dir_name}] frontmatter に name: がない")
        errors += 1
    elif fm["name"] != dir_name:
        warn(f"[{dir_name}] name: '{fm['name']}' がディレクトリ名と不一致")
        warnings += 1

    # ── フロントマター: description または use-when ──────
    # metadata.md は use-when: を使用、SKILL.md は description: を使用
    desc_val = fm.get("description") or fm.get("use-when", "")
    if not desc_val:
        err(f"[{dir_name}] frontmatter に description: / use-when: がない")
        errors += 1
    elif len(desc_val) < 20:
        warn(f"[{dir_name}] description/use-when が短すぎる ({len(desc_val)} 文字) — トリガー精度が下がる可能性")
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
    all_agent_names = {f.stem for f in collect_all_agent_files()}
    skill_calls = re.findall(
        r"`((?:devops|figma|project)-[a-z\-]+)`",
        body
    )
    for skill_ref in set(skill_calls):
        # エージェント名自身は除外
        if skill_ref == file_name:
            continue
        # エージェント名リストにあるなら除外
        if skill_ref in all_agent_names:
            continue
        if skill_ref not in all_skill_names:
            warn(f"[agent:{file_name}] `{skill_ref}` を参照しているが plugins/ にも agents/ にも存在しない")
            warnings += 1

    return errors, warnings


MAX_DEP_DEPTH = 3  # これ以上深い依存チェーンは警告

KNOWN_TEAMS = {"review-team", "quality-team", "commit-team", "feature-team"}


def check_teams(all_skill_names: set) -> tuple[int, int]:
    """
    plugins/*/plugin.json の teams: フィールドを検証する。
    - 登録されたスキルが実際に存在するか
    - チーム名が KNOWN_TEAMS に含まれるか
    - plugin.json に teams: フィールドがあるか
    Returns (errors, warnings)
    """
    errors = 0
    warnings = 0

    if not PLUGINS_DIR.exists():
        return errors, warnings

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        pjson = plugin_dir / "plugin.json"
        if not pjson.exists():
            warn(f"[{plugin_dir.name}] plugin.json が存在しない")
            warnings += 1
            continue

        try:
            data = json.loads(pjson.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"[{plugin_dir.name}] plugin.json が不正な JSON: {e}")
            errors += 1
            continue

        if "teams" not in data:
            warn(f"[{plugin_dir.name}] plugin.json に teams: フィールドがない — Agent Teams に参加しない")
            warnings += 1
            continue

        teams = data["teams"]
        for team_name, members in teams.items():
            # 未知のチーム名チェック
            if team_name not in KNOWN_TEAMS:
                warn(f"[{plugin_dir.name}] teams.{team_name} — 未定義のチーム名 (既知: {', '.join(sorted(KNOWN_TEAMS))})")
                warnings += 1
            # メンバーの存在チェック
            for skill in members:
                if skill not in all_skill_names:
                    err(f"[{plugin_dir.name}] teams.{team_name}: '{skill}' — plugins/ に存在しないスキルを参照")
                    errors += 1

    return errors, warnings


def _build_deps() -> dict[str, list[str]]:
    """requires: フィールドから依存グラフを構築 (plugins/ ベース)"""
    deps: dict[str, list[str]] = {}
    for skill_dir in collect_all_skill_dirs():
        meta_md  = skill_dir / "metadata.md"
        skill_md = skill_dir / "SKILL.md"
        source = meta_md if meta_md.exists() else (skill_md if skill_md.exists() else None)
        if source is None:
            continue
        fm = parse_frontmatter(source)
        name = fm.get("name", skill_dir.name)
        if "requires" in fm:
            raw = fm["requires"].strip("[]")
            deps[name] = [r.strip() for r in raw.split(",") if r.strip()]
        else:
            deps[name] = []
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
def collect_all_skill_dirs() -> list[Path]:
    """plugins/*/skills/* のスキルディレクトリ一覧を返す"""
    skill_dirs: list[Path] = []
    if not PLUGINS_DIR.exists():
        return skill_dirs
    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            continue
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_dirs.append(skill_dir)
    return skill_dirs


def collect_all_agent_files() -> list[Path]:
    """plugins/*/agents/*.md のエージェントファイル一覧を返す"""
    agent_files: list[Path] = []
    if not PLUGINS_DIR.exists():
        return agent_files
    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        agents_dir = plugin_dir / "agents"
        if not agents_dir.exists():
            continue
        for agent_file in sorted(agents_dir.glob("*.md")):
            agent_files.append(agent_file)
    return agent_files


def main() -> int:
    total_errors   = 0
    total_warnings = 0

    print()
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}{BLUE}  skill-agent-factory — Lint チェック{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print()

    # ── スキル一覧を収集 (plugins/ ベース) ───────────────
    skill_dirs      = collect_all_skill_dirs()
    all_skill_names = {d.name for d in skill_dirs}

    # ── Skills チェック ─────────────────────────────────
    print(f"{BOLD}📦 Skills ({len(skill_dirs)} 個){RESET}")
    if skill_dirs:
        for skill_dir in skill_dirs:
            e, w = check_skill(skill_dir, all_skill_names)
            if e == 0 and w == 0:
                ok(skill_dir.name)
            total_errors   += e
            total_warnings += w
    else:
        warn("plugins/*/skills/ にスキルが見つからない")
        total_warnings += 1

    print()

    # ── Agents チェック ─────────────────────────────────
    agent_files = collect_all_agent_files()
    print(f"{BOLD}🤖 Agents ({len(agent_files)} 個){RESET}")
    if not agent_files:
        warn("plugins/*/agents/ にエージェントが見つからない")
        total_warnings += 1
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

    # ── Teams 整合性チェック ─────────────────────────────
    print(f"{BOLD}🤝 Teams 整合性チェック{RESET}")
    teams_errors, teams_warnings = check_teams(all_skill_names)
    total_errors   += teams_errors
    total_warnings += teams_warnings
    if teams_errors == 0 and teams_warnings == 0:
        ok("全 teams エントリの参照が正常")

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
