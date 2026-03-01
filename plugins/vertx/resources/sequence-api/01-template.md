# Sequence-API テンプレート

---

## GET — CallBack パターン

```java
// 採番取得
final String methodName = "{methodName}";

String param = "{sequenceType}";
new DataAccess(container, vertx).getSequenceAPI(param,
    new CallBack(methodName, container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    LogUtil.info(container.logger(), BUS_NAME, methodName, "採番成功");
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    LogUtil.error(container.logger(), BUS_NAME, methodName, "採番失敗: code=" + code);
                    message.reply(ResponseUtil.createReplyObjectFail("採番失敗: " + code));
                }
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
