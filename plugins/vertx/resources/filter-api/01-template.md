# Filter-API テンプレート

---

## GET — CallBackGet パターン

```java
// {テーブル名}フィルタ検索
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{TABLENAME}" + ParamBuilder.setParam(
    "_filter", "{filterExpression}",
    "_sort", "{sortField}",
    "_count", "100"
);

new DataAccess(container, vertx).getFilterAPI(param,
    new CallBackGet(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, responseData.toString());
                JsonObject body = responseData.getObject("body");
                // フィルタ結果を JSON 形式に変換
                JsonArray data = body.getArray("data");
                JsonArray converted = FilterConverter.convertFilterResultInJsonFormat(data);
                message.reply(ResponseUtil.convertResponse(
                    new JsonObject().putArray("data", converted)));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void noContent(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "データなし");
                message.reply(ResponseUtil.createReplyObject(204, "データなし"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "フィルタ検索失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("フィルタ検索失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## FilterConverter の使い分け

```java
import jp.co.payroll.p3.submodules.refactorCommonScreen.util.FilterConverter;

// CSV配列 → JSON オブジェクト配列
JsonArray jsonData = FilterConverter.convertFilterResultInJsonFormat(filterResult);

// JSON → PUT 用データ（BFX フィールド除去 + "_" 値除去）
JsonArray putData = FilterConverter.editJsonToPut(jsonArray);

// JSON → CSV 形式（"H" ヘッダ + "D" データ行）
JsonArray csvData = FilterConverter.convertFilterResultInJconCsvFormat(jsonArray);

// JSON → 配列形式
JsonArray arrayData = FilterConverter.convertFilterResultInArrayFormat(jsonArray);
```
