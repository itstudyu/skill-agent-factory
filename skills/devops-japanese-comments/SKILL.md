---
name: devops-japanese-comments
description: Enforce Japanese language in code comments and log messages. Run after code review. Converts all English comments to Japanese. Adds missing comments to complex logic blocks.
allowed-tools: Read, Edit, Grep, Glob
---

# Japanese Comments Enforcement (Step 4 of Pipeline)

コードのコメントとログメッセージを日本語に統一する。

---

## Rules

1. **ALL comments must be in Japanese** — no English comments in source code
2. **Log messages** (console.log, logger.info, print, etc.) → Japanese
3. **JSDoc / docstring** → Japanese
4. **TODO / FIXME comments** → Japanese
5. **Inline comments** → Japanese
6. **Do NOT translate:** variable names, function names, string values returned to users/API

---

## What to Convert

### Before
```typescript
// Get user by ID
const user = await db.user.findUnique({ where: { id } });

// Check if user exists
if (!user) {
  throw new Error('User not found'); // This stays in English (API response)
}

console.log('User fetched successfully', user.id); // ← convert this
```

### After
```typescript
// IDでユーザーを取得する
const user = await db.user.findUnique({ where: { id } });

// ユーザーの存在確認
if (!user) {
  throw new Error('User not found'); // API レスポンスは英語のまま
}

console.log('ユーザーの取得に成功しました', user.id);
```

---

## Adding Missing Comments

Add Japanese comments to:
- [ ] Functions/methods without any description comment
- [ ] Complex logic blocks (conditions with 3+ conditions, non-obvious algorithms)
- [ ] Class definitions
- [ ] Important constants

**Do NOT add comments to obvious one-liners** (e.g., `return true`, simple assignments).

---

## JSDoc Example

```typescript
/**
 * ユーザーIDに基づいてプロフィール情報を取得する
 * @param userId - 対象ユーザーのID
 * @returns ユーザープロフィール、存在しない場合はnull
 */
async function getUserProfile(userId: string): Promise<UserProfile | null> {
```

---

## Scan & Fix Process

1. Use `Grep` to find all files modified in this task
2. Read each file
3. Find English comments — convert to Japanese
4. Find complex logic without comments — add Japanese comments
5. Use `Edit` to apply changes

---

## Output

```
## 📝 Japanese Comments

- 変換したコメント数: X 件
- 追加したコメント数: Y 件
- 対象ファイル: [list]
```
