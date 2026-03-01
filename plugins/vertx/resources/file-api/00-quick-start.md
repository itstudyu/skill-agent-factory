# File-API クイックスタート

> ファイルの ID 発行・取得・永続化・削除を行う API。

---

## いつ使うか

- ファイル ID の事前発行
- ファイルメタ情報の取得
- 一時ファイルの永続化
- ファイル削除

---

## DataAccess メソッド

### GET（ファイル取得）
```java
da.getFileAPI(String param, CallBack cb);                    // ファイル・メタ取得
da.getFileIdAPI(String param, CallBack cb);                  // ファイルID発行
da.getFileIdAPI(String param, CallBackGet cb);               // ファイルID発行（分岐）
```

### PUT（永続化）
```java
da.putFileAPIPersist(String param, CallBackGet cb);          // 一時→永続化
```

### DELETE（削除）
```java
da.deleteFileAPI(String param, CallBack cb);                 // 一時ファイル削除のみ
```

---

## ワークフロー

```
1. getFileIdAPI() → ファイルID取得
2. （ファイルアップロード処理）
3. putFileAPIPersist() → 永続化
4. deleteFileAPI() → 不要時に削除（一時ファイルのみ）
```
