# File-API テンプレート

---

## ファイルID発行 — CallBackGet パターン

```java
// ファイルID発行
final String methodName = "{methodName}";

new DataAccess(container, vertx).getFileIdAPI("",
    new CallBackGet(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, responseData.toString());
                // responseData からファイルIDを取得
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void noContent(JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "ファイルID発行失敗");
                message.reply(ResponseUtil.createReplyObjectFail("ファイルID発行失敗"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "ファイルID発行エラー: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("ファイルID発行エラー: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## ファイル永続化 — CallBackGet パターン

```java
// ファイル永続化
final String methodName = "{methodName}";
String fileId = "{fileId}";

new DataAccess(container, vertx).putFileAPIPersist(fileId,
    new CallBackGet(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "永続化成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void noContent(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "永続化（データなし）");
                message.reply(ResponseUtil.createReplyObject(204, "永続化完了"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "永続化失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("永続化失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## ファイル削除

```java
// 一時ファイル削除
String param = "{fileId}";
new DataAccess(container, vertx).deleteFileAPI(param,
    new CallBack("BUS_NAME", container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200
                    || code == HttpConstants.HTTP_CODE_SUCCESS_204) {
                    message.reply(ResponseUtil.createReplyObject(204, "削除完了"));
                } else {
                    message.reply(ResponseUtil.createReplyObjectFail("ファイル削除失敗: " + code));
                }
            } catch (Exception e) {
                container.logger().error(e.getMessage());
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
