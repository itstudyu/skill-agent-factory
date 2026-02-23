---
name: devops-git-commit
version: v1.0
description: Git commit with branch strategy. Run at the END of every development task. Creates a feature branch if needed, writes a concise Japanese commit message (1-4 lines), and never commits to master/main unless the user explicitly says so.
tags: [devops, git, commit, branch, version-control]
allowed-tools: Bash
---

# Git Commit (Step 7 of Pipeline)

開発完了後のgitコミット手順。マスターブランチへの直接コミットは禁止。

---

## Step 1 — Check Current Branch

```bash
git branch --show-current
git status
```

---

## Step 2 — Branch Strategy

| Current branch | User instruction | Action |
|---------------|-----------------|--------|
| `master` or `main` | No instruction to commit to master | **Create new feature branch** |
| `master` or `main` | User explicitly says "master/mainにコミット" | Commit to master |
| Feature branch already | — | Stay on current branch |

### Creating a New Branch

If a new branch is needed → **Ask the user for:**
1. **Task Number** (e.g., `TASK-123`, `#42`, `001`)
2. **Feature Name** (short English name, e.g., `user-auth`, `payment-api`)

Branch naming format:
```
feature/{TaskNumber}/{Name}
```

Examples:
- `feature/TASK-123/user-auth`
- `feature/42/payment-api`
- `feature/001/dashboard-redesign`

```bash
git checkout -b feature/{TaskNumber}/{Name}
```

---

## Step 3 — Stage Changed Files

Stage only the files related to this task:
```bash
git add {specific files}
```

**Never use `git add .` or `git add -A`** — always add files explicitly to avoid accidentally staging unrelated changes or sensitive files.

Review what will be staged:
```bash
git diff --staged
```

---

## Step 4 — Write Commit Message (Japanese, 1-4 lines)

### Rules
- **Language: Japanese only**
- **Length: 1–4 lines max** — concise, key content only
- First line: what was done (imperative form)
- Lines 2–4 (optional): why or what changed

### Format
```
{変更内容の要約}

{必要であれば補足1}
{必要であれば補足2}
```

### Good Examples
```
ユーザー認証APIを実装

- JWTトークンによる認証処理を追加
- ログイン・ログアウトエンドポイントを作成
```

```
決済フォームのバリデーション修正
```

```
商品一覧ページのパフォーマンス改善

N+1クエリを解消しバッチ取得に変更
```

### Bad Examples
```
fix bug                          ← Not Japanese
Updated various things and fixed several issues as well as adding new feature   ← Too long
WIP                              ← Not descriptive
```

---

## Step 5 — User Confirmation (REQUIRED before committing)

**ALWAYS ask the user before running `git commit`.** Never commit silently.

Show the user a summary and wait for explicit approval:

```
## 📋 コミット確認

**ブランチ:** feature/TASK-123/user-auth
**ステージ予定ファイル:**
  - src/api/auth.ts (new)
  - src/utils/jwt.ts (new)
  - tests/__tests__/auth.test.ts (new)

**コミットメッセージ:**
  ユーザー認証APIを実装

  - JWTトークンによる認証処理を追加
  - ログイン・ログアウトエンドポイントを作成

コミットを実行してよろしいですか？
```

**Gate:** Do not proceed to Step 6 until the user says yes (e.g., "yes", "ok", "はい", "ㅇㅇ", "해줘").

If the user wants to change the message or files → apply changes and re-confirm.

---

## Step 6 — Commit

```bash
git commit -m "$(cat <<'EOF'
{日本語コミットメッセージ1行目}

{補足2行目（あれば）}
{補足3行目（あれば）}
EOF
)"
```

---

## Step 7 — Report

```bash
git log --oneline -3
git status
```

```
## ✅ コミット完了

- ブランチ: feature/TASK-123/user-auth
- コミット: {hash} {message}
- 変更ファイル: X 件
```
