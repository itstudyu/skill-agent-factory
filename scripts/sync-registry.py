#!/usr/bin/env python3
"""
# スキル・エージェントファクトリー — レジストリ自動同期スクリプト
# skills/ と agents/ を自動スキャンして registry.md と README.md を更新する
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

# ============================================================
# 設定
# ============================================================
FACTORY_ROOT = Path(__file__).parent.parent
SKILLS_DIR   = FACTORY_ROOT / "skills"
AGENTS_DIR   = FACTORY_ROOT / "agents"
REGISTRY_MD  = FACTORY_ROOT / "registry.md"
README_MD    = FACTORY_ROOT / "README.md"
TODAY        = date.today().isoformat()

# registry.md に載せない内部エージェント
SKIP_AGENTS = set()


# ============================================================
# フロントマターパーサー
# ============================================================
def parse_frontmatter(filepath: Path) -> dict:
    """YAML フロントマター (---..---) をパースして dict を返す"""
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
        val = val.strip().strip('"').strip("'")
        # 複数行 description (インデントされた継続行) をまとめる
        if key and val:
            result[key] = val

    # description の継続行を結合
    desc_lines = []
    in_desc = False
    for line in fm_block.splitlines():
        if line.startswith("description:"):
            in_desc = True
            val = line.partition(":")[2].strip().strip('"').strip("'")
            if val:
                desc_lines.append(val)
        elif in_desc and line.startswith("  "):
            desc_lines.append(line.strip())
        else:
            if in_desc:
                in_desc = False

    if desc_lines:
        result["description"] = " ".join(desc_lines)

    return result


# ============================================================
# スキャン
# ============================================================
def scan_skills() -> list[dict]:
    assets = []
    if not SKILLS_DIR.exists():
        return assets

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        fm = parse_frontmatter(skill_md)
        name = fm.get("name") or skill_dir.name
        # カテゴリはスキル名のプレフィックスから推定
        category = name.split("-")[0] if "-" in name else "general"
        requires = fm.get("requires", "")

        # tags: [a, b, c] → "a, b, c"
        raw_tags = fm.get("tags", "")
        tags_str = raw_tags.strip("[]").replace(", ", ",")
        tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]

        assets.append({
            "name":        name,
            "type":        "skill",
            "category":    category,
            "version":     fm.get("version", "v1.0"),
            "description": fm.get("description", "—"),
            "file_path":   f"skills/{skill_dir.name}/SKILL.md",
            "modified":    TODAY,
            "requires":    requires,
            "tags":        tags_list,
        })
    return assets


def scan_agents() -> list[dict]:
    assets = []
    if not AGENTS_DIR.exists():
        return assets

    for agent_md in sorted(AGENTS_DIR.glob("*.md")):
        if agent_md.name in SKIP_AGENTS:
            continue

        fm = parse_frontmatter(agent_md)
        name = fm.get("name") or agent_md.stem
        category = name.split("-")[0] if "-" in name else "general"

        assets.append({
            "name":        name,
            "type":        "agent",
            "category":    category,
            "version":     fm.get("version", "v1.0"),
            "description": fm.get("description", "—"),
            "file_path":   f"agents/{agent_md.name}",
            "modified":    TODAY,
            "model":       fm.get("model", "sonnet"),
            "requires":    fm.get("requires", ""),
            "tags":        [],
        })
    return assets


# ============================================================
# registry.md 更新
# ============================================================
def build_registry_table(assets: list[dict]) -> str:
    header = (
        "| Name | Type | Category | Tags | Version | Description | File Path | Last Modified |\n"
        "|------|------|----------|------|---------|-------------|-----------|---------------|\n"
    )
    rows = []
    for a in assets:
        desc = a["description"].replace("|", "\\|")
        if len(desc) > 100:
            desc = desc[:97] + "..."
        tags_cell = ", ".join(f"`{t}`" for t in a.get("tags", [])) or "—"
        rows.append(
            f"| {a['name']} | {a['type']} | {a['category']} | {tags_cell} | {a['version']} "
            f"| {desc} | {a['file_path']} | {a['modified']} |"
        )
    return header + "\n".join(rows)


def build_statistics(assets: list[dict]) -> str:
    skills = [a for a in assets if a["type"] == "skill"]
    agents = [a for a in assets if a["type"] == "agent"]

    # カテゴリ別スキル集計
    cat_map: dict[str, list[str]] = {}
    for s in skills:
        cat_map.setdefault(s["category"], []).append(s["name"])

    skill_lines = []
    for cat, names in sorted(cat_map.items()):
        skill_lines.append(f"  - {cat.capitalize()} ({len(names)}): {', '.join(names)}")

    agent_names = ", ".join(a["name"] for a in agents)

    lines = [
        f"- **Total assets**: {len(assets)}",
        f"- **Skills**: {len(skills)}",
    ] + skill_lines + [
        f"- **Agents**: {len(agents)} ({agent_names})",
        "- **Plugins**: 0",
        "- **Hooks**: 0",
        "- **MCP Servers**: 0",
        "- **Output Styles**: 0",
        "",
        f"*Last updated: {TODAY}*",
    ]
    return "\n".join(lines)


def update_registry(assets: list[dict]):
    text = REGISTRY_MD.read_text(encoding="utf-8")

    # Registry Table セクションを置換
    table_str = build_registry_table(assets)
    text = re.sub(
        r"(## Registry Table\n\n).*?(\n---)",
        rf"\g<1>{table_str}\n\2",
        text,
        flags=re.DOTALL,
    )

    # Statistics セクションを置換
    stats_str = build_statistics(assets)
    text = re.sub(
        r"(## Statistics\n\n).*",
        rf"\g<1>{stats_str}",
        text,
        flags=re.DOTALL,
    )

    REGISTRY_MD.write_text(text, encoding="utf-8")
    print(f"✅ registry.md 更新完了 ({len(assets)} 件)")


# ============================================================
# README.md 更新
# ============================================================
def update_readme(assets: list[dict]):
    text = README_MD.read_text(encoding="utf-8")

    skills = [a for a in assets if a["type"] == "skill"]
    agents = [a for a in assets if a["type"] == "agent"]

    # カテゴリ別スキルテーブルを再構築
    cat_map: dict[str, list[dict]] = {}
    for s in skills:
        cat_map.setdefault(s["category"], []).append(s)

    skill_sections = []
    for cat, items in sorted(cat_map.items()):
        header = f"### {cat.capitalize()} Skills\n\n| Skill | Purpose |\n|-------|---------|"
        rows = [f"| `{i['name']}` | {i['description'][:80]} |" for i in items]
        skill_sections.append(header + "\n" + "\n".join(rows))

    skills_block = "\n\n".join(skill_sections)

    # Agents テーブル
    agent_header = "### Agents\n\n| Agent | Model | Purpose |\n|-------|-------|---------|"
    agent_rows = [
        f"| `{a['name']}` | {a.get('model','sonnet')} | {a['description'][:80]} |"
        for a in agents
    ]
    agents_block = agent_header + "\n" + "\n".join(agent_rows)

    # README の "## Current Skills & Agents" セクションを置換
    replacement = f"## Current Skills & Agents\n\n{skills_block}\n\n{agents_block}"
    text = re.sub(
        r"## Current Skills & Agents.*?(?=\n## )",
        replacement + "\n\n",
        text,
        flags=re.DOTALL,
    )

    README_MD.write_text(text, encoding="utf-8")
    print(f"✅ README.md 更新完了")


# ============================================================
# エントリポイント
# ============================================================
def main():
    print(f"🔍 スキャン開始: {FACTORY_ROOT}")

    skills = scan_skills()
    agents = scan_agents()
    all_assets = skills + agents

    print(f"   スキル: {len(skills)} 件")
    print(f"   エージェント: {len(agents)} 件")

    update_registry(all_assets)
    update_readme(all_assets)

    print("\n✨ 同期完了!")

    # 不整合チェック: frontmatter に name がないファイルを警告
    for a in all_assets:
        if a["description"] == "—":
            print(f"⚠️  description 未設定: {a['file_path']}")


if __name__ == "__main__":
    main()
