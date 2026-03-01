# Env-API テンプレート

---

## GET — CallBackEnv パターン

```java
// モジュール環境設定取得
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "module" + ParamBuilder.setParam("name", "{moduleId}");
new DataAccess(container, vertx).getEnvAPI(param,
    new CallBackEnv(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, responseData.toString());
                // レスポンスから環境変数を直接取得
                JsonObject body = responseData.getObject("body");
                // body.getString("queue")    → Queue 名
                // body.getString("moduleid")  → Module ID
                // body.getString("version")   → Module Version
                message.reply(ResponseUtil.convertResponse(body));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "Env 取得失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("Env 取得失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## GET — CallBack パターン（シンプル）

```java
// モジュール環境設定取得（コード分岐なし）
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "module" + ParamBuilder.setParam("name", "{moduleId}");
new DataAccess(container, vertx).getEnvAPI(param,
    new CallBack("BUS_NAME", container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    LogUtil.info(container.logger(), BUS_NAME, methodName, responseData.toString());
                    JsonObject body = responseData.getObject("body");
                    message.reply(ResponseUtil.convertResponse(body));
                } else {
                    LogUtil.error(container.logger(), BUS_NAME, methodName, "Env 取得失敗: code=" + code);
                    message.reply(ResponseUtil.createReplyObjectFail("Env 取得失敗: " + code));
                }
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
