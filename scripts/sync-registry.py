#!/usr/bin/env python3
"""
# スキル・エージェントファクトリー — レジストリ自動同期スクリプト
# skills/*/metadata.md と agents/*.md をスキャンして registry.md と README.md を更新する
# Phase A: metadata.md ベースのルーティングに対応
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
        if key and val:
            result[key] = val

    # description の継続行を結合
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

    # tags: [a, b, c] パース
    if "tags" in result:
        raw = result["tags"].strip("[]")
        result["tags"] = [t.strip() for t in raw.split(",") if t.strip()]
    else:
        result["tags"] = []

    return result


# ============================================================
# スキャン
# ============================================================
def scan_skills() -> list[dict]:
    """skills/*/metadata.md を優先スキャン。なければ SKILL.md にフォールバック"""
    assets = []
    if not SKILLS_DIR.exists():
        return assets

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        metadata_md = skill_dir / "metadata.md"
        skill_md    = skill_dir / "SKILL.md"

        # metadata.md 優先
        if metadata_md.exists():
            fm = parse_frontmatter(metadata_md)
            source = "metadata.md"
        elif skill_md.exists():
            fm = parse_frontmatter(skill_md)
            source = "SKILL.md"
        else:
            continue

        name     = fm.get("name") or skill_dir.name
        category = fm.get("category") or (name.split("-")[0] if "-" in name else "general")
        tags     = fm.get("tags", [])
        desc     = fm.get("use-when") or fm.get("description", "—")
        model    = fm.get("model", "sonnet")
        requires = fm.get("requires", "")

        assets.append({
            "name":        name,
            "type":        "skill",
            "category":    category,
            "tags":        tags,
            "model":       model,
            "version":     fm.get("version", "v1.0"),
            "description": desc,
            "file_path":   f"skills/{skill_dir.name}/SKILL.md",
            "meta_path":   f"skills/{skill_dir.name}/{source}",
            "modified":    TODAY,
            "requires":    requires,
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
        name     = fm.get("name") or agent_md.stem
        category = name.split("-")[0] if "-" in name else "general"

        assets.append({
            "name":        name,
            "type":        "agent",
            "category":    category,
            "tags":        fm.get("tags", []),
            "model":       fm.get("model", "sonnet"),
            "version":     fm.get("version", "v1.0"),
            "description": fm.get("description", "—"),
            "file_path":   f"agents/{agent_md.name}",
            "modified":    TODAY,
            "requires":    fm.get("requires", ""),
        })
    return assets


# ============================================================
# registry.md 更新
# ============================================================
def fmt_tags(tags: list[str]) -> str:
    if not tags:
        return "—"
    return ", ".join(f"`{t}`" for t in tags)


def build_registry_table(assets: list[dict]) -> str:
    header = (
        "| Name | Type | Category | Model | Tags | Version | Description | File Path | Last Modified |\n"
        "|------|------|----------|-------|------|---------|-------------|-----------|---------------|\n"
    )
    rows = []
    for a in assets:
        desc = a["description"].replace("|", "\\|")
        if len(desc) > 100:
            desc = desc[:97] + "..."
        tags_str = fmt_tags(a.get("tags", []))
        rows.append(
            f"| {a['name']} | {a['type']} | {a['category']} | {a.get('model','sonnet')} "
            f"| {tags_str} | {a['version']} "
            f"| {desc} | {a['file_path']} | {a['modified']} |"
        )
    return header + "\n".join(rows)


def build_statistics(assets: list[dict]) -> str:
    skills = [a for a in assets if a["type"] == "skill"]
    agents = [a for a in assets if a["type"] == "agent"]

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

    table_str = build_registry_table(assets)
    text = re.sub(
        r"(## Registry Table\n\n).*?(\n---)",
        rf"\g<1>{table_str}\n\2",
        text,
        flags=re.DOTALL,
    )

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

    cat_map: dict[str, list[dict]] = {}
    for s in skills:
        cat_map.setdefault(s["category"], []).append(s)

    skill_sections = []
    for cat, items in sorted(cat_map.items()):
        header = f"### {cat.capitalize()} Skills\n\n| Skill | Model | Tags | Purpose |\n|-------|-------|------|---------|"
        rows = [
            f"| `{i['name']}` | {i.get('model','sonnet')} | {fmt_tags(i.get('tags',[]))} | {i['description'][:80]} |"
            for i in items
        ]
        skill_sections.append(header + "\n" + "\n".join(rows))

    skills_block = "\n\n".join(skill_sections)

    agent_header = "### Agents\n\n| Agent | Model | Purpose |\n|-------|-------|---------|"
    agent_rows = [
        f"| `{a['name']}` | {a.get('model','sonnet')} | {a['description'][:80]} |"
        for a in agents
    ]
    agents_block = agent_header + "\n" + "\n".join(agent_rows)

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
    print(f"   metadata.md 優先スキャン (Phase A)")

    skills = scan_skills()
    agents = scan_agents()
    all_assets = skills + agents

    # ソース統計
    meta_count = sum(1 for s in skills if "metadata.md" in s.get("meta_path", ""))
    fallback_count = len(skills) - meta_count

    print(f"   スキル: {len(skills)} 件 (metadata.md: {meta_count}, SKILL.md fallback: {fallback_count})")
    print(f"   エージェント: {len(agents)} 件")

    update_registry(all_assets)
    update_readme(all_assets)

    print("\n✨ 同期完了!")

    # 整合性チェック
    for a in all_assets:
        if a["description"] == "—":
            print(f"⚠️  description/use-when 未設定: {a['file_path']}")
        if a["type"] == "skill" and not a.get("tags"):
            print(f"⚠️  tags 未設定: {a['file_path']}")


if __name__ == "__main__":
    main()
