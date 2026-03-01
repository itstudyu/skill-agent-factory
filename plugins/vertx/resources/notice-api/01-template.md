# Notice-API テンプレート

---

## POST — CallBack パターン

```java
// 通知送信
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{noticeType}";
JsonObject body = new JsonObject();
// body に通知データをセット

new DataAccess(container, vertx).postNoticeAPI(param, body,
    new CallBack(methodName, container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200
                    || code == HttpConstants.HTTP_CODE_SUCCESS_201) {
                    LogUtil.info(container.logger(), BUS_NAME, methodName, "通知送信成功");
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    LogUtil.error(container.logger(), BUS_NAME, methodName, "通知送信失敗: code=" + code);
                    message.reply(ResponseUtil.createReplyObjectFail("通知送信失敗: " + code));
                }
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
