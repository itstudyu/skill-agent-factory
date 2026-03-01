# Insert-API テンプレート

---

## PUT — CallBackPut パターン

```java
// データ新規挿入
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{TABLENAME}";
JsonObject body = new JsonObject();
// body に挿入データをセット

new DataAccess(container, vertx).putInsertAPI(param, body,
    new CallBackPut(methodName, container, message) {

        @Override
        public void created(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "挿入成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void resourceAlreadyChanged(JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "重複エラー");
                message.reply(ResponseUtil.createReplyObject(40909, "データが既に存在します"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "挿入失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("挿入失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
