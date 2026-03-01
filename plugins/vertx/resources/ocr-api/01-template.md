# OCR-API テンプレート

---

## POST — CallBackPostOcr パターン

```java
// OCR 処理実行
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{ocrType}";
JsonObject body = new JsonObject();
// body に OCR リクエストデータをセット

new DataAccess(container, vertx).postOcrAPI(param, body,
    new CallBackPostOcr(methodName, container, message) {

        @Override
        public void success(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "OCR 成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void errorApplication(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "OCR アプリエラー: code=" + code);
                message.reply(ResponseUtil.createReplyObject(code, "OCR アプリケーションエラー"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void errorOcr(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "OCR 処理エラー: code=" + code);
                message.reply(ResponseUtil.createReplyObject(code, "OCR 処理エラー"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void errorSystem(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "OCR システムエラー: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("OCR システムエラー"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "OCR 想定外エラー: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("OCR 想定外エラー: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## タイムアウト指定（長時間処理）

```java
// OCR 処理（タイムアウト60秒）
long timeout = 60000L;
new DataAccess(container, vertx).postOcrAPI(param, body, timeout, callback);
```
