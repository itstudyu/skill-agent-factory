# Data-API クイックスタート

> データの CRUD 操作を行う中心的な API。

---

## いつ使うか

- テーブルデータの取得・更新・削除
- SLkey（マスタデータ）の取得
- DataWrite による一括書込

---

## DataAccess メソッド一覧

### GET
```java
da.getDataAPI(String param, CallBack cb);
da.getDataAPI(String param, CallBackGet cb);
da.getDataAPI(String param, CallBack cb, boolean cache);  // cache=true でキャッシュ使用
```

### PUT
```java
da.putDataAPI(String param, JsonObject body, CallBack cb);
da.putDataAPI(String param, JsonObject body, CallBackPut cb);
```

### DELETE
```java
da.deleteDataAPI(String param, CallBack cb);
da.deleteDataAPI(String param, CallBackDelete cb);
```

### SLkey（マスタ取得）
```java
da.getSLkey(String classId, CallBackSLkey cb);    // TreeMap 返却
da.getSLkey(String classId, CallBackGet cb);       // JSON 返却
da.getSLkey(String classId, String lang, CallBackGet cb);  // 多言語
```

### DataWrite（一括書込）
```java
da.putDataWriteAPI(String dataWriteId, JsonArray data, CallBack cb);
```

---

## パラメータ構築パターン

```java
// 基本: テーブル名 + 条件
String param = "TABLENAME" + ParamBuilder.setParam("key1", "val1", "key2", "val2");
// → "TABLENAME?key1=val1&key2=val2"

// SLkey: MPSL/{nonPlatformId}/{classId}（DataAccess が自動構築）
da.getSLkey("CL001", callback);

// DataWrite: {nonPlatformId}/{dataWriteId}（DataAccess が自動構築）
da.putDataWriteAPI("DW001", dataArray, callback);
```
