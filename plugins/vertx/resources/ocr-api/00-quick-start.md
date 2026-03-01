# OCR-API クイックスタート

> OCR（光学文字認識）処理を行う API。

---

## いつ使うか

- 画像からのテキスト読取
- 帳票の OCR 処理

---

## DataAccess メソッド

```java
da.postOcrAPI(String param, JsonObject body, CallBackPostOcr cb);
da.postOcrAPI(String param, JsonObject body, long timeout, CallBackPostOcr cb);
```

> **注意**: OCR は処理時間が長い。デフォルトタイムアウトは `container.config().getLong("timeoutShort")`。
> 長時間処理の場合は `timeout` パラメータ付きメソッドを使用。
