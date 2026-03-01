# Async-API テンプレート

---

## AsyncJob ヘルパー使用（推奨）

```java
// 非同期ジョブ投入
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String asyncParam = ParamBuilder.makeAsyncParam("{platformId}", "{param1}", "{param2}");

new AsyncJob(container, vertx).exec(message,
    new AsyncJob.Param("{moduleId}", asyncParam, AsyncJob.RunMode.Run),
    new CallBackAsync(BUS_NAME, container, message) {

        @Override
        public void created(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "ジョブ投入成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void exclusive(JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "排他制御エラー");
                message.reply(ResponseUtil.createReplyObject(40926, "同一ジョブが実行中です"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "ジョブ投入失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("ジョブ投入失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## ジョブ状態確認

```java
// ジョブ状態取得
String param = "job/{jobId}";
new DataAccess(container, vertx).getAsyncAPI(param,
    new CallBack("BUS_NAME", container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    message.reply(ResponseUtil.createReplyObjectFail("ジョブ状態取得失敗: " + code));
                }
            } catch (Exception e) {
                container.logger().error(e.getMessage());
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
