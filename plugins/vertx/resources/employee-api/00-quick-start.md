# Employee-API クイックスタート

> 社員情報の取得・更新を行う API。

---

## いつ使うか

- 社員番号による社員情報取得
- 社員情報の更新

---

## DataAccess メソッド

### GET
```java
da.getEmployeeAPI(String param, CallBackGet cb);
```

### PUT
```java
da.putEmployeeAPI(String param, JsonObject body, CallBackPut cb);
```
