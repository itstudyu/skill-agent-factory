# HTTP ステータスコード リファレンス

> `HttpConstants` クラスに定義されたステータスコードの完全一覧。

---

## 成功系

| コード | 定数 | 意味 | 対応コールバックメソッド |
|-------|------|------|---------------------|
| 200 | `HTTP_CODE_SUCCESS_200` | 成功（データあり） | `ok()`, `success()`, `callBack(200, ...)` |
| 201 | `HTTP_CODE_SUCCESS_201` | 作成/更新成功 | `created()`, `callBack(201, ...)` |
| 202 | `HTTP_CODE_SUCCESS_202` | 受付完了 | `callBack(202, ...)` |
| 204 | `HTTP_CODE_SUCCESS_204` | 成功（データなし） | `noContent()`, `callBack(204, ...)` |

---

## クライアントエラー系

| コード | 定数 | 意味 | 対応コールバックメソッド |
|-------|------|------|---------------------|
| 404 | `HTTP_STATUS_CODE_NOT_FOUND` | リソースが見つからない | `fail(404, ...)` |
| 40406 | — | 主キーの型が一致しない | `fail(40406, ...)` |
| 40407 | — | インデックスプロパティの型不一致 | `fail(40407, ...)` |
| 40410 | `HTTP_STATUS_CODE_REQUESTED_RESOURCE_DOES_NOT_EXIST` | リソース定義が存在しない | `resourceDoesNotExist()` |
| 40423 | — | リソース定義が見つからない | `fail(40423, ...)` |
| 409 | `HTTP_STATUS_CODE_CONFLICT` | 競合（楽観ロック等） | `fail(409, ...)` |
| 40909 | `HTTP_STATUS_CODE_RESOURCE_CHANGED` | 楽観ロック失敗（他者更新済み） | `resourceAlreadyChanged()` |
| 40910 | — | DB 整合性制約違反 | `databaseIntegrityConstraintViolation()` |
| 40926 | `HTTP_STATUS_CODE_EXCLUSIVE_CONTROL` | 排他制御エラー | `exclusive()` |

---

## サーバーエラー系

| コード | 定数 | 意味 | 対応コールバックメソッド |
|-------|------|------|---------------------|
| 500 | `HTTP_CODE_ERROR` | サーバー内部エラー | `fail(500, ...)` |
| 50018 | — | リソース定義取得不能 | `fail(50018, ...)` |

---

## 特殊

| コード | 定数 | 意味 | 対応コールバックメソッド |
|-------|------|------|---------------------|
| 900 | `HTTP_STATUS_CODE_TIMEOUT` | タイムアウト | EventBus 送信失敗時に自動設定 |

---

## ステータス文字列

| 定数 | 値 |
|------|-----|
| `HTTP_STATUS_SUCCESS` | `"success"` |
| `HTTP_STATUS_ERROR` | `"error"` |
| `HTTP_STATUS_FAIL` | `"fail"` |
| `HTTP_MESSAGE_SUCCESSFUL` | `"successful"` |
| `HTTP_MESSAGE_ERROR` | `"INTERNAL SERVER ERROR"` |
