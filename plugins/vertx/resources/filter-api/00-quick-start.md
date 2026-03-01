# Filter-API クイックスタート

> 複雑な条件でのフィルタ検索を行う API。Data-API との違いはクエリ文字列による柔軟な検索。

---

## いつ使うか

- 複数条件を組み合わせた検索
- ページネーション付き検索
- ソート条件付き検索
- Data-API の単純 GET では不足する場合

---

## DataAccess メソッド

```java
da.getFilterAPI(String param, CallBack cb);
da.getFilterAPI(String param, CallBackGet cb);
```

---

## パラメータ構築

```java
// フィルタ条件をクエリ文字列で指定
String param = "{TABLENAME}" + ParamBuilder.setParam(
    "_filter", "{filterExpression}",
    "_sort", "{sortExpression}",
    "_count", "{件数}",
    "_start", "{開始位置}"
);
```
