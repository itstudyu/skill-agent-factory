---
name: vertx-repo-analyzer
version: v1.0
description: Vert.x プロジェクトの構造を解析し、既存の Verticle・EventBus ハンドラ・アドレス一覧を把握する。新しいエンドポイント追加前の事前調査として使用。
tags: [vertx, java, eventbus, verticle, analysis]
allowed-tools: Read, Grep, Glob
---

# Vert.x リポジトリ解析

新しい EventBus エンドポイントを追加する前に、既存の構造を正確に把握する。

---

## STEP 1: プロジェクト構造の確認

```
Glob: **/*.java           → Java ソースファイルの一覧
Glob: **/pom.xml          → Maven 依存関係
Glob: **/build.gradle     → Gradle 依存関係（あれば）
```

確認すべき情報:
- Verticle クラスの命名規則 (`*Verticle.java`, `*Handler.java`, `*Worker.java`)
- パッケージ構成 (例: `com.example.vertx.verticle`)
- Java バージョン (Java 7 → ラムダ不可、匿名内部クラス使用)

---

## STEP 2: Verticle クラスの列挙

```
Grep: "extends AbstractVerticle"   → メイン Verticle
Grep: "extends Verticle"           → 旧 API Verticle
Grep: "implements Handler"         → ハンドラ実装
Grep: "eventBus().registerHandler" → Java 7 式ハンドラ登録
Grep: "eventBus().consumer"        → Java 8+ 式ハンドラ登録（参考）
```

> **Java 7 制約**: `eventBus().consumer()` は Vert.x 3.x+ の API。
> Java 7 プロジェクトでは `eventBus().registerHandler()` (Vert.x 2.x) を使用。
> バージョンを必ず確認すること。

---

## STEP 3: EventBus アドレス一覧の抽出

登録済みアドレスを grep で抽出:

```
Grep: "registerHandler\("   → ハンドラ登録箇所
Grep: "eventBus\.send\("    → 送信箇所
Grep: "eventBus\.publish\(" → ブロードキャスト箇所
```

アドレスの命名規則を確認する (例: `module.action.resource`):
- `user.get.list`
- `order.create`
- `notification.send.all`

---

## STEP 4: API リファレンスとの照合

`plugins/vertx/resources/api-reference/` のドキュメントと現状の実装を照合する。

```
Read: plugins/vertx/resources/api-reference/README.md
```

ドキュメント化されていないエンドポイントがあれば、その旨を報告する。

---

## 出力フォーマット

```
## 🔍 Vert.x リポジトリ解析結果

### プロジェクト情報
- Vert.x バージョン: x.x.x
- Java バージョン: 7 / 8 / 11
- ハンドラ登録スタイル: registerHandler (Vert.x 2.x) / consumer (Vert.x 3.x+)

### Verticle 一覧
| クラス名 | パッケージ | 役割 |
|---------|-----------|------|
| MainVerticle | com.example.vertx | エントリーポイント |
| UserVerticle | com.example.vertx.user | ユーザー系ハンドラ |

### EventBus アドレス一覧
| アドレス | Verticle | 説明 |
|---------|---------|------|
| user.get.list | UserVerticle | ユーザー一覧取得 |
| order.create | OrderVerticle | 注文作成 |

### ⚠️ 未ドキュメントのエンドポイント
- `xxx.yyy.zzz` — API リファレンスに記載なし

### 次のアクション
- 新しいエンドポイントを追加する場合: vertx-eventbus-register を使用
- フロントから呼び出す場合: vertx-api-caller を使用
```
