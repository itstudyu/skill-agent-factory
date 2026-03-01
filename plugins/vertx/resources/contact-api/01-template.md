# Contact-API テンプレート

---

## GET — CallBackGet パターン

```java
// 連絡先取得
final String methodName = "{methodName}";

String param = "{contactParam}" + ParamBuilder.setParam("{key}", "{value}");
new DataAccess(container, vertx).getContactAPI(param,
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
                message.reply(ResponseUtil.createReplyObject(204, "連絡先データなし"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "連絡先取得失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("連絡先取得失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## POST（汎用連絡先登録）— CallBack パターン

```java
// 汎用連絡先登録
final String methodName = "{methodName}";

String param = "{contactType}";
JsonObject body = new JsonObject();
// body に連絡先データをセット

new DataAccess(container, vertx).postGenContactAPI(param, body,
    new CallBack(methodName, container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200
                    || code == HttpConstants.HTTP_CODE_SUCCESS_201) {
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    message.reply(ResponseUtil.createReplyObjectFail("連絡先登録失敗: " + code));
                }
            } catch (Exception e) {
                container.logger().error(e.getMessage());
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```
