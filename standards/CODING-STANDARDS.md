# Global Coding Standards

> **全プロジェクト共通のコーディング規則。**
> これらの規則はすべての言語・カテゴリに適用される。
> 詳細は各カテゴリの CLAUDE.md で言語別に補足する。

---

## Rule 1 — File Header

**すべてのソースファイルの1行目に、そのファイルの責務を一行コメントで書くこと。**

### Format

```
{comment_syntax} {日本語1行サマリー} — {主な処理の説明}
```

### Examples by Language

```typescript
// ユーザー認証サービス — JWTトークンの発行・検証・失効処理を担当
```

```python
# 商品検索モジュール — キーワード・カテゴリ・価格帯での絞り込みと並び替えを処理
```

```go
// データベース接続管理 — コネクションプール設定とヘルスチェックを提供
```

```java
// 注文処理コントローラー — 注文作成・更新・キャンセルのHTTPエンドポイントを定義
```

```sql
-- ユーザーテーブル定義 — 認証情報・プロフィール・設定を管理
```

```css
/* ダッシュボードレイアウト — グリッド構造とレスポンシブブレークポイントを定義 */
```

### Rules
- **Japanese only**
- **1 line only** — no multi-line descriptions here
- Describe the **file's main responsibility**, not what a specific function does
- Use the language's native single-line comment syntax

### ❌ Bad Examples
```typescript
// utils                     ← too vague
// This file was created by John on 2024-01-01  ← irrelevant
// TODO: needs refactoring   ← not a summary
```

---

## Rule 2 — Function / Method Length (Max 30 Lines)

**関数・メソッドは30行以内に収めること（空行・コメント行を除く）。**

### Why 30 Lines?
- A function that fits on one screen is easier to understand and test
- Long functions usually mean the function is doing more than one thing
- Forces Single Responsibility at the function level

### How to Split

```typescript
// ❌ 50-line monolith — doing too many things
async function processOrder(order: Order) {
  if (!order.userId) throw new Error('...');
  if (!order.items.length) throw new Error('...');
  if (order.items.some(i => i.qty <= 0)) throw new Error('...');
  // ... more validation (10 lines total)

  let total = 0;
  for (const item of order.items) {
    const product = await db.product.findUnique({ where: { id: item.productId } });
    total += product.price * item.qty;
  }
  const discount = await getApplicableDiscount(order.userId);
  total = total * (1 - discount);
  // ... more price calculation (15 lines total)

  await db.order.create({ data: { ...order, total } });
  // ... more DB logic (10 lines total)

  await emailService.send({ to: order.userEmail, subject: '...' });
  await pushNotification.send({ userId: order.userId, message: '...' });
  // ... more notifications (10 lines total)
}

// ✅ Split into focused functions — each under 30 lines
async function processOrder(order: Order) {
  validateOrder(order);
  const total = await calculateOrderTotal(order);
  await saveOrder(order, total);
  await notifyUser(order);
}

function validateOrder(order: Order) { ... }          // 10 lines
async function calculateOrderTotal(order: Order) { ... }   // 15 lines
async function saveOrder(order: Order, total: number) { ... } // 8 lines
async function notifyUser(order: Order) { ... }        // 8 lines
```

### Exceptions (must add comment explaining why)
```typescript
// NOTE: このswitch文はAPIの全ステータスコードを網羅するために長くなっている。
//       分割すると可読性が下がるため例外とする。
function getStatusMessage(code: number): string {
  switch (code) {
    case 200: return '...';
    case 201: return '...';
    // ... 35+ cases
  }
}
```

Acceptable exceptions:
- Long `switch` / `match` statements covering exhaustive cases
- Generated/scaffolded code
- SQL query builders with many conditions
- Configuration objects

---

## Rule 3 — One File, One Responsibility

**1ファイル = 1つの関心事。関係のないロジックを同じファイルに混在させない。**

### File Naming Should Reflect Responsibility

| ❌ Avoid | ✅ Do This |
|---------|----------|
| `utils.ts` (20 unrelated helpers) | `format-date.ts`, `validate-email.ts`, `sanitize-html.ts` |
| `api.ts` (all API endpoints) | `auth.api.ts`, `user.api.ts`, `product.api.ts` |
| `helpers.py` (DB + formatting + auth) | `db_helpers.py`, `format_helpers.py`, `auth_helpers.py` |
| `services.ts` (all services) | `user.service.ts`, `payment.service.ts`, `email.service.ts` |
| `types.ts` (all types for entire app) | `user.types.ts`, `product.types.ts`, `api.types.ts` |

### Suggested File Structure by Category

**Backend (TypeScript/Node)**
```
src/
├── controllers/
│   ├── auth.controller.ts      # 認証エンドポイントのみ
│   └── user.controller.ts      # ユーザーエンドポイントのみ
├── services/
│   ├── auth.service.ts         # 認証ロジックのみ
│   └── user.service.ts         # ユーザーロジックのみ
├── utils/
│   ├── format-date.ts          # 日付フォーマットのみ
│   └── validate-input.ts       # バリデーションのみ
```

**Frontend (React)**
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx          # Buttonコンポーネントのみ
│   │   └── Button.test.tsx
│   └── Modal/
│       ├── Modal.tsx
│       └── Modal.test.tsx
├── hooks/
│   ├── useAuth.ts              # 認証フックのみ
│   └── useCart.ts              # カートフックのみ
```

---

## Rule 4 — Commit Confirmation

**`git commit` を実行する前に、必ずユーザーに確認を取ること。**

Show this summary before committing:
```
## 📋 コミット確認

ブランチ: feature/TASK-123/user-auth
ファイル:
  - src/api/auth.ts (new)
  - src/utils/jwt.ts (modified)

コミットメッセージ:
  ユーザー認証APIを実装
  - JWTトークンによる認証処理を追加

コミットを実行してよろしいですか？
```

See `skills/devops-git-commit/SKILL.md` for full commit procedure.

---

## Rule 5 — Folder Structure

**backend / frontend を分離し、役割別ディレクトリを設ける。**

```
src/
├── backend/          # サーバーサイド
│   ├── services/     # ビジネスロジック
│   ├── utils/        # 再利用ヘルパー
│   └── repositories/ # DB アクセス層
└── frontend/         # クライアントサイド
    ├── features/     # 機能単位のまとまり
    ├── components/   # UI コンポーネント
    └── utils/        # フロント用ヘルパー
```

詳細チェックは `skills/devops-arch-review/SKILL.md` を参照。

---

## Rule 6 — Main Role (フロー制御のみ)

**Main モジュール（エントリポイント）はフロー制御に専念する。ビジネスロジックを書かない。**

| Main に書いてよいもの | Main に書いてはいけないもの |
|---------------------|--------------------------|
| 関数呼び出し・実行順序 | 計算・データ変換 |
| エラーのキャッチ・最終ログ | 条件分岐（データ処理に関するもの） |
| レスポンスの返却 | バリデーションロジック / SQL クエリ |

---

## Rule 7 — Naming Conventions

**camelCase を基本とし、保遍的な略語はそのまま使用する。**

| 対象 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | camelCase | `getUserById`, `isLoading` |
| クラス・型 | PascalCase | `UserService`, `OrderItem` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 保遍的略語 | 略語のまま許可 | `id`, `url`, `api`, `db`, `ctx` |

---

## Rule 8 — Duplicate Code → Extract to Utils

**同じロジックが3箇所以上出現したら utils に必ず抽出する。**

```typescript
// ❌ 3ファイルに同じ処理が散在
// ✅ utils/format-date.ts に抽出して import
```

---

## Rule 9 — try/catch Placement

**外部 API / DB / ファイル IO でキャッチ → re-throw → Main で最終処理。**

```
外部IO層    → catch → エラーフォーマット後 re-throw のみ
                ↓
Main 層     → 最終 catch → ログ出力 + レスポンス返却
```

エラーメッセージ形式: `[モジュール名] 操作名失敗: 理由`

言語別の re-throw パターンは `skills/devops-arch-review/SKILL.md` STEP 7 を参照。

---

## Rule 10 — Log Levels

**info は本当にデバッグに必要なものだけ。不要なログは書かない。**

| レベル | 用途 |
|--------|------|
| `error` | 例外・障害 |
| `warn`  | 想定内の異常（リトライ可能など） |
| `info`  | デバッグに有用な情報のみ |
| `debug` | 開発時のみ（本番では無効化） |

```typescript
❌ logger.info(`getUserById called`);   // 不要
✅ logger.info(`[UserService] キャッシュミス — DBから取得: id=${id}`);  // 有用
```

---

## Language-Specific Extensions

These global rules are extended with language-specific conventions in each category:

| Category | Detailed Rules File |
|----------|-------------------|
| Backend | `categories/backend/CLAUDE.md` |
| Frontend | `categories/frontend/CLAUDE.md` |
| Database | `categories/database/CLAUDE.md` |
| API Reference | `categories/api-reference/CLAUDE.md` |
| DevOps | `categories/devops/CLAUDE.md` |

*Last updated: 2026-02-21*
