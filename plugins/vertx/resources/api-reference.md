# Vert.x EventBus API Reference

> このファイルは全エンドポイントの契約書です。
> フロントエンドはここを見て address / request / response を確認してから呼び出しを実装してください。

---

## 記述形式

```markdown
## エンドポイント名

- **Address**: `module.action.resource`
- **Request**: `{ field: type, ... }`
- **Response**: `{ status: "ok"|"error", ... }`
- **説明**: 何をするか
- **処理モジュール**: data-api / filter-api / notice-api / env-api / async-api
```

## 処理モジュール一覧

| ファイル | 担当 |
|---------|------|
| `data-api.md` | データ取得・登録・更新・削除 |
| `filter-api.md` | 検索・フィルタリング |
| `notice-api.md` | 通知・アナウンス送信 |
| `env-api.md` | 環境設定・マスタデータ |
| `async-api.md` | 非同期処理・バックグラウンドジョブ |
| `email-api.md` | メール送信・テンプレート管理 *(追加予定)* |

---

## エンドポイント一覧

> 🚧 **準備中** — 実際のエンドポイントをここに追加してください。

<!-- ここにエンドポイントを追加 -->
<!-- 例:
## ユーザー一覧取得

- **Address**: `user.get.list`
- **Request**: `{ page: number, size: number }`
- **Response**: `{ status: "ok", data: [{ id, name, ... }], total: number }`
- **説明**: ページネーション付きでユーザー一覧を取得する
- **処理モジュール**: data-api
-->
