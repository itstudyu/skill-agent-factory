# Contact-API クイックスタート

> 連絡先情報の取得・登録を行う API。

---

## いつ使うか

- 連絡先の取得（contact-api）
- 汎用連絡先の登録（gen-contact-api）

---

## DataAccess メソッド

### GET
```java
da.getContactAPI(String param, CallBackGet cb);
```

### POST（汎用連絡先）
```java
da.postGenContactAPI(String param, JsonObject body, CallBack cb);
```

> **注意**: GET は `APIClientPool.CONTACT_API`、POST は `APIClientPool.GEN_CONTACT_API` を使用。
