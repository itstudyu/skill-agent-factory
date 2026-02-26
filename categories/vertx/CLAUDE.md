# Vert.x Category — Context & Conventions

> This CLAUDE.md is auto-read when working inside the `vertx/` directory.
> It provides Vert.x and Java 7 EventBus context for creating skills and agents.

---

## Category Scope

Assets in this category target **Vert.x EventBus backend** tasks:
- Java 7 Verticle の作成・修正
- EventBus ハンドラの登録（匿名内部クラス形式）
- フロントエンドからの EventBus 呼び出し（SockJS + EventBus クライアント）
- 既存 Vert.x リポジトリの構造解析
- API リファレンスの参照・更新

---

## ⚠️ Java 7 制約（全スキル共通）

このカテゴリのすべてのコード生成はJava 7に準拠すること:

| 禁止 | 代替 |
|-----|------|
| ラムダ式 `() -> {}` | 匿名内部クラス |
| `eventBus().consumer()` | `eventBus().registerHandler()` |
| メソッド参照 `Foo::bar` | 匿名内部クラス内で直接実装 |
| ダイヤモンド演算子 `<>` | 型パラメータ明示 |
| try-with-resources | 明示的な finally ブロック |
| Stream API | for ループ・Iterator |

---

## Vert.x Workflow

Vert.x 開発の標準フロー:

| ステップ | スキル | 用途 |
|---------|-------|------|
| 1 | `plugins/vertx/skills/vertx-repo-analyzer/` | 既存構造・アドレス一覧の把握 |
| 2 | `plugins/vertx/skills/vertx-eventbus-register/` | 新しいハンドラの追加 |
| 3 | `plugins/vertx/skills/vertx-api-caller/` | フロントからの呼び出し実装 |

---

## Directory Layout

```
skill-agent-factory/
└── plugins/vertx/
    ├── plugin.json
    ├── resources/
    │   ├── api-reference.md        ← エンドポイント契約書 (address / request / response 一覧)
    │   ├── data-api/               ← データ取得・登録・更新・削除 (README + 8ファイル)
    │   ├── filter-api/             ← 検索・フィルタリング
    │   ├── insert-api/             ← 一括データ挿入
    │   ├── employee-api/           ← 社員情報管理
    │   ├── organ-api/              ← 組織・役職情報
    │   ├── schema-api/             ← テーブルスキーマ参照
    │   ├── notice-api/             ← 通知配信 (メール/SMS)
    │   ├── sms-api/                ← SMS送信
    │   ├── file-api/               ← ファイル操作
    │   ├── env-api/                ← 環境設定・モジュール設定
    │   ├── async-api/              ← 非同期ジョブ
    │   └── image/                  ← ドキュメント用画像
    └── skills/
        ├── vertx-repo-analyzer/    (metadata.md + SKILL.md)
        ├── vertx-eventbus-register/
        └── vertx-api-caller/
```

各処理モジュールフォルダの構成: `00-quick-start.md` (概要・判断ツリー) + `01-*-template.md` (実装テンプレート)。
data-api/ は最も成熟: README.md + GET/PUT/DELETE/chaining/error-handling/status-codes 別に分割。

---

## Conventions

### スキルの実装規則:
- ファイル先頭に日本語サマリーコメント (`// クラス名 — 説明`)
- 各メソッド・ハンドラは 30 行以内（超える場合は private メソッドに分割）
- バリデーションを必ず含める（null チェック、必須項目チェック）
- エラー時は `message.reply()` でエラーレスポンスを返す

### アドレス命名規則:
`{module}.{action}.{resource}`

例: `user.get.list`, `order.create`, `notification.send.all`

### API ドキュメント:
新しいエンドポイントを追加したら以下の 2 箇所に必ず記載する:
- `plugins/vertx/resources/api-reference.md` — エンドポイント契約書 (address / request / response 一覧)
- `plugins/vertx/resources/{category}-api/` — 該当する処理モジュールフォルダのテンプレートに追記

---

## Related Docs
- `../../_docs/skills.md` — Skill format reference
- `../../plugins/vertx/resources/api-reference.md` — エンドポイント契約書 (address / request / response 一覧)
- `../../plugins/vertx/resources/{category}-api/00-quick-start.md` — 各処理モジュールの基本パターン
- `../../registry.md` — All assets registry

*Category: vertx | Last updated: 2026-02-26*
