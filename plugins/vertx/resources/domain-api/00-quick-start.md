# Domain-API クイックスタート

> ドメインロジック（業務処理）を実行する API。

---

## いつ使うか

- 複雑な業務ロジックの実行
- バリデーション付き処理
- トランザクション的な処理

---

## DataAccess メソッド

```java
da.postDomainAPI(String param, JsonObject body, CallBackDomain cb);
```
