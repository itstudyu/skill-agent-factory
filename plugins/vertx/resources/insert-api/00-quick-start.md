# Insert-API クイックスタート

> データの新規挿入（INSERT）を行う API。

---

## いつ使うか

- 新規レコードの挿入
- Data-API の PUT（UPDATE）とは異なり、INSERT 専用

---

## DataAccess メソッド

```java
da.putInsertAPI(String param, JsonObject body, CallBackPut cb);
```
