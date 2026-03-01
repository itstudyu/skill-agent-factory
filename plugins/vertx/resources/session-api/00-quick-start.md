# Session-API クイックスタート

> Web セッション情報の取得・更新を行う API。

---

## いつ使うか

- ユーザーセッション情報の取得
- セッション情報の更新

---

## DataAccess メソッド

### GET
```java
da.getSessionAPI(String param, CallBack cb);
```

### PUT
```java
da.putSessionAPI(String param, JsonObject body, CallBackGet cb);
```
