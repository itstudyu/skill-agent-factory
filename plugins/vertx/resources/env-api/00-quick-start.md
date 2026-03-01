# Env-API クイックスタート

> 環境変数・モジュール設定を取得する API。非同期ジョブの Queue 名やバージョン取得に使用。

---

## いつ使うか

- 非同期ジョブの Queue 名・Module バージョン取得
- 環境設定値の取得
- AsyncJob ヘルパー内で自動的に呼ばれる（手動不要な場合が多い）

---

## DataAccess メソッド

```java
da.getEnvAPI(String param, CallBack cb);
da.getEnvAPI(String param, CallBackEnv cb);
```

---

## パラメータ構築

```java
// モジュール設定取得
String param = "module" + ParamBuilder.setParam("name", "{moduleId}");
// → "module?name={moduleId}"
```
