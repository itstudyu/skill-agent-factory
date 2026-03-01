# Error Message Format Patterns by Language

> Referenced from SKILL.md STEP 8 — エラーメッセージ形式チェック

---

## Format Rule

```
[モジュール名] 操作名失敗: 理由
```

---

## TypeScript / JavaScript

```typescript
throw new Error(`[UserService] ユーザー作成失敗: メールアドレスが重複しています`);
throw new Error(`[PaymentService] 決済処理失敗: カードが拒否されました`);
```

## Python

```python
raise RuntimeError(f"[UserService] ユーザー作成失敗: メールアドレスが重複しています")
```

## Java

```java
throw new ServiceException("[UserService] ユーザー作成失敗: メールアドレスが重複しています");
```

## Go

```go
return nil, fmt.Errorf("[UserService] ユーザー作成失敗: メールアドレスが重複しています")
```

---

## Checklist

- `[ ]` でモジュール名を括っているか
- 操作名 + `失敗:` の形式か
- 理由が具体的か（"エラーが発生しました" は NG）
