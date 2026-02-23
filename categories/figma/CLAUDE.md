# Figma Category — Context & Conventions

> Figma MCP を使ったデザイン → コード変換の標準ワークフロー。
> このカテゴリのスキルは既存の Figma スキル群と連携して動作する。

---

## 前提条件

以下の MCP が設定済みであること:
- **Figma MCP** — Figmaデザインの読み取り用 (全スキルで使用)
- **Talk to Figma MCP** — Figmaデザインの作成・変更用 (`figma-designer` agentのみ)

---

## スキル一覧 (このリポジトリで管理)

全スキルおよびエージェントは `plugins/figma/` に格納済み。
`install.sh` を実行すると `~/.claude/skills/` にシムリンクが作成される。

### スキル

| スキル | 役割 | 使用タイミング |
|--------|------|--------------|
| `figma-project-context` | プロジェクト構造を解析し `context.md` 生成 | **最初に必ず実行** |
| `figma-design-token-extractor` | 色・フォント・余白・影などのデザイントークンを抽出 → `tokens.css` 等 | コーディング前 |
| `figma-framework-figma-mapper` | フレームワーク ↔ Figma コンポーネントのマッピング表生成 | コーディング前 |
| `figma-design-analyzer` | Figmaデザインを読んで `implementation-blueprint.md` 生成 | コーディング前の設計 |
| `figma-component-inventory` | Figmaファイル内の全コンポーネントをスキャン・カタログ化 | 大規模変換時/ギャップ分析 |
| `figma-responsive-validator` | 生成コードのレスポンシブ対応を検証 (Mobile/Tablet/Desktop) | コーディング後 |
| `figma-code-sync` | マッピングと実装の一致を検証 → 同期スコア (0–100%) | コーディング後 |

### エージェント

| エージェント | モデル | 役割 |
|------------|--------|------|
| `figma-to-code` | opus | Figma → コード全工程自動化 (プリフライト → 生成 → 検証 → コミット) |
| `figma-designer` | opus | Talk to Figma MCP でデザイン新規作成 (デザインシステム準拠) |

---

## 標準ワークフロー (Figma → Code)

```
[1] figma-project-context      ← プロジェクト構造・フレームワーク・規約を把握
         ↓
[2] figma-design-token-extractor ← デザイントークン抽出 → tokens.ts / tailwind.config
         ↓
[3] figma-framework-figma-mapper ← コンポーネントマッピング表作成
         ↓
[4] figma-design-analyzer      ← 実装blueprint生成 (スクリーンショット + 構造分析)
         ↓
[5] コード生成 (devops-pipeline経由)
         ↓
[6] figma-code-sync            ← マッピングと実装の一致検証 ← NEW
         ↓
[7] figma-responsive-validator ← レスポンシブ検証
         ↓
[8] devops-pipeline 残ステップ (Step 2〜8)
```

---

## devops-pipeline との統合

フロントエンド開発リクエストに Figma が含まれる場合:
- **Step 1 (Requirements)** → Figma URLまたはMCPが利用可能か確認
- **Step 5 (Frontend Review)** → `figma-code-sync` を使って検証 (スクリーンショット比較ではなく正確な値で比較)

---

## 使い分け判断

| 状況 | 使うもの |
|------|---------|
| Figma URLがあり、コードを生成したい | `figma-to-code` agent (全自動) |
| デザイントークンだけ欲しい | `figma-design-token-extractor` |
| 実装が正しいか確認したい | `figma-code-sync` |
| 新しいデザインをFigmaで作りたい | `figma-designer` agent |
| スクリーンショットしかない | `devops-frontend-review` (Figma MCPなし) |

---

## Related Docs
- `../../_docs/skills.md` — Skill format reference
- `../../_docs/sub-agents.md` — Agent format reference
- `../../registry.md` — All assets registry

*Category: figma | Last updated: 2026-02-21*
