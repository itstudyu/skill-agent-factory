---
name: vertx-api-caller
version: v1.0
description: フロントエンド（JavaScript/TypeScript）から Vert.x EventBus を SockJS 経由で呼び出すコードを生成する。既存の呼び出しパターンに倣い、エラーハンドリングとタイムアウト処理を含む。
tags: [vertx, eventbus, frontend, javascript, sockjs]
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Vert.x EventBus API 呼び出し（フロントエンド）

フロントエンドから Vert.x EventBus を呼び出すコードを実装する。

---

## STEP 1: 既存の呼び出しパターンを確認

```
Grep: "eventBus.send("      → 既存の EventBus 呼び出し
Grep: "vertx-eventbus"      → ライブラリの使用方法
Grep: "SockJS"              → SockJS 接続設定
Grep: "eb.send("            → EventBus インスタンス経由の呼び出し
```

プロジェクトで使っているライブラリを確認:
- `vertx3-eventbus-client` (npm)
- `vertxbus.js` (ファイル直接参照)
- カスタムラッパー

---

## STEP 2: EventBus 接続設定の確認

```javascript
// Vert.x EventBus 接続設定
var eb = new EventBus('http://{host}:{port}/eventbus');
eb.onopen = function() {
    // 接続完了後に呼び出し可能
};
```

接続先 URL をプロジェクトの設定ファイルから確認する:
```
Grep: "eventbus"    → 接続設定ファイル
Grep: "/eventbus"   → エンドポイントURL
```

---

## STEP 3: API 呼び出しコードの生成

### パターン A: シンプルな呼び出し（Promise なし）

```javascript
// {エンドポイント説明} — {address} を呼び出す
function call{EndpointName}(params, callback) {
    var request = {
        field1: params.field1,
        field2: params.field2
    };

    eb.send('{address}', request, function(err, reply) {
        if (err) {
            console.error('{address} 呼び出しエラー:', err);
            callback(err, null);
            return;
        }
        if (reply.body.status === 'error') {
            callback(new Error(reply.body.message), null);
            return;
        }
        callback(null, reply.body);
    });
}
```

### パターン B: Promise ラッパー（ES6 使用可能な場合）

```javascript
// {エンドポイント説明} — Promise形式で {address} を呼び出す
function call{EndpointName}(params) {
    return new Promise(function(resolve, reject) {
        var request = {
            field1: params.field1,
            field2: params.field2
        };

        eb.send('{address}', request, function(err, reply) {
            if (err) {
                reject(err);
                return;
            }
            if (reply.body.status === 'error') {
                reject(new Error(reply.body.message));
                return;
            }
            resolve(reply.body);
        });
    });
}
```

### パターン C: タイムアウト付き（長時間処理の場合）

```javascript
// {エンドポイント説明} — タイムアウト付きで {address} を呼び出す
var TIMEOUT_MS = 30000; // 30秒

function call{EndpointName}WithTimeout(params, callback) {
    var timeoutId = setTimeout(function() {
        callback(new Error('{address} タイムアウト (' + TIMEOUT_MS + 'ms)'), null);
    }, TIMEOUT_MS);

    eb.send('{address}', params, function(err, reply) {
        clearTimeout(timeoutId);
        if (err) {
            callback(err, null);
            return;
        }
        callback(null, reply.body);
    });
}
```

---

## STEP 4: API リファレンスとの照合

呼び出し前に `plugins/vertx/resources/api-reference.md` でエンドポイント仕様を確認:

```
Read: plugins/vertx/resources/api-reference.md
```

address が確認できたら、処理モジュール詳細も必要に応じて参照:
```
Read: plugins/vertx/resources/{category}-api.md
```

- リクエストフィールドの型・必須/任意を確認
- レスポンス構造を確認
- エラーレスポンスのパターンを確認

---

## STEP 5: エラーハンドリングチェック

実装後に確認:

- [ ] `err` チェック（接続エラー・タイムアウト）
- [ ] `reply.body.status === 'error'` チェック（アプリケーションエラー）
- [ ] ユーザーへのエラー表示処理
- [ ] ログ出力（`console.error` に日本語メッセージ）
- [ ] 必要な場合はタイムアウト処理

---

## 出力フォーマット

```
## ✅ EventBus 呼び出しコード生成完了

### 呼び出し先エンドポイント
- **Address**: `{address}`
- **リクエスト**: `{ field1: string, field2: number }`
- **レスポンス**: `{ status: string, data: [...] }`

### 生成したコード
（コードスニペット）

### 追加先ファイル
- `src/js/{moduleName}.js` または指定ファイル

### 注意事項
- EventBus 接続が完了 (`eb.onopen`) してから呼び出すこと
- （その他の注意があれば）
```
