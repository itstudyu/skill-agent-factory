# SMS-API クイックスタート

> SMS メッセージの送信を行う API。

---

## いつ使うか

- SMS メッセージ送信
- 認証コード送信

---

## DataAccess メソッド

```java
da.postShortMessageSendAPI(String param, JsonObject body, CallBack cb);
```

> **注意**: API 名は定数 `APIClientPool.SMS_API` を使用。
