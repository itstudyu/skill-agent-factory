# Employee-API テンプレート

---

## GET — CallBackGet パターン

```java
// 社員情報取得
final String methodName = "{methodName}";

String param = "{empNo}" + ParamBuilder.setParam("{key}", "{value}");
new DataAccess(container, vertx).getEmployeeAPI(param,
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
                LogUtil.info(container.logger(), BUS_NAME, methodName, "社員データなし");
                message.reply(ResponseUtil.createReplyObject(204, "社員データなし"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "社員情報取得失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("社員情報取得失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## PUT — CallBackPut パターン

```java
// 社員情報更新
final String methodName = "{methodName}";

String param = "{empNo}";
JsonObject body = new JsonObject();
// body に更新データをセット

new DataAccess(container, vertx).putEmployeeAPI(param, body,
    new CallBackPut(methodName, container, message) {

        @Override
        public void created(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "社員情報更新成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void resourceAlreadyChanged(JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "楽観ロック失敗");
                message.reply(ResponseUtil.createReplyObject(40909, "他のユーザーが更新済みです"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "社員情報更新失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("社員情報更新失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
