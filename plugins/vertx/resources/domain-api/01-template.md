# Domain-API テンプレート

---

## POST — CallBackDomain パターン

```java
// ドメイン処理実行
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{domainType}";
JsonObject body = new JsonObject();
// body に処理パラメータをセット

new DataAccess(container, vertx).postDomainAPI(param, body,
    new CallBackDomain(methodName, container, message) {

        @Override
        public void created(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "ドメイン処理成功");
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void appError(int code, int detailCode, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName,
                    "業務エラー: code=" + code + " detail=" + detailCode);
                message.reply(ResponseUtil.createReplyObject(detailCode, "業務エラー: " + detailCode));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "ドメイン処理失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("ドメイン処理失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
