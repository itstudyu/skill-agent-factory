# Organ-API テンプレート

---

## GET — CallBackGet パターン

```java
// 組織情報取得
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{organParam}" + ParamBuilder.setParam("{key}", "{value}");
new DataAccess(container, vertx).getOrganAPI(param,
    new CallBackGet(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, responseData.toString());
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void noContent(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "組織データなし");
                message.reply(ResponseUtil.createReplyObject(204, "組織データなし"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "組織情報取得失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("組織情報取得失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
