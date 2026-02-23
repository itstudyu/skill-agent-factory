#!/usr/bin/env python3
"""
# スキル・エージェントファクトリー — レジストリ自動同期スクリプト
# plugins/*/skills/*/metadata.md と plugins/*/agents/*.md をスキャンして
# registry.md と README.md を更新する
# Phase B: plugin 単位スキャンに対応
"""

import json
import re
from datetime import date
from pathlib import Path

# ============================================================
# 設定
# ============================================================
FACTORY_ROOT = Path(__file__).parent.parent
PLUGINS_DIR  = FACTORY_ROOT / "plugins"
REGISTRY_MD  = FACTORY_ROOT / "registry.md"
README_MD    = FACTORY_ROOT / "README.md"
TODAY        = date.today().isoformat()


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
# スキャン (plugins/ 単位)
# ============================================================
def scan_skills() -> list[dict]:
    """plugins/*/skills/*/metadata.md を優先スキャン。なければ SKILL.md にフォールバック"""
    assets = []
    if not PLUGINS_DIR.exists():
        return assets

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            continue
        plugin_name = plugin_dir.name

        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            metadata_md = skill_dir / "metadata.md"
            skill_md    = skill_dir / "SKILL.md"

            if metadata_md.exists():
                fm = parse_frontmatter(metadata_md)
                source = "metadata.md"
            elif skill_md.exists():
                fm = parse_frontmatter(skill_md)
                source = "SKILL.md"
            else:
                continue

            name     = fm.get("name") or skill_dir.name
            category = fm.get("category") or plugin_name
            tags     = fm.get("tags", [])
            desc     = fm.get("use-when") or fm.get("description", "—")
            model    = fm.get("model", "sonnet")
            requires = fm.get("requires", "")

            assets.append({
                "name":        name,
                "type":        "skill",
                "plugin":      plugin_name,
                "category":    category,
                "tags":        tags,
                "model":       model,
                "version":     fm.get("version", "v1.0"),
                "description": desc,
                "file_path":   f"plugins/{plugin_name}/skills/{skill_dir.name}/SKILL.md",
                "meta_path":   f"plugins/{plugin_name}/skills/{skill_dir.name}/{source}",
                "modified":    TODAY,
                "requires":    requires,
            })
    return assets


def scan_agents() -> list[dict]:
    """plugins/*/agents/*.md をスキャン"""
    assets = []
    if not PLUGINS_DIR.exists():
        return assets

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        agents_dir = plugin_dir / "agents"
        if not agents_dir.exists():
            continue
        plugin_name = plugin_dir.name

        for agent_md in sorted(agents_dir.glob("*.md")):
            fm   = parse_frontmatter(agent_md)
            name = fm.get("name") or agent_md.stem

            if fm.get("status") == "deprecated":
                continue

            assets.append({
                "name":        name,
                "type":        "agent",
                "plugin":      plugin_name,
                "category":    plugin_name,
                "tags":        fm.get("tags", []),
                "model":       fm.get("model", "sonnet"),
                "version":     fm.get("version", "v1.0"),
                "description": fm.get("description", "—"),
                "file_path":   f"plugins/{plugin_name}/agents/{agent_md.name}",
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
        "| Name | Type | Plugin | Model | Tags | Version | Description | File Path | Last Modified |\n"
        "|------|------|--------|-------|------|---------|-------------|-----------|---------------|\n"
    )
    rows = []
    for a in assets:
        desc = a["description"].replace("|", "\\|")
        if len(desc) > 100:
            desc = desc[:97] + "..."
        tags_str = fmt_tags(a.get("tags", []))
        rows.append(
            f"| {a['name']} | {a['type']} | {a.get('plugin','—')} | {a.get('model','sonnet')} "
            f"| {tags_str} | {a['version']} "
            f"| {desc} | {a['file_path']} | {a['modified']} |"
        )
    return header + "\n".join(rows)


def build_statistics(assets: list[dict]) -> str:
    skills = [a for a in assets if a["type"] == "skill"]
    agents = [a for a in assets if a["type"] == "agent"]

    plugin_map: dict[str, list[str]] = {}
    for s in skills:
        plugin_map.setdefault(s.get("plugin", "—"), []).append(s["name"])

    skill_lines = []
    for plugin, names in sorted(plugin_map.items()):
        skill_lines.append(f"  - plugin/{plugin} ({len(names)}): {', '.join(names)}")

    agent_names = ", ".join(a["name"] for a in agents)
    plugin_count = len(list(PLUGINS_DIR.iterdir())) if PLUGINS_DIR.exists() else 0

    lines = [
        f"- **Total assets**: {len(assets)}",
        f"- **Skills**: {len(skills)}",
    ] + skill_lines + [
        f"- **Agents**: {len(agents)} ({agent_names})",
        f"- **Plugins**: {plugin_count} (devops, figma, project)",
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

    plugin_map: dict[str, list[dict]] = {}
    for s in skills:
        plugin_map.setdefault(s.get("plugin", "general"), []).append(s)

    skill_sections = []
    for plugin, items in sorted(plugin_map.items()):
        header = (
            f"### {plugin.capitalize()} Plugin Skills\n\n"
            f"| Skill | Model | Tags | Purpose |\n"
            f"|-------|-------|------|---------|"
        )
        rows = [
            f"| `{i['name']}` | {i.get('model','sonnet')} | {fmt_tags(i.get('tags',[]))} | {i['description'][:80]} |"
            for i in items
        ]
        skill_sections.append(header + "\n" + "\n".join(rows))

    skills_block = "\n\n".join(skill_sections)

    agent_header = "### Agents\n\n| Agent | Plugin | Model | Purpose |\n|-------|--------|-------|---------|"
    agent_rows = [
        f"| `{a['name']}` | {a.get('plugin','—')} | {a.get('model','sonnet')} | {a['description'][:80]} |"
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
# README Agent Teams セクション自動更新
# ============================================================
TEAM_EXECUTION = {
    "review-team":  "**Parallel**",
    "quality-team": "**Sequential**",
    "commit-team":  "**Sequential**",
    "feature-team": "**Gated**",
}


def build_teams_table() -> str:
    """全 plugin.json の teams: を集約して Markdown テーブルを生成"""
    # チームごとにメンバーを集約
    team_members: dict[str, list[str]] = {}
    if PLUGINS_DIR.exists():
        for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
            if not plugin_dir.is_dir():
                continue
            pjson = plugin_dir / "plugin.json"
            if not pjson.exists():
                continue
            try:
                data = json.loads(pjson.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            for team_name, members in data.get("teams", {}).items():
                team_members.setdefault(team_name, []).extend(members)

    if not team_members:
        return "| Team | Execution | Members |\n|------|-----------|---------|"

    header = "| Team | Execution | Members |\n|------|-----------|---------|"
    rows = []
    for team in sorted(team_members.keys()):
        members = team_members[team]
        exec_style = TEAM_EXECUTION.get(team, "—")
        members_str = ", ".join(members) if members else "—"
        rows.append(f"| `{team}` | {exec_style} | {members_str} |")

    return header + "\n" + "\n".join(rows)


def update_readme_teams(text: str) -> str:
    """README の TEAMS_TABLE_START ~ END ブロックを更新"""
    table = build_teams_table()
    return re.sub(
        r"(<!-- TEAMS_TABLE_START -->).*?(<!-- TEAMS_TABLE_END -->)",
        rf"\1\n{table}\n\2",
        text,
        flags=re.DOTALL,
    )


# ============================================================
# エントリポイント
# ============================================================
def main():
    print(f"🔍 スキャン開始: {FACTORY_ROOT}")
    print(f"   Plugin 単位スキャン (Phase B)")

    skills = scan_skills()
    agents = scan_agents()
    all_assets = skills + agents

    meta_count     = sum(1 for s in skills if "metadata.md" in s.get("meta_path", ""))
    fallback_count = len(skills) - meta_count

    print(f"   スキル: {len(skills)} 件 (metadata.md: {meta_count}, SKILL.md fallback: {fallback_count})")
    print(f"   エージェント: {len(agents)} 件")

    update_registry(all_assets)
    update_readme(all_assets)

    # Agent Teams テーブル更新
    readme_text = README_MD.read_text(encoding="utf-8")
    readme_text = update_readme_teams(readme_text)
    README_MD.write_text(readme_text, encoding="utf-8")
    print("✅ README.md Teams テーブル更新完了")

    print("\n✨ 同期完了!")

    for a in all_assets:
        if a["description"] == "—":
            print(f"⚠️  description/use-when 未設定: {a['file_path']}")
        if a["type"] == "skill" and not a.get("tags"):
            print(f"⚠️  tags 未設定: {a['file_path']}")


if __name__ == "__main__":
    main()
