# Notice-API クイックスタート

> 通知（メール等）の送信を行う API。

---

## いつ使うか

- メール通知の送信
- テンプレートベースの通知

---

## DataAccess メソッド

```java
da.postNoticeAPI(String param, JsonObject body, CallBack cb);
```

> **注意**: API 名は定数 `APIClientPool.NOTICE_API` を使用。
