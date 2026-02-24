# Vert.x API Reference

このディレクトリには、各 EventBus エンドポイントの API リファレンスが格納されています。

## ファイル構成

| ファイル | 内容 |
|---------|------|
| `data-api.md`   | データ取得・更新系 API (CRUD) |
| `filter-api.md` | 検索・フィルタリング系 API |
| `notice-api.md` | 通知・アナウンス系 API |
| `env-api.md`    | 環境設定・マスタデータ系 API |
| `async-api.md`  | 非同期処理・バックグラウンドジョブ系 API |

## 記述ルール

各ファイルは以下の形式で記述してください。

```markdown
## エンドポイント名

- **Address**: `module.action.resource`
- **Request**: `{ field: type, ... }`
- **Response**: `{ field: type, ... }`
- **説明**: 何をするエンドポイントか
- **Verticle**: 対応する Verticle クラス名
```

## 現在のステータス

> 🚧 **準備中** — API ドキュメントは順次追加予定です。
> 各 .md ファイルに実際のエンドポイント情報を追加してください。
