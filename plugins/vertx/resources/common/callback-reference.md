# コールバック型リファレンス

> 各コールバックの正確なインポート・コンストラクタ・メソッドを記載。
> AI はこのファイルを参照して、コールバック実装を一貫して生成すること。

---

## 共通パッケージ

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.*;
```

---

## 0. AbstractCallBack（全コールバックの基底クラス）

CallBack インターフェースと CallBackSLkey を除く、すべてのコールバッククラスが継承する基底クラス。
共通フィールド (`busname`, `container`, `message`) を保持し、`replyFail()` ヘルパーを提供する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.AbstractCallBack;

// 直接インスタンス化は不可（abstract class）
// 具象コールバック（CallBackGet, CallBackPut 等）が extends する
```

**提供フィールド:**

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `busname` | `String` | EventBus バス名（ログ識別用） |
| `container` | `Container` | Verticle コンテナ（ログ・設定取得） |
| `message` | `Message<JsonObject>` | EventBus メッセージ（reply 送信先） |

**提供メソッド:**

| メソッド | 説明 |
|---------|------|
| `replyFail(int code, String logMessage)` | エラーログ出力 + createReplyObject で返却 |

**コンストラクタパターン:**

```java
// すべての具象コールバックはこの形式
public CallBackXxx(String busname, Container container, Message<JsonObject> message) {
    super(busname, container, message);
}
```

> **重要**: 各具象コールバックのメソッド（ok, created, fail 等）にはデフォルト実装がある。
> ビジネスロジックのカスタマイズが必要な場合のみ `@Override` する。
> デフォルト実装は LogUtil でログ出力 + ResponseUtil で reply を返す。

---

## 1. CallBack（基本インターフェース）

最もシンプルなコールバック。成功/失敗を `code` で判定する。
**AbstractCallBack を継承しない（interface）。**

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBack;

new CallBack("BUS_NAME", container, message) {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                // 成功処理
                JsonObject body = responseData.getObject("body");
                message.reply(ResponseUtil.convertResponse(body));
            } else {
                // エラー処理
                container.logger().error("API エラー: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("API エラー"));
            }
        } catch (Exception e) {
            container.logger().error(e.getMessage());
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 2. CallBackGet（GET 専用） — extends AbstractCallBack

200 → `ok()`, 204 → `noContent()`, その他 → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackGet;

// パターン A: デフォルト実装をそのまま使う（@Override 不要）
new CallBackGet("BUS_NAME", container, message);

// パターン B: ok() のみカスタマイズ
new CallBackGet("BUS_NAME", container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            // 200: データ取得成功 — ビジネスロジックを追加
            JsonObject body = responseData.getObject("body");
            message.reply(ResponseUtil.convertResponse(body));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "ok", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};

// パターン C: 全メソッドをカスタマイズ
new CallBackGet("BUS_NAME", container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            JsonObject body = responseData.getObject("body");
            message.reply(ResponseUtil.convertResponse(body));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "ok", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void noContent(JsonObject responseData) {
        try {
            // 204: データなし
            message.reply(ResponseUtil.createReplyObject(204, "データなし"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "noContent", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "GET 失敗: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("GET 失敗: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 3. CallBackPut（PUT 専用） — extends AbstractCallBack

201 → `created()`, 40909 → `resourceAlreadyChanged()`, 40910 → `databaseIntegrityConstraintViolation()`, その他 → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackPut;

// パターン A: デフォルト実装をそのまま使う
new CallBackPut("BUS_NAME", container, message);

// パターン B: created() のみカスタマイズ
new CallBackPut("BUS_NAME", container, message) {
    @Override
    public void created(JsonObject responseData) {
        try {
            // 201: 更新成功
            message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "created", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void resourceAlreadyChanged(JsonObject responseData) {
        try {
            // 40909: 楽観ロック失敗（他者が先に更新）
            message.reply(ResponseUtil.createReplyObject(40909, "他のユーザーが更新済みです"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "resourceAlreadyChanged", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "PUT 失敗: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("PUT 失敗: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

> **注意**: `databaseIntegrityConstraintViolation(JsonObject)` もデフォルト実装あり。必要な場合のみ @Override する。

---

## 4. CallBackDelete（DELETE 専用） — extends AbstractCallBack

204 → `noContent()`, 40410 → `resourceDoesNotExist()`, その他 → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackDelete;

// パターン A: デフォルト実装をそのまま使う
new CallBackDelete("BUS_NAME", container, message);

// パターン B: カスタマイズ
new CallBackDelete("BUS_NAME", container, message) {
    @Override
    public void noContent(JsonObject responseData) {
        try {
            // 204: 削除成功
            message.reply(ResponseUtil.createReplyObject(204, "削除完了"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "noContent", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void resourceDoesNotExist(JsonObject responseData) {
        try {
            // 40410: 対象リソースが存在しない
            message.reply(ResponseUtil.createReplyObject(40410, "対象データが存在しません"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "resourceDoesNotExist", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "DELETE 失敗: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("DELETE 失敗: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 5. CallBackEnv（Env-API 専用） — extends AbstractCallBack

200 → `ok()`, その他 → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackEnv;

// パターン A: デフォルト実装をそのまま使う
new CallBackEnv("BUS_NAME", container, message);

// パターン B: ok() をカスタマイズして環境変数を抽出
new CallBackEnv("BUS_NAME", container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            LogUtil.info(container.logger(), busname, "ok", responseData.toString());
            // レスポンスから環境変数を直接取得
            JsonObject body = responseData.getObject("body");
            // body から必要な値を取得
            // body.getString("queue")    → Queue 名
            // body.getString("moduleid")  → Module ID
            message.reply(ResponseUtil.convertResponse(body));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "ok", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "Env 取得失敗: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("Env 取得失敗: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 6. CallBackAsync（Async-API 専用） — extends AbstractCallBack

201 → `created()`, 40926 → `exclusive()`, その他 → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackAsync;

// パターン A: デフォルト実装をそのまま使う
new CallBackAsync("BUS_NAME", container, message);

// パターン B: カスタマイズ
new CallBackAsync("BUS_NAME", container, message) {
    @Override
    public void created(JsonObject responseData) {
        try {
            // 201: ジョブ投入成功
            message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "created", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void exclusive(JsonObject responseData) {
        try {
            // 40926: 排他制御エラー（同一ジョブ実行中）
            message.reply(ResponseUtil.createReplyObject(40926, "同一ジョブが実行中です"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "exclusive", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "Async 投入失敗: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("Async 投入失敗: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 7. CallBackDomain（Domain-API 専用） — extends AbstractCallBack

201 → `created()`, 400系 → `appError()`, その他(500系) → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

> **修正済み**: `appError()` は実際のエラーコードで返却する（旧版は201を返していた）。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackDomain;

// パターン A: デフォルト実装をそのまま使う
new CallBackDomain("BUS_NAME", container, message);

// パターン B: カスタマイズ
new CallBackDomain("BUS_NAME", container, message) {
    @Override
    public void created(JsonObject responseData) {
        try {
            // 201: ドメイン処理成功
            message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "created", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void appError(int code, int detailCode, JsonObject responseData) {
        try {
            // 400系: アプリケーションエラー — 実際のエラーコードで返却
            LogUtil.error(container.logger(), busname, "appError",
                "code=" + code + " detail=" + detailCode);
            message.reply(ResponseUtil.createReplyObject(code, responseData.toString()));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "appError", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "Domain 失敗: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("Domain 失敗: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 8. CallBackPostOcr（OCR-API 専用） — extends AbstractCallBack

200 → `success()`, 300 → `errorApplication()`, 400 → `errorOcr()`, 500 → `errorSystem()`, その他 → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackPostOcr;

// パターン A: デフォルト実装をそのまま使う
new CallBackPostOcr("BUS_NAME", container, message);

// パターン B: success() のみカスタマイズ
new CallBackPostOcr("BUS_NAME", container, message) {
    @Override
    public void success(JsonObject responseData) {
        try {
            message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "success", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void errorApplication(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "errorApplication", "OCR アプリエラー: code=" + code);
            message.reply(ResponseUtil.createReplyObject(code, "OCR アプリケーションエラー"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "errorApplication", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void errorOcr(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "errorOcr", "OCR 処理エラー: code=" + code);
            message.reply(ResponseUtil.createReplyObject(code, "OCR 処理エラー"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "errorOcr", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void errorSystem(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "errorSystem", "OCR システムエラー: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("OCR システムエラー"));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "errorSystem", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "OCR 想定外エラー: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("OCR 想定外エラー: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 9. CallBackService（サービス呼び出し専用） — extends AbstractCallBack

200 → `ok()`, その他 → `fail()`

デフォルト実装あり。カスタマイズが必要なメソッドのみ @Override する。

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackService;

// パターン A: デフォルト実装をそのまま使う
new CallBackService("BUS_NAME", container, message);

// パターン B: カスタマイズ
new CallBackService("BUS_NAME", container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "ok", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }

    @Override
    public void fail(int code, JsonObject responseData) {
        try {
            LogUtil.error(container.logger(), busname, "fail", "Service 失敗: code=" + code);
            message.reply(ResponseUtil.createReplyObjectFail("Service 失敗: " + code));
        } catch (Exception e) {
            LogUtil.error(container.logger(), busname, "fail", e);
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 10. CallBackSLkey（SLkey マスタ取得専用）

TreeMap&lt;String, String&gt; で Class値→名称 を返す。
**AbstractCallBack を継承しない（interface）。**

```java
import java.util.TreeMap;
import jp.co.payroll.p3.submodules.refactorCommonScreen.api.callback.CallBackSLkey;

new CallBackSLkey() {
    @Override
    public void callBack(int code, TreeMap<String, String> map, Throwable th) {
        try {
            if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                // map: {Class値 → 名称} の TreeMap
                for (Map.Entry<String, String> entry : map.entrySet()) {
                    // entry.getKey() = Class値, entry.getValue() = 名称
                }
            } else {
                container.logger().error("SLkey 取得失敗: code=" + code);
            }
        } catch (Exception e) {
            container.logger().error(e.getMessage());
            message.reply(ResponseUtil.createReplyObjectFail(e));
        }
    }
};
```

---

## 継承構造まとめ

```
AbstractCallBack (abstract class)
  ├─ CallBackGet        — ok / noContent / fail
  ├─ CallBackPut        — created / resourceAlreadyChanged / databaseIntegrityConstraintViolation / fail
  ├─ CallBackDelete     — noContent / resourceDoesNotExist / fail
  ├─ CallBackEnv        — ok / fail
  ├─ CallBackAsync      — created / exclusive / fail
  ├─ CallBackDomain     — created / appError / fail
  ├─ CallBackPostOcr    — success / errorApplication / errorOcr / errorSystem / fail
  └─ CallBackService    — ok / fail

CallBack (interface)     — callBack(code, responseData, th)
CallBackSLkey (interface) — callBack(code, map, th)
```

---

## 共通ユーティリティ インポート

```java
// レスポンス構築
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.ResponseUtil;

// ログ出力
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.LogUtil;

// パラメータ構築
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.ParamBuilder;

// HTTP ステータスコード定数
import jp.co.payroll.p3.submodules.refactorCommonScreen.constants.HttpConstants;

// JSON キー定数
import jp.co.payroll.p3.submodules.refactorCommonScreen.constants.JsonKeyConstants;

// 文字列ユーティリティ
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.StringUtil;

// フィルタ結果変換
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.FilterConverter;

// JSON ナビゲーション（P3フォーム型別）
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.JsonNavigator;
```
