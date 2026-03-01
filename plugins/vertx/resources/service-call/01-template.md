# Service 呼び出しテンプレート

---

## getService — CallBackService パターン

```java
// サービス呼び出し
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String address = "{service-address}";
JsonObject serviceMessage = new JsonObject();
// serviceMessage にリクエストデータをセット

new DataAccess(container, vertx).getService(address, serviceMessage,
    new CallBackService(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "サービス呼び出し成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "サービス呼び出し失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("サービス呼び出し失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## getServiceOriginal — 原文返却パターン

```java
// サービス呼び出し（原文返却）
final String methodName = "{methodName}";

String address = "{service-address}";
JsonObject serviceMessage = new JsonObject();

new DataAccess(container, vertx).getServiceOriginal(address, serviceMessage,
    new CallBackService(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                // 全レスポンスがそのまま渡される（コード無関係）
                LogUtil.info(container.logger(), BUS_NAME, methodName, "原文返却");
                message.reply(responseData);
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "サービスエラー: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("サービスエラー: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
