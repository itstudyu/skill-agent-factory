# Re-throw / Error Propagation Patterns by Language

> Referenced from SKILL.md STEP 7 — try/catch 配置チェック

---

## TypeScript / JavaScript

```typescript
// ✅ 下位レイヤー（Service / Repository）— フォーマット後 re-throw
async function fetchUser(id: string): Promise<User> {
  try {
    return await db.user.findUniqueOrThrow({ where: { id } });
  } catch (err) {
    // エラーフォーマット後 re-throw のみ
    throw new Error(`[UserRepository] ユーザー取得失敗: ${(err as Error).message}`);
  }
}

// ✅ Main レイヤー（Controller）— 最終ログ + 出力
async function handleGetUser(req: Request, res: Response) {
  try {
    const user = await userService.getUser(req.params.id);
    res.json(user);
  } catch (err) {
    // 最終ログ + レスポンス返却
    logger.error((err as Error).message);
    res.status(500).json({ error: (err as Error).message });
  }
}
```

---

## Python

```python
# ✅ 下位レイヤー（Service / Repository）— フォーマット後 re-raise
def fetch_user(user_id: str) -> User:
    try:
        return db.query(User).filter(User.id == user_id).one()
    except NoResultFound as e:
        # エラーフォーマット後 re-raise のみ
        raise RuntimeError(f"[UserRepository] ユーザー取得失敗: {e}") from e

# ✅ Main レイヤー — 最終ログ + 出力
def handle_get_user(user_id: str):
    try:
        user = user_service.get_user(user_id)
        return jsonify(user)
    except RuntimeError as e:
        # 最終ログ + レスポンス返却
        logger.error(str(e))
        return jsonify({"error": str(e)}), 500
```

---

## Java

```java
// ✅ 下位レイヤー（Repository）— フォーマット後 re-throw
public User fetchUser(String id) {
    try {
        return userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("not found"));
    } catch (Exception e) {
        // エラーフォーマット後 re-throw のみ
        throw new ServiceException("[UserRepository] ユーザー取得失敗: " + e.getMessage(), e);
    }
}

// ✅ Main レイヤー（Controller）— 最終ログ + 出力
@GetMapping("/{id}")
public ResponseEntity<?> getUser(@PathVariable String id) {
    try {
        User user = userService.getUser(id);
        return ResponseEntity.ok(user);
    } catch (ServiceException e) {
        // 最終ログ + レスポンス返却
        log.error(e.getMessage());
        return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
    }
}
```

---

## Go

```go
// ✅ 下位レイヤー（Repository）— エラーラップ後 return
func (r *UserRepository) FetchUser(id string) (*User, error) {
    user, err := r.db.FindUser(id)
    if err != nil {
        // %w でラップして re-return のみ
        return nil, fmt.Errorf("[UserRepository] ユーザー取得失敗: %w", err)
    }
    return user, nil
}

// ✅ Main レイヤー（Handler）— 最終ログ + 出力
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, err := h.service.GetUser(r.PathValue("id"))
    if err != nil {
        // 最終ログ + レスポンス返却
        slog.Error(err.Error())
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(user)
}
```
