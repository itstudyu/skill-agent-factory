# Schema-API テンプレート

---

## GET — CallBack パターン

```java
// スキーマ情報取得
final String methodName = "{methodName}";

new DataAccess(container, vertx).getSchemaAPI("{TABLENAME}",
    new CallBack(methodName, container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    LogUtil.info(container.logger(), BUS_NAME, methodName, "スキーマ取得成功");
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    LogUtil.error(container.logger(), BUS_NAME, methodName, "スキーマ取得失敗: code=" + code);
                    message.reply(ResponseUtil.createReplyObjectFail("スキーマ取得失敗: " + code));
                }
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
