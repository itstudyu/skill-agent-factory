# SMS-API テンプレート

---

## POST — CallBack パターン

```java
// SMS 送信
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{smsType}";
JsonObject body = new JsonObject();
body.putString("to", "{phoneNumber}");
body.putString("message", "{messageBody}");

new DataAccess(container, vertx).postShortMessageSendAPI(param, body,
    new CallBack(methodName, container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200
                    || code == HttpConstants.HTTP_CODE_SUCCESS_201) {
                    LogUtil.info(container.logger(), BUS_NAME, methodName, "SMS 送信成功");
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    LogUtil.error(container.logger(), BUS_NAME, methodName, "SMS 送信失敗: code=" + code);
                    message.reply(ResponseUtil.createReplyObjectFail("SMS 送信失敗: " + code));
                }
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
