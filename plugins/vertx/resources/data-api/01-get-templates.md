# GET Request Templates

## Template 1: Basic GET with CallBack

**Use this for custom logic and data processing.**

```java
public void methodName(String param1, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    // Build parameter
    String param = "TABLE_NAME/" + nonPlatformID + "/" + param1;
    
    // Add query parameters if needed
    if (!StringUtil.isNullOrEmpty(optionalParam)) {
        param += "?_lang=" + optionalParam;
    }
    
    container.logger().debug(LogConstants.PARAMETAR + param);
    
    da.getDataAPI(param, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                container.logger().debug(LogConstants.CODE + code);
                
                // STEP 1: Check exception FIRST
                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }
                
                // STEP 2: Handle status codes
                switch (code) {
                    case HttpConstants.HTTP_CODE_SUCCESS_200:
                        container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                        
                        JsonArray ja = responseData.getObject(JsonKeyConstants.BODY)
                            .getArray(JsonKeyConstants.DATA);
                        
                        // Process data here
                        if (ja.size() > 0) {
                            JsonObject result = ja.get(0);
                            message.reply(result);
                        } else {
                            message.reply(new JsonObject().putNumber("code", 204));
                        }
                        break;
                        
                    case HttpConstants.HTTP_CODE_SUCCESS_204:
                        container.logger().debug(methodName + " - No content");
                        message.reply(new JsonObject().putNumber("code", 204));
                        break;
                        
                    default:
                        JsonObject joErr = new JsonObject(responseData.toString());
                        joErr.putNumber(JsonKeyConstants.CODE, code);
                        container.logger().error(methodName + LogConstants.ERROR + joErr);
                        message.reply(joErr);
                        break;
                }
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}
```

---

## Template 2: GET with CallBackGet (Auto-Reply)

**Use this when you want automatic response handling.**

```java
public void methodName(String param1, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    String param = "TABLE_NAME/" + nonPlatformID + "/" + param1;
    
    container.logger().debug(LogConstants.PARAMETAR + param);
    
    da.getDataAPI(param, new CallBackGet(methodName, container, message) {
        @Override
        public void ok(JsonObject responseData) {
            // HTTP 200: Process successful response
            container.logger().debug(methodName + " - Success");
            
            JsonArray data = responseData.getObject(JsonKeyConstants.BODY)
                .getArray(JsonKeyConstants.DATA);
            
            // Optional: Process data before auto-reply
            // ...
            
            super.ok(responseData); // Automatically replies to message
        }
        
        @Override
        public void noContent(JsonObject responseData) {
            // HTTP 204: No data found
            container.logger().debug(methodName + " - No content");
            super.noContent(responseData);
        }
        
        @Override
        public void fail(int code, JsonObject responseData) {
            // Other error codes
            container.logger().error(methodName + " - Failed with code: " + code);
            super.fail(code, responseData);
        }
    });
}
```

---

## When to Use Which Template

| Scenario | Template | Reason |
|----------|----------|--------|
| Need custom data processing | Template 1 (CallBack) | Full control over response |
| Simple pass-through | Template 2 (CallBackGet) | Automatic reply handling |
| Need to transform data | Template 1 (CallBack) | Can modify before replying |
| Just fetch and return | Template 2 (CallBackGet) | Less boilerplate |

---

## Real Example from Codebase

**File**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/formal/CustomFormal_H101_base.java`  
**Line**: 141

```java
private void getMCAP(final Message<JsonObject> message, final ParamObject paramObj) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);

    String param = "MCAP/" + paramObj.nonPlatformID + "/" + Constant.APP_ID + "/COM";
    if (!StringUtil.isNullOrEmpty(paramObj.lang)) {
        param += "?_lang=" + paramObj.lang;
    }

    container.logger().debug(LogConstants.PARAMETAR + param);

    paramObj.da.getDataAPI(param, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                container.logger().debug(LogConstants.CODE + code);

                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }

                switch (code) {
                    case HttpConstants.HTTP_CODE_SUCCESS_200:
                        container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());

                        JsonArray ja = responseData.getObject(JsonKeyConstants.BODY)
                            .getArray(JsonKeyConstants.DATA);

                        for (int i = 0; i < ja.size(); i++) {
                            JsonObject jo = ja.get(i);
                            paramObj.mcapMap = JsonUtil.getAsMap05(jo, "MCAPP");
                        }

                        respCreate(message, JsonUtil.getAsString05(paramObj.mcapMap, 5, "MCAPP01"));
                        break;

                    default:
                        JsonObject joErr = new JsonObject(responseData.toString());
                        joErr.putNumber(JsonKeyConstants.CODE, code);
                        container.logger().error(methodName + LogConstants.ERROR + joErr);
                        message.reply(joErr);
                        break;
                }
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}
```

---

## Common Patterns

### Pattern 1: GET with Query Parameters

```java
String param = "TABLE/" + nonPlatformID + "/" + id;

// Add single query parameter
param += "?_lang=" + lang;

// Add multiple query parameters
param += "?_lang=" + lang + "&_format=json";
```

### Pattern 2: Extract Data from Response

```java
JsonArray ja = responseData.getObject(JsonKeyConstants.BODY)
    .getArray(JsonKeyConstants.DATA);

if (ja.size() > 0) {
    JsonObject firstItem = ja.get(0);
    String value = firstItem.getString("fieldName");
}
```

### Pattern 3: Handle Empty Response

```java
case HttpConstants.HTTP_CODE_SUCCESS_200:
    JsonArray ja = responseData.getObject(JsonKeyConstants.BODY)
        .getArray(JsonKeyConstants.DATA);
    
    if (ja.size() == 0) {
        // No data found
        JsonObject empty = new JsonObject();
        empty.putNumber("code", 204);
        empty.putString("message", "No data found");
        message.reply(empty);
    } else {
        // Process data
        message.reply(ja.get(0));
    }
    break;
```

---

## Checklist

Before writing GET request code, verify:

- [ ] Used `final DataAccess da = new DataAccess(container, vertx)`
- [ ] Built param as `"TABLE/" + nonPlatformID + "/" + id`
- [ ] Logged param: `container.logger().debug(LogConstants.PARAMETAR + param)`
- [ ] Checked `if (th != null)` FIRST
- [ ] Called `return;` after handling exception
- [ ] Wrapped callback in `try-catch`
- [ ] Handled HTTP 200 and 204
- [ ] Included `default:` case
- [ ] Checked array size before accessing: `if (ja.size() > 0)`
- [ ] Logged response code: `container.logger().debug(LogConstants.CODE + code)`

---

**Related**: 
- Error handling: `06-error-handling.md`
- Status codes: `07-status-codes.md`
- SLkey (master data): `04-slkey-template.md`
