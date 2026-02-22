---
name: devops-arch-review
description: Architecture and coding standards review. Use when the user asks to check code structure, folder layout, naming conventions, error handling patterns, try/catch placement, log levels, or duplicate code. Triggers on "check architecture", "review structure", "코드 구조 확인", "アーキテクチャレビュー", "중복 코드", "에러 처리 패턴".
---

# Architecture Review Skill

コーディング規約・アーキテクチャパターンの準拠を検査するスキル。
コード品質レビュー（devops-code-review）の後に実行し、構造的な問題を検出・修正する。

---

## STEP 0 — Main 定義の確認 (コンテキストキャッシュ付き)

**プロジェクトルートの `.skill-factory-context.json` を先に確認すること。**

### 0-1: キャッシュ確認

```bash
# プロジェクトルートを検索
Glob: .skill-factory-context.json
```

**キャッシュが存在する場合 → そのまま使用:**
```
✅ コンテキストキャッシュ読み込み済み
   Mainモジュール: {mainModule.description}
   対象ファイル: {mainModule.files}
   → 確認不要。チェック開始します。
```

**キャッシュが存在しない場合 → ユーザーに質問:**

```
## 📋 アーキテクチャレビュー開始前の確認 (初回のみ)

このプロジェクトで「メインモジュール（フロー制御のみを担当するエントリポイント）」は
どのファイル・レイヤーに該当しますか？

例:
1. index.ts / main.ts / app.ts（エントリポイントファイル）
2. Controller / Handler レイヤー
3. Route ファイル（Express/Fastify など）
4. __main__.py / main.py（Python）
5. Main.java / Application.java（Java）
6. その他（自由に教えてください）

→ 次回から自動的に記憶されます。
```

### 0-2: キャッシュ保存

ユーザーの回答を受け取ったら `.skill-factory-context.json` を作成/更新する:

```json
{
  "mainModule": {
    "description": "{ユーザーの回答}",
    "files": ["{検出されたファイルパターン}"]
  },
  "language": "{検出された言語}",
  "framework": "{検出されたフレームワーク}",
  "testFramework": "{検出されたテストフレームワーク}",
  "lastUpdated": "{今日の日付}"
}
```

> このファイルは `.gitignore` に追加を推奨（プロジェクトごとに異なるため）。
> ただしチームで共有したい場合はコミットしてもよい。

ユーザーの回答 or キャッシュ確認完了後 → 以下のチェックリストを実行する。

---

## STEP 1 — フォルダ構造チェック

### チェック項目

**1-1. backend / frontend の分離**
```
✅ OK:   src/backend/   src/frontend/
✅ OK:   apps/api/      apps/web/
❌ NG:   src/ 内にバックエンドとフロントエンドが混在
```

**1-2. 役割別ディレクトリの存在**

| ディレクトリ | 役割 | 存在すべき場所 |
|-------------|------|--------------|
| `/services` | ビジネスロジック | backend / 共通 |
| `/utils`    | 再利用可能なヘルパー | backend / frontend 両方 |
| `/features` | 機能単位のまとまり | frontend 推奨 |
| `/controllers` or `/handlers` | HTTPレイヤー | backend |
| `/repositories` | DB アクセス層 | backend |

**報告フォーマット:**
```
### [STEP 1] フォルダ構造
✅ backend/frontend 分離: OK
⚠️  /services ディレクトリが見当たりません → src/services/ の作成を推奨
❌ バックエンドとフロントのコードが src/ に混在 → 分離が必要
```

---

## STEP 2 — ファイル責務チェック

### チェック項目

**2-1. 同一ドメインの関数まとめ**

```
✅ OK:  userService.ts にユーザー関連の関数がまとまっている
✅ OK:  orderRepository.ts に注文のDB操作がまとまっている
❌ NG:  utils.ts に日付・バリデーション・認証・メール送信が混在
```

**2-2. 1ファイル1責務**

各ファイルを読んで確認:
- ファイル名とその内容が一致しているか
- 関係のない処理が混入していないか

**NG パターン例:**
```typescript
// ❌ user.service.ts にメール送信ロジックが直接書かれている
async function createUser(data) {
  await db.user.create({ data });
  await nodemailer.createTransport(...).sendMail(...); // ← email.service.ts へ移動すべき
}
```

---

## STEP 3 — Main ロール チェック

STEP 0 で確認したメインモジュールを対象に検査する。

### ルール

| 許可 | 禁止 |
|------|------|
| ✅ 関数呼び出し | ❌ 計算・データ変換ロジック |
| ✅ 実行順序の決定 | ❌ 条件分岐による処理 (データに関するもの) |
| ✅ エラーのキャッチ・最終ログ | ❌ バリデーションロジック |
| ✅ レスポンスの返却 | ❌ SQL / DB クエリの直書き |

**NG 例 → 修正例:**

```typescript
// ❌ Main(Controller)にビジネスロジックが混入
async function handleCreateUser(req, res) {
  const { email, password } = req.body;

  // ← バリデーションはサービス層へ
  if (!email.includes('@')) return res.status(400).json({ error: 'Invalid email' });
  if (password.length < 8) return res.status(400).json({ error: 'Password too short' });

  // ← ハッシュ計算はサービス層へ
  const hashed = await bcrypt.hash(password, 12);
  const user = await db.user.create({ data: { email, password: hashed } });

  res.json(user);
}

// ✅ Main はフロー制御のみ
async function handleCreateUser(req, res) {
  try {
    const user = await userService.createUser(req.body); // ← 全ロジックをサービスへ委譲
    res.json(user);
  } catch (err) {
    logger.error(`[UserController] ユーザー作成失敗: ${err.message}`);
    res.status(500).json({ error: err.message });
  }
}
```

---

## STEP 4 — 関数30行チェック

### 例外として許容するもの (コメント必須)

```
✅ 例外OK: switch/match の網羅的なケース列挙
✅ 例外OK: データ定義・設定オブジェクト
✅ 例外OK: SQL クエリビルダー（JOIN・WHERE が多い場合）
✅ 例外OK: 自動生成されたコード
❌ 例外NG: 「複雑だから」という理由だけで長い通常の関数
```

例外の場合はコメントを追加:
```typescript
// NOTE: 全APIステータスコードを網羅するためswitch文が長くなっている。分割すると可読性が低下するため例外とする。
```

---

## STEP 5 — 命名規則チェック

### ルール

| 対象 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | camelCase | `getUserById`, `isLoading` |
| クラス・型 | PascalCase | `UserService`, `OrderItem` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| ファイル名 | kebab-case or camelCase | `user-service.ts`, `userService.ts` |
| 保遍的略語 | そのまま許可 | `id`, `url`, `api`, `db`, `ctx`, `req`, `res` |

**NG パターン:**
```typescript
❌ get_user_by_id()   ← snake_case（JS/TSでは NG）
❌ GetUserById()      ← PascalCase（関数には NG）
❌ identifier         ← id で十分
❌ universalResourceLocator ← url で十分
```

---

## STEP 6 — 重複コードチェック

### ルール

3箇所以上で同じロジックが出現 → **utils へ必ず抽出**

**検出方法:**
```bash
# 類似パターンを検索
grep -rn "{重複しているパターン}" src/
```

**修正パターン:**
```typescript
// ❌ 3ファイルに同じ日付フォーマット処理
const formatted = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-...`

// ✅ utils/format-date.ts に抽出
export function formatDate(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-...`
}
```

---

## STEP 7 — try/catch 配置チェック

### ルール

```
外部 API / DB / ファイル IO → ここで catch → エラーフォーマット後 re-throw
                                          ↓
                                     Main で最終 catch → ログ + 出力
```

**下位レイヤー:** エラーをフォーマットして re-throw のみ。ログ出力・レスポンス返却禁止。
**Main レイヤー:** 最終 catch でログ出力 + レスポンス返却。

---

### 言語別 Re-throw パターン

#### TypeScript / JavaScript
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

#### Python
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

#### Java
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

#### Go
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

---

## STEP 8 — エラーメッセージ形式チェック

### 形式

```
[モジュール名] 操作名失敗: 理由
```

**言語別例:**

```typescript
// TypeScript
throw new Error(`[UserService] ユーザー作成失敗: メールアドレスが重複しています`);
throw new Error(`[PaymentService] 決済処理失敗: カードが拒否されました`);
```

```python
# Python
raise RuntimeError(f"[UserService] ユーザー作成失敗: メールアドレスが重複しています")
```

```java
// Java
throw new ServiceException("[UserService] ユーザー作成失敗: メールアドレスが重複しています");
```

```go
// Go
return nil, fmt.Errorf("[UserService] ユーザー作成失敗: メールアドレスが重複しています")
```

**チェックポイント:**
- `[ ]` でモジュール名を括っているか
- 操作名 + `失敗:` の形式か
- 理由が具体的か（"エラーが発生しました" は NG）

---

## STEP 9 — ログレベルチェック

### ルール

| レベル | 使う場面 | 禁止例 |
|--------|---------|--------|
| `error` | 例外・失敗・障害 | — |
| `warn`  | 想定内の異常（リトライ可能など） | — |
| `info`  | デバッグに必要な情報のみ | ❌ 全リクエストの開始/終了 |
| `debug` | 開発時のみ（本番では無効化） | — |

**NG パターン:**
```typescript
❌ logger.info(`getUserById called with id=${id}`);   // デバッグ不要な定型ログ
❌ logger.info(`Response sent successfully`);          // 不要な成功ログ
❌ logger.info(`Loop iteration ${i}`);                 // ループごとのログ
```

**OK パターン:**
```typescript
✅ logger.info(`[UserService] キャッシュミス — DBから取得: userId=${id}`);  // デバッグに有用
✅ logger.warn(`[PaymentService] リトライ実行: attempt=${retryCount}`);
✅ logger.error(`[OrderService] 注文確定失敗: ${err.message}`);
```

---

## 最終レポート形式

```
## 🏗️ アーキテクチャレビュー完了

**Mainモジュール:** {ユーザーが指定したファイル/レイヤー}

| チェック項目 | 結果 | 問題数 |
|------------|------|-------|
| フォルダ構造 | ✅ / ⚠️ / ❌ | {N}件 |
| ファイル責務 | ✅ / ⚠️ / ❌ | {N}件 |
| Mainロール  | ✅ / ⚠️ / ❌ | {N}件 |
| 関数30行    | ✅ / ⚠️ / ❌ | {N}件 |
| 命名規則    | ✅ / ⚠️ / ❌ | {N}件 |
| 重複コード  | ✅ / ⚠️ / ❌ | {N}件 |
| try/catch配置 | ✅ / ⚠️ / ❌ | {N}件 |
| エラーメッセージ形式 | ✅ / ⚠️ / ❌ | {N}件 |
| ログレベル  | ✅ / ⚠️ / ❌ | {N}件 |

**修正済み:** {N}件
**要確認（自動修正不可）:** {N}件

{要確認事項のリスト}
```

---

*Skill: devops-arch-review | Category: devops | Version: v1.0 | Last updated: 2026-02-22*
