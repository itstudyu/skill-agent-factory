# Async-API クイックスタート

> 非同期ジョブの投入・状態確認を行う API。

---

## いつ使うか

- バッチ処理の非同期実行
- ジョブ投入と状態確認
- 排他制御付きジョブ実行

---

## 呼び出し方法

### 方法1: AsyncJob ヘルパー（推奨）

EnvAPI → postAsyncAPI を自動で実行する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.AsyncJob;

new AsyncJob(container, vertx).exec(message, param, callback);
```

### 方法2: DataAccess 直接呼び出し

```java
da.postAsyncAPI(String param, JsonObject body, CallBack cb);
da.postAsyncAPI(String param, JsonObject body, CallBackAsync cb);
da.getAsyncAPI(String param, CallBack cb);  // 状態確認
```

---

## AsyncJob.Param 構築

```java
// 基本
new AsyncJob.Param("{moduleId}", "{param}", AsyncJob.RunMode.Run)

// Queue 名・バージョン手動指定（EnvAPI スキップ）
new AsyncJob.Param("{moduleId}", "{param}", AsyncJob.RunMode.Run)
    .setQueueName("{queueName}")
    .setModuleVersion("{version}")

// EnvAPI から Module ID を取得
new AsyncJob.Param("{moduleId}", "{param}", AsyncJob.RunMode.Run, true)
```

---

## RunMode

| モード | 値 | 用途 |
|-------|-----|------|
| `Run` | `"0"` | 通常実行 |
| `Deploy` | `"1"` | モジュール配置のみ |
| `Exclusive` | `"2"` | 排他実行 |
