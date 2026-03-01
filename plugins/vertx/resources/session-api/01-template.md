# Session-API テンプレート

---

## GET — CallBack パターン

```java
// セッション情報取得
final String methodName = "{methodName}";

String param = "{sessionKey}";
new DataAccess(container, vertx).getSessionAPI(param,
    new CallBack(methodName, container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    message.reply(ResponseUtil.createReplyObjectFail("セッション取得失敗: " + code));
                }
            } catch (Exception e) {
                container.logger().error(e.getMessage());
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## PUT — CallBackGet パターン

```java
// セッション情報更新
final String methodName = "{methodName}";

String param = "{sessionKey}";
JsonObject body = new JsonObject();
// body にセッションデータをセット

new DataAccess(container, vertx).putSessionAPI(param, body,
    new CallBackGet(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "セッション更新成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void noContent(JsonObject responseData) {
            try {
                message.reply(ResponseUtil.createReplyObject(204, "セッション更新完了"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "セッション更新失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("セッション更新失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
