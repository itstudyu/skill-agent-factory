# Multi-Model Strategy

> **モデル選択戦略リファレンス。**
> タスクタイプ別の理想モデルと Claude フォールバックを定義する。
> 現状 Claude Code は Claude モデルのみネイティブ対応。
> Gemini / GPT-4o を使う場合は MCP サーバー経由が必要（将来対応）。

---

## モデル選択マトリクス

| タスクタイプ | 理想モデル | 理由 | 現在の実装 |
|------------|-----------|------|----------|
| **画像 → コード** | Gemini 2.0 Flash / GPT-4o | 画像理解の精度が高い | Claude Sonnet (fallback) |
| **コード生成・レビュー** | Claude Sonnet | コード品質・指示追従が強い | ✅ Claude Sonnet (使用中) |
| **文書作成** | Claude Opus / GPT-4o | 長文生成・構成力が高い | ✅ Claude Opus (使用中) |
| **データ分析** | Gemini / Claude Sonnet | 長コンテキスト処理が強い | ✅ Claude Sonnet (使用中) |
| **高速・軽量タスク** | Claude Haiku | コスト・レイテンシ優先 | ✅ Claude Haiku (使用中) |

---

## タスク別ガイドライン

### 画像 → コード

**理想:** Gemini 2.0 Flash または GPT-4o Vision

理由:
- スクリーンショット・Figmaエクスポート画像を直接解析
- ピクセル単位のレイアウト読み取りが得意
- 視覚的な階層構造をコードに変換する精度が高い

**現在の Claude fallback:**
```
figma-to-code agent (opus) + figma-design-analyzer skill
→ Figma MCP で構造解析 + スクリーンショット取得で補完
```

**将来の実装方針:**
```
MCP サーバー経由で Gemini Vision API を呼び出し
→ 画像解析結果を受け取り → Claude でコード生成
```

---

### コード生成・レビュー

**推奨:** Claude Sonnet ✅ (現在使用中)

理由:
- コーディング規約への追従精度が高い
- 長いコンテキスト（コードベース全体）でも安定
- 日本語コメントの品質が高い

使用しているエージェント/スキル:
- `devops-pipeline` (sonnet)
- `skill-router` (sonnet)
- `devops-code-review`, `devops-arch-review` など全 devops スキル

---

### 文書作成

**推奨:** Claude Opus / Claude Sonnet ✅ (現在使用中)

理由:
- 長文の構成力・論理的な説明が得意
- 技術文書・API ドキュメントの品質が高い

使用しているエージェント:
- `figma-to-code` (opus) — 実装ブループリント生成
- 文書生成タスク全般

---

### データ分析

**推奨:** Claude Sonnet または Gemini

理由:
- Gemini: 100万トークン超のコンテキストウィンドウ（大規模ログ・CSV 解析に有利）
- Claude Sonnet: 精度と速度のバランスが良い

**現在の Claude fallback:** Claude Sonnet

---

### 高速・軽量タスク

**推奨:** Claude Haiku ✅

理由:
- レイテンシが最小
- コストが最小
- 単純なルーティング・分類・フォーマット変換に最適

---

## フォールバック戦略

```
理想モデルが利用不可の場合 → Claude Sonnet を使用
Gemini / GPT-4o が必要な場合 → MCP サーバー経由で将来対応
画像解析が必要な場合 → Figma MCP + スクリーンショット取得で代替
```

---

## 将来ロードマップ

| フェーズ | 内容 | 優先度 |
|---------|------|-------|
| Phase 1 | Gemini Vision MCP サーバー構築 — 画像→コード精度向上 | 高 |
| Phase 2 | GPT-4o MCP サーバー構築 — 文書生成の選択肢追加 | 中 |
| Phase 3 | skill-router にモデル選択ロジック追加 — タスク→モデル自動振り分け | 中 |
| Phase 4 | コスト最適化 — タスク複雑度に応じて Haiku / Sonnet / Opus を動的選択 | 低 |

---

## skill-router との連携（将来）

Phase 3 実装後のフロー:

```
User Request
    ↓
skill-router (スキル選択)
    ↓
model-selector (タスクタイプ → モデル決定)
    ├─ 画像あり → Gemini Vision MCP
    ├─ コード → Claude Sonnet
    ├─ 文書 → Claude Opus
    └─ 軽量 → Claude Haiku
    ↓
選択されたモデルで実行
```

---

*Reference: model-strategy | Version: v1.0 | Last updated: 2026-02-22*
