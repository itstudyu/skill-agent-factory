---
name: devops-skill-eval
description: Evaluates the quality and correctness of a skill by running test scenarios against it. Use when the user wants to test a skill before deploying, validate a newly created skill, check if a skill behaves as expected, or benchmark skill performance. Triggers on "스킬 테스트", "eval skill", "test skill", "スキルテスト", "validate skill", "skill quality check".
tags: [devops, eval, quality, skill, validate, test]
---

# Skill Eval — スキル品質検証

スキルが正しく動作するかを自動テストシナリオで検証するスキル。
新しいスキルを作成・更新したときに実行し、デプロイ前の品質を保証する。

---

## STEP 1 — 対象スキルの読み込み

```
# 評価対象スキルを指定
Read: skills/{skill-name}/SKILL.md
```

以下を抽出する:
- `name` — スキル識別子
- `description` — トリガーキーワードと用途
- `requires` — 依存スキル
- 本文のステップ・チェックリスト・出力形式

---

## STEP 2 — テストシナリオの自動生成

SKILL.md の description と本文を解析して、以下の3種類のシナリオを生成する。

### シナリオ A — ハッピーパス (正常系)
スキルが最も典型的に使われるケース。

```
例: devops-arch-review の場合
  入力: "src/controllers/user.ts でアーキテクチャをチェックして"
  期待: Main 定義の確認 or キャッシュ読み込み → 9項目チェック → レポート出力
```

### シナリオ B — エッジケース
境界値・不完全な入力・例外的な状況。

```
例: devops-arch-review の場合
  入力: コンテキストキャッシュなし状態でのアーキレビュー
  期待: ユーザーに Main 定義を質問し、回答後にキャッシュ保存
```

### シナリオ C — ネガティブケース (誤発動テスト)
スキルが**発動すべきでない**入力を与えて誤発動を確認。

```
例: devops-arch-review の場合
  入力: "このAPIのレスポンスタイムを教えて" (アーキレビューと無関係)
  期待: スキルが発動しない / 適切にスキップ
```

---

## STEP 3 — 評価基準の設定

各シナリオに対してパス条件を定義する:

| 評価項目 | 説明 | 重み |
|---------|------|------|
| **トリガー精度** | 正しいリクエストで発動するか | 30% |
| **ステップ網羅性** | SKILL.md に定義された全ステップが実行されるか | 25% |
| **出力形式の準拠** | 指定されたレポート形式で出力されるか | 20% |
| **requires 遵守** | 依存スキルを先に実行しているか | 15% |
| **誤発動なし** | 無関係なリクエストで発動しないか | 10% |

---

## STEP 4 — シナリオ実行

各シナリオを実際に実行してレスポンスを記録する。

```
## ▶️ シナリオ A 実行: ハッピーパス
入力: {scenario_input}
---
{実際の出力}
---
```

実行後に以下を確認:
- 期待されたステップが全て実行されたか
- 出力形式が SKILL.md の定義と一致しているか
- エラーや中断が発生しなかったか

---

## STEP 5 — スコアリング

各評価項目をスコアリングし、総合スコアを算出する。

```
## 📊 スキル評価レポート: {skill-name}

### シナリオ結果

| シナリオ | 結果 | 詳細 |
|---------|------|------|
| A: ハッピーパス | ✅ PASS / ❌ FAIL | {詳細} |
| B: エッジケース | ✅ PASS / ❌ FAIL | {詳細} |
| C: 誤発動テスト | ✅ PASS / ❌ FAIL | {詳細} |

### 評価スコア

| 評価項目 | スコア | 重み | 加重スコア |
|---------|--------|------|----------|
| トリガー精度 | {0-100} | 30% | {score} |
| ステップ網羅性 | {0-100} | 25% | {score} |
| 出力形式の準拠 | {0-100} | 20% | {score} |
| requires 遵守 | {0-100} | 15% | {score} |
| 誤発動なし | {0-100} | 10% | {score} |

**総合スコア: {total}/100**

### 判定

| スコア | 判定 | 対応 |
|--------|------|------|
| 90〜100 | ✅ EXCELLENT | デプロイOK |
| 75〜89  | ✅ GOOD | 軽微な改善を推奨してデプロイOK |
| 60〜74  | ⚠️ NEEDS WORK | 問題点を修正してから再評価 |
| 0〜59   | ❌ FAIL | 大幅な見直しが必要 |

### 改善提案

{FAILまたは低スコア項目があれば、具体的な改善案を記載}
```

---

## STEP 6 — 改善サポート (スコアが 75 未満の場合)

スコアが低い場合、以下を提案する:

1. **description の改善** — トリガーキーワードを追加・整理
2. **ステップの明確化** — 曖昧な指示を具体的な手順に変更
3. **出力形式の明示** — 期待するレポート形式をコードブロックで定義
4. **requires の追加** — 依存スキルが未定義の場合

修正後に `devops-skill-eval` を再実行して改善を確認する。

---

*Skill: devops-skill-eval | Category: devops | Version: v1.0 | Last updated: 2026-02-22*
