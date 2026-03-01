# Schema-API クイックスタート

> テーブルのスキーマ情報（カラム定義・型情報）を取得する API。

---

## いつ使うか

- テーブル構造の動的取得
- フォーム自動生成のための項目情報取得
- データバリデーション用の型情報取得

---

## DataAccess メソッド

```java
da.getSchemaAPI(String param, CallBack cb);
```

---

## パラメータ構築

```java
String param = "{TABLENAME}";
```
