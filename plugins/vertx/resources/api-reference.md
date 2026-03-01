# Vert.x API リファレンス（マスター）

> AI がコードを生成する際、必ずこのファイルを最初に参照すること。
> 各 API の詳細テンプレートは `{api-name}/` フォルダを参照。

---

## 共通インポート

すべての API 呼び出しに必要な共通インポート:

```java
import org.vertx.java.core.json.JsonObject;
import org.vertx.java.core.json.JsonArray;
import org.vertx.java.platform.Container;
import org.vertx.java.core.Vertx;
import org.vertx.java.core.eventbus.Message;
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.DataAccess;
```

---

## DataAccess インスタンス生成

```java
DataAccess da = new DataAccess(container, vertx);
```

- `container`: Verticle の `Container`（設定・ログ取得用）
- `vertx`: Verticle の `Vertx`（EventBus アクセス用）

---

## 全 API メソッド一覧

### GET 系

| API | DataAccess メソッド | コールバック型 | 詳細 |
|-----|-------------------|-------------|------|
| data-api | `getDataAPI(String param, CallBack cb)` | CallBack | 汎用 GET |
| data-api | `getDataAPI(String param, CallBackGet cb)` | CallBackGet | ok/noContent/fail 分岐 |
| data-api | `getDataAPI(String param, CallBack cb, boolean cache)` | CallBack | キャッシュ付き GET |
| filter-api | `getFilterAPI(String param, CallBack cb)` | CallBack | フィルタ検索 |
| filter-api | `getFilterAPI(String param, CallBackGet cb)` | CallBackGet | フィルタ検索（分岐） |
| schema-api | `getSchemaAPI(String param, CallBack cb)` | CallBack | スキーマ取得 |
| env-api | `getEnvAPI(String param, CallBack cb)` | CallBack | 環境変数取得 |
| env-api | `getEnvAPI(String param, CallBackEnv cb)` | CallBackEnv | 環境変数取得（分岐） |
| file-api | `getFileAPI(String param, CallBack cb)` | CallBack | ファイル取得 |
| file-api | `getFileIdAPI(String param, CallBack cb)` | CallBack | ファイルID発行 |
| file-api | `getFileIdAPI(String param, CallBackGet cb)` | CallBackGet | ファイルID発行（分岐） |
| async-api | `getAsyncAPI(String param, CallBack cb)` | CallBack | 非同期ジョブ状態取得 |
| session-api | `getSessionAPI(String param, CallBack cb)` | CallBack | セッション取得 |
| employee-api | `getEmployeeAPI(String param, CallBackGet cb)` | CallBackGet | 社員情報取得 |
| contact-api | `getContactAPI(String param, CallBackGet cb)` | CallBackGet | 連絡先取得 |
| organ-api | `getOrganAPI(String param, CallBackGet cb)` | CallBackGet | 組織情報取得 |
| sequence-api | `getSequenceAPI(String param, CallBack cb)` | CallBack | 採番取得 |
| SLkey | `getSLkey(String classId, CallBackSLkey cb)` | CallBackSLkey | マスタ取得(TreeMap) |
| SLkey | `getSLkey(String classId, CallBackGet cb)` | CallBackGet | マスタ取得(JSON) |
| SLkey | `getSLkey(String classId, String lang, CallBackGet cb)` | CallBackGet | マスタ取得(多言語) |

### POST 系

| API | DataAccess メソッド | コールバック型 | 詳細 |
|-----|-------------------|-------------|------|
| domain-api | `postDomainAPI(String param, JsonObject body, CallBackDomain cb)` | CallBackDomain | ドメイン処理 |
| async-api | `postAsyncAPI(String param, JsonObject body, CallBack cb)` | CallBack | 非同期ジョブ投入 |
| async-api | `postAsyncAPI(String param, JsonObject body, CallBackAsync cb)` | CallBackAsync | 非同期ジョブ投入（分岐） |
| ocr-api | `postOcrAPI(String param, JsonObject body, CallBackPostOcr cb)` | CallBackPostOcr | OCR 処理 |
| ocr-api | `postOcrAPI(String param, JsonObject body, long timeout, CallBackPostOcr cb)` | CallBackPostOcr | OCR 処理（タイムアウト指定） |
| pdf-api | `postPdfAPI(String param, String body, CallBack cb)` | CallBack | PDF 生成（CSV形式） |
| notice-api | `postNoticeAPI(String param, JsonObject body, CallBack cb)` | CallBack | 通知送信 |
| gen-contact-api | `postGenContactAPI(String param, JsonObject body, CallBack cb)` | CallBack | 汎用連絡先登録 |
| sms-api | `postShortMessageSendAPI(String param, JsonObject body, CallBack cb)` | CallBack | SMS 送信 |

### PUT 系

| API | DataAccess メソッド | コールバック型 | 詳細 |
|-----|-------------------|-------------|------|
| data-api | `putDataAPI(String param, JsonObject body, CallBack cb)` | CallBack | データ更新 |
| data-api | `putDataAPI(String param, JsonObject body, CallBackPut cb)` | CallBackPut | データ更新（分岐） |
| insert-api | `putInsertAPI(String param, JsonObject body, CallBackPut cb)` | CallBackPut | データ挿入 |
| employee-api | `putEmployeeAPI(String param, JsonObject body, CallBackPut cb)` | CallBackPut | 社員情報更新 |
| file-api | `putFileAPIPersist(String param, CallBackGet cb)` | CallBackGet | ファイル永続化 |
| session-api | `putSessionAPI(String param, JsonObject body, CallBackGet cb)` | CallBackGet | セッション更新 |
| datawrite-api | `putDataWriteAPI(String dataWriteId, JsonArray data, CallBack cb)` | CallBack | DataWrite 一括書込 |

### DELETE 系

| API | DataAccess メソッド | コールバック型 | 詳細 |
|-----|-------------------|-------------|------|
| file-api | `deleteFileAPI(String param, CallBack cb)` | CallBack | ファイル削除 |
| data-api | `deleteDataAPI(String param, CallBack cb)` | CallBack | データ削除 |
| data-api | `deleteDataAPI(String param, CallBackDelete cb)` | CallBackDelete | データ削除（分岐） |

### サービス呼び出し

| メソッド | コールバック型 | 詳細 |
|---------|-------------|------|
| `getService(String address, JsonObject message, CallBackService cb)` | CallBackService | EventBus サービス呼び出し |
| `getServiceOriginal(String address, JsonObject message, CallBackService cb)` | CallBackService | サービス呼び出し（原文返却） |

---

## コールバック型 選択ガイド

```
データ取得だけ？
  ├─ 成功/失敗だけで十分 → CallBack
  ├─ 200/204/fail を分けたい → CallBackGet
  └─ マスタ(TreeMap)が欲しい → CallBackSLkey

データ更新？
  ├─ 成功/失敗だけで十分 → CallBack
  └─ 201/409(楽観ロック)/fail を分けたい → CallBackPut

データ削除？
  ├─ 成功/失敗だけで十分 → CallBack
  └─ 204/404/fail を分けたい → CallBackDelete

特殊 API？
  ├─ Env → CallBackEnv (ok/fail)
  ├─ Async Job → CallBackAsync (created/exclusive/fail)
  ├─ Domain → CallBackDomain (created/appError/fail)
  ├─ OCR → CallBackPostOcr (success/errorApp/errorOcr/errorSys/fail)
  └─ Service → CallBackService (ok/fail)
```

---

## パラメータ構築

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.ParamBuilder;

// URI パラメータ: "テーブル?key1=val1&key2=val2"
String param = "TABLENAME" + ParamBuilder.setParam("key1", "val1", "key2", "val2");

// 非同期パラメータ: "val1 val2 val3"（半角スペース区切り）
String asyncParam = ParamBuilder.makeAsyncParam("val1", "val2", "val3");
```

---

## ステータスコード一覧

| コード | 定数名 | 意味 |
|-------|-------|------|
| 200 | `HTTP_CODE_SUCCESS_200` | 成功（データあり） |
| 201 | `HTTP_CODE_SUCCESS_201` | 作成成功 |
| 202 | `HTTP_CODE_SUCCESS_202` | 受付完了 |
| 204 | `HTTP_CODE_SUCCESS_204` | 成功（データなし） |
| 404 | `HTTP_STATUS_CODE_NOT_FOUND` | リソース不在 |
| 40406 | — | 主キー型不一致 |
| 40407 | — | インデックスプロパティ型不一致 |
| 40410 | `HTTP_STATUS_CODE_REQUESTED_RESOURCE_DOES_NOT_EXIST` | リソース定義不在 |
| 40423 | — | リソース定義が見つからない |
| 409 | `HTTP_STATUS_CODE_CONFLICT` | 競合 |
| 40909 | `HTTP_STATUS_CODE_RESOURCE_CHANGED` | 楽観ロック失敗（他者更新済み） |
| 40910 | — | DB整合性制約違反 |
| 40926 | `HTTP_STATUS_CODE_EXCLUSIVE_CONTROL` | 排他制御エラー |
| 500 | `HTTP_CODE_ERROR` | サーバーエラー |
| 50018 | — | リソース定義取得不能 |
| 900 | `HTTP_STATUS_CODE_TIMEOUT` | タイムアウト |
```