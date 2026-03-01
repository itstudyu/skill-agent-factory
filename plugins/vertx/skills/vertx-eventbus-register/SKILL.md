---
name: vertx-eventbus-register
version: v1.0
description: Vert.x EventBus に新しいハンドラを Java 7 形式（匿名内部クラス）で登録する。既存 Verticle への追加または新規 Verticle 作成を行い、コーディング規約（日本語コメント、30行制限）に準拠する。
tags: [vertx, java, java7, eventbus, handler, register]
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
requires: [vertx-repo-analyzer]
---

# Vert.x EventBus ハンドラ登録

Java 7 制約に準拠した EventBus ハンドラを追加する。

---

## ⚠️ Java 7 制約事項（必読）

| 禁止 | 代替 |
|-----|------|
| ラムダ式 `message -> { }` | 匿名内部クラス `new Handler<Message<JsonObject>>() { ... }` |
| `eventBus().consumer()` (Vert.x 3.x+) | `eventBus().registerHandler()` (Vert.x 2.x) |
| メソッド参照 `this::handleRequest` | 匿名内部クラス内で直接実装 |
| ダイヤモンド演算子 `new ArrayList<>()` | 型パラメータ明示 `new ArrayList<String>()` |
| try-with-resources | 明示的な finally ブロック |

---

## STEP 1: 事前確認

まず `vertx-repo-analyzer` の出力（または手動確認）で以下を把握する:

1. Vert.x バージョン (`pom.xml` の `vertx-core` バージョン)
2. 既存のハンドラ登録スタイル（`registerHandler` or `consumer`）
3. 追加先 Verticle（既存 or 新規）
4. アドレス命名規則

```
Read: pom.xml    → Vert.x バージョン確認
Grep: "registerHandler"  → 既存の登録スタイル確認
```

---

## STEP 2: アドレスの決定

命名規則: `{module}.{action}.{resource}`

例:
- `user.get.list` — ユーザー一覧取得
- `order.create` — 注文作成
- `notification.send.all` — 全員通知

ユーザーに確認:
- モジュール名
- アクション (get / create / update / delete / send)
- リソース名

---

## STEP 3: ハンドラの実装

### パターン A: 既存 Verticle に追加

```java
// {モジュール名}ハンドラ — {説明}
vertx.eventBus().registerHandler("{address}", new Handler<Message<JsonObject>>() {
    @Override
    public void handle(Message<JsonObject> message) {
        // リクエストの取り出し
        JsonObject request = message.body();
        String param = request.getString("paramName");

        // バリデーション
        if (param == null || param.isEmpty()) {
            JsonObject error = new JsonObject()
                .putString("status", "error")
                .putString("message", "paramName は必須です");
            message.reply(error);
            return;
        }

        // 処理
        JsonObject response = new JsonObject();
        // ... ビジネスロジック ...
        response.putString("status", "ok");

        message.reply(response);
    }
});
```

### パターン B: 新規 Verticle を作成

```java
// {モジュール名}Verticle — {説明}を担当する Verticle
public class {ModuleName}Verticle extends Verticle {

    @Override
    public void start() {
        registerHandlers();
    }

    // ハンドラ登録 — 全エンドポイントをここで一括登録
    private void registerHandlers() {
        registerGetListHandler();
        registerCreateHandler();
        // 追加のハンドラ...
    }

    // {リソース}一覧取得ハンドラ
    private void registerGetListHandler() {
        vertx.eventBus().registerHandler("{address}.get.list", new Handler<Message<JsonObject>>() {
            @Override
            public void handle(Message<JsonObject> message) {
                // 実装
                JsonObject response = new JsonObject();
                response.putString("status", "ok");
                message.reply(response);
            }
        });
    }
}
```

> **30行制限**: 各 `handle()` メソッドが 30 行を超える場合は、`private` メソッドに分割する。

---

## STEP 4: Verticle の起動登録

新規 Verticle を作成した場合、メイン Verticle（またはデプロイ設定）に登録する:

```java
// {ModuleName}Verticle のデプロイ
container.deployVerticle("{パッケージ}.{ModuleName}Verticle", new AsyncResultHandler<String>() {
    @Override
    public void handle(AsyncResult<String> result) {
        if (result.failed()) {
            // {ModuleName}Verticle のデプロイ失敗
            logger.error("{ModuleName}Verticle デプロイ失敗: " + result.cause().getMessage());
        }
    }
});
```

---

## STEP 5: コーディング規約チェック

実装後に以下を確認する:

- [ ] ファイル先頭に日本語サマリーコメント (`// {クラス名} — {説明}`)
- [ ] 各 `handle()` メソッドが 30 行以内
- [ ] バリデーションが含まれている（null チェック、必須項目チェック）
- [ ] エラー時に `message.reply()` でエラーレスポンスを返している
- [ ] ラムダ式・メソッド参照を使っていない
- [ ] `eventBus().consumer()` を使っていない（Vert.x 2.x の場合）

---

## STEP 6: API リファレンス・処理モジュールへの記載

新しいエンドポイントを追加したら以下の 2 箇所に記載する:

**① `plugins/vertx/resources/api-reference.md`** — エンドポイント契約書に追記:
```markdown
## {エンドポイント名}

- **Address**: `{address}`
- **Request**: `{ field: type, ... }`
- **Response**: `{ field: type, ... }`
- **説明**: 何をするか
- **処理モジュール**: data-api / filter-api / notice-api / env-api / async-api
```

**② 該当する処理モジュールフォルダ** — 実装テンプレートを参照して追記:
```
Read: plugins/vertx/resources/{category}-api/00-quick-start.md  ← 基本パターン確認
Read: plugins/vertx/resources/{category}-api/01-*-template.md   ← 実装テンプレート参照
```
適切なフォルダ（data-api/ / filter-api/ / notice-api/ / env-api/ / async-api/ 等）の
テンプレートに倣って実装する。

---

## 出力フォーマット

```
## ✅ EventBus ハンドラ登録完了

### 追加したエンドポイント
- **Address**: `{address}`
- **Verticle**: `{VerticleName}.java`
- **変更ファイル**: `src/main/java/.../VerticleName.java`

### コードスニペット
（追加したコードの主要部分）

### 次のアクション
- フロントから呼び出す場合: vertx-api-caller を使用
- API ドキュメント更新: api-reference.md + {category}-api/ フォルダに追記済み / 要追記
```
