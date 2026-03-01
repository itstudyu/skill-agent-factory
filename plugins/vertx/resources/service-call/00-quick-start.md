# Service 呼び出しクイックスタート

> EventBus 上の他のサービス（Verticle）を直接呼び出す。API-Verticle を経由しない直接通信。

---

## いつ使うか

- 他の Verticle への直接メッセージ送信
- API-Verticle 経由ではない EventBus 通信
- 原文返却が必要な場合は `getServiceOriginal` を使用

---

## DataAccess メソッド

```java
da.getService(String address, JsonObject message, CallBackService cb);
da.getServiceOriginal(String address, JsonObject message, CallBackService cb);
```

### 違い
- `getService`: レスポンスコード 200 → `ok()`、その他 → `fail()`
- `getServiceOriginal`: 全レスポンスを `ok()` に渡す（コード無関係）。エラー時のみ `fail()`

---

## タイムアウト

デフォルト: `container.config().getLong("timeoutShort", 5000L)`
