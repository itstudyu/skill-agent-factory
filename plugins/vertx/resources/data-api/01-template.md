# Data-API テンプレート

> コピー＆ペーストして使用する。`{...}` を実際の値に置換すること。

---

## GET — CallBackGet パターン（推奨）

```java
// {テーブル名}データ取得
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{TABLENAME}" + ParamBuilder.setParam("{key}", "{value}");
new DataAccess(container, vertx).getDataAPI(param,
    new CallBackGet(methodName, container, message) {

        @Override
        public void ok(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, responseData.toString());
                // responseData.getObject("body").getArray("data") でデータ配列取得
                message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void noContent(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "データなし");
                message.reply(ResponseUtil.createReplyObject(204, "データなし"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("取得失敗: " + code));
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
// {テーブル名}データ取得（シンプル）
String param = "{TABLENAME}" + ParamBuilder.setParam("{key}", "{value}");
new DataAccess(container, vertx).getDataAPI(param,
    new CallBack("BUS_NAME", container, message) {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    message.reply(ResponseUtil.convertResponse(responseData.getObject("body")));
                } else {
                    message.reply(ResponseUtil.createReplyObjectFail("取得失敗: " + code));
                }
            } catch (Exception e) {
                container.logger().error(e.getMessage());
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## PUT — CallBackPut パターン（推奨）

```java
// {テーブル名}データ更新
final String methodName = "{methodName}";
LogUtil.info(container.logger(), BUS_NAME, methodName, LogConstants.START);

String param = "{TABLENAME}";
JsonObject body = new JsonObject();
// body にデータをセット

new DataAccess(container, vertx).putDataAPI(param, body,
    new CallBackPut(methodName, container, message) {

        @Override
        public void created(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "更新成功");
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
                LogUtil.error(container.logger(), BUS_NAME, methodName, "更新失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("更新失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## DELETE — CallBackDelete パターン

```java
// {テーブル名}データ削除
final String methodName = "{methodName}";

String param = "{TABLENAME}" + ParamBuilder.setParam("{key}", "{value}");
new DataAccess(container, vertx).deleteDataAPI(param,
    new CallBackDelete(methodName, container, message) {

        @Override
        public void noContent(JsonObject responseData) {
            try {
                LogUtil.info(container.logger(), BUS_NAME, methodName, "削除成功");
                message.reply(ResponseUtil.createReplyObject(204, "削除完了"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void resourceDoesNotExist(JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "対象不在");
                message.reply(ResponseUtil.createReplyObject(40410, "対象データが存在しません"));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }

        @Override
        public void fail(int code, JsonObject responseData) {
            try {
                LogUtil.error(container.logger(), BUS_NAME, methodName, "削除失敗: code=" + code);
                message.reply(ResponseUtil.createReplyObjectFail("削除失敗: " + code));
            } catch (Exception e) {
                LogUtil.error(container.logger(), BUS_NAME, methodName, e);
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## SLkey — TreeMap パターン

```java
// マスタデータ取得（Class値→名称）
new DataAccess(container, vertx).getSLkey("{classId}",
    new CallBackSLkey() {
        @Override
        public void callBack(int code, TreeMap<String, String> map, Throwable th) {
            try {
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    // map: {Class値 → 名称}
                    JsonObject result = new JsonObject();
                    for (Map.Entry<String, String> entry : map.entrySet()) {
                        result.putString(entry.getKey(), entry.getValue());
                    }
                    message.reply(ResponseUtil.convertResponse(result));
                } else {
                    message.reply(ResponseUtil.createReplyObjectFail("SLkey 取得失敗: " + code));
                }
            } catch (Exception e) {
                container.logger().error(e.getMessage());
                message.reply(ResponseUtil.createReplyObjectFail(e));
            }
        }
    });
```

---

## レスポンス JSON 構造

```json
{
    "code": 200,
    "status": "success",
    "body": {
        "data": [ { "FIELD1": "value1", "FIELD2": "value2" }, ... ],
        "message": "successful"
    }
}
```

- `body.data` : データ配列（JsonArray）
- `body.data[i]` : 各レコード（JsonObject）
- `code` : HTTP ステータスコード
