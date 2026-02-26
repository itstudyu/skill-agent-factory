# API Reference — エンドポイント契約書

> **FOR AI**: フロントエンドから呼び出す address / request / response の一覧。
> 各処理モジュールの実装詳細は `{category}-api/` フォルダを参照。

---

## 処理モジュール一覧

| モジュール | DataAccess メソッド | Callback | 概要 | ドキュメント |
|-----------|--------------------|---------|----|-------------|
| data-api | `getDataAPI()` `putDataAPI()` `deleteDataAPI()` | CallBack, CallBackGet, CallBackPut, CallBackDelete | CRUD 操作 (最も頻用) | `data-api/` (README + 8ファイル) |
| filter-api | `getFilterAPI()` | CallBackGet | フィルタリング・検索 | `filter-api/` |
| insert-api | `postInsertAPI()` | CallBack | 一括データ挿入 | `insert-api/` |
| employee-api | `getEmployeeAPI()` `putEmployeeAPI()` | CallBackGet, CallBackPut | 社員番号管理・バリデーション | `employee-api/` |
| organ-api | `getOrganAPI()` | CallBackGet | 組織・役職情報取得 | `organ-api/` |
| schema-api | `getSchemaAPI()` | CallBack | テーブルスキーマ参照 | `schema-api/` |
| notice-api | `postNoticeAPI()` | CallBack | 通知配信 (メール + SMS) | `notice-api/` |
| sms-api | `postSMSAPI()` | CallBack | SMS 送信 | `sms-api/` |
| file-api | `getFileIdAPI()` `getFileAPI()` `putFileAPIPersist()` `deleteFileAPI()` | CallBackGet, CallBack | ファイル操作 (upload/download/persist/delete) | `file-api/` |
| env-api | `getEnvAPI()` | CallBackEnv | 環境設定・モジュール設定 | `env-api/` |
| async-api | `postAsyncAPI()` `getAsyncAPI()` | CallBackAsync | 非同期ジョブ (POST で開始, GET で状態確認) | `async-api/` |

---

## 使い方

### スキルからの参照フロー

```
1. このファイルで対象 API のメソッド・Callback を確認
2. 該当フォルダの 00-quick-start.md で基本パターンを確認
3. 01-*-template.md で実装テンプレートをコピー
```

### 新しいエンドポイント追加時

このファイルの上記テーブルに行を追加し、該当フォルダのテンプレートに実装例を追記する。

---

## 共通パターン

### リクエスト基本構造
```
DataAccess メソッド(パラメータ文字列, CallBack インスタンス)
```
- パラメータ: `"TABLE_NAME/{platformID}/{key}"` 形式
- クエリパラメータ: `"?_lang=ja&_limit=100"` を末尾に付与

### レスポンス共通フィールド
- `code` — HTTP ステータスコード (200, 404, 500 等)
- `responseData` — JsonObject のレスポンス本体
- `th` — 例外 (正常時は null)

### Callback パターン
| Callback | 用途 |
|---------|------|
| `CallBack` | 汎用 (code, JsonObject, Throwable) |
| `CallBackGet` | GET 応答用 (code, JsonObject, Throwable) |
| `CallBackPut` | PUT 応答用 (code, JsonObject, Throwable) |
| `CallBackDelete` | DELETE 応答用 (code, JsonObject, Throwable) |
| `CallBackEnv` | 環境設定 API 専用 |
| `CallBackAsync` | 非同期ジョブ API 専用 |

---

*Last updated: 2026-02-26*
