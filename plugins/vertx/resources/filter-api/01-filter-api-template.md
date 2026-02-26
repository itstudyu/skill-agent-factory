# Filter-API Template

## Template: Basic Filter-API GET

**Use this template for all Filter-API calls.**

```java
public void methodName(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Build query string
        JsonObject body = message.body();
        String nonPlatformID = container.config().getString(ScreenConstants.NON_PLATFORM);
        
        String query = nonPlatformID + "/FILTER_NAME";
        
        // Add parameters if needed
        String param1 = JsonUtil.getString(body, "param1");
        if (!StringUtil.isNullOrEmpty(param1)) {
            query += "?param1=" + param1;
        }
        
        container.logger().debug("Filter query: " + query);
        
        // Call Filter-API
        new DataAccess(container, vertx).getFilterAPI(query,
            new CallBackGet(BUS_NAME, container, message) {
                
                @Override
                public void ok(JsonObject responseData) {
                    try {
                        // Response is JsonArray directly in body
                        message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }
                
                @Override
                public void noContent(JsonObject responseData) {
                    try {
                        // No data found
                        message.reply(responseData);
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }
            });
            
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Real Example 1: Simple Filter Query

**File**: `src/main/java/jp/co/payroll/p3/storerevampapplication/applicantlist/custom/filter/XTLGTask.java`

```java
public class XTLGTask extends BusModBase implements Handler<Message<JsonObject>> {

    public final static String BUS_NAME = Constant.APP_ID + "/XTLGTask";

    @Override
    public void handle(Message<JsonObject> message) {
        try {
            container.logger().info(BUS_NAME + LogConstants.START);
            getXTLG(message);
        } catch (Throwable th) {
            message.reply(JsonUtil.createReplyObjectFail(th));
        }
    }

    private void getXTLG(final Message<JsonObject> message) {
        final String methodName = new Throwable().getStackTrace()[0].getMethodName();

        // Get query string from request
        String query = JsonUtil.getString(message.body(), "query");

        new DataAccess(container, vertx).getFilterAPI(query,
            new CallBackGet(BUS_NAME, container, message) {

                @Override
                public void ok(JsonObject responseData) {
                    try {
                        message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }

                @Override
                public void noContent(JsonObject responseData) {
                    try {
                        message.reply(responseData);
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }
            });
    }
}
```

---

## Real Example 2: Filter with Parameters

**File**: `src/main/java/jp/co/payroll/p3/storerevampapplication/recruitmentstatuslist/custom/filter/XTLH.java`

```java
public class XTLH extends BusModBase implements Handler<Message<JsonObject>> {

    public final static String BUS_NAME = Constant.APP_ID + "/XTLH";

    @Override
    public void handle(Message<JsonObject> message) {
        try {
            container.logger().info(BUS_NAME + LogConstants.START);
            getXTLH(message);
        } catch (Throwable th) {
            message.reply(JsonUtil.createReplyObjectFail(th));
        }
    }

    private void getXTLH(final Message<JsonObject> message) {
        final String methodName = new Throwable().getStackTrace()[0].getMethodName();

        JsonObject body = message.body();
        
        // Build query with parameter
        String queryString = container.config().getString(ScreenConstants.NON_PLATFORM) + "/XTLH"
            + Util.SetParam("$platformId", JsonUtil.getString(body, "platformId"));

        new DataAccess(container, vertx).getFilterAPI(queryString,
            new CallBackGet(BUS_NAME, container, message) {

                @Override
                public void ok(JsonObject responseData) {
                    try {
                        message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }

                @Override
                public void noContent(JsonObject responseData) {
                    try {
                        message.reply(responseData);
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }
            });
    }
}
```

---

## Query String Patterns

### Pattern 1: Simple Filter (No Parameters)

```java
String nonPlatformID = container.config().getString(ScreenConstants.NON_PLATFORM);
String query = nonPlatformID + "/FILTER_NAME";

// Example: "platform123/XTLG"
```

### Pattern 2: Filter with Single Parameter

```java
String query = nonPlatformID + "/FILTER_NAME" + "?param1=" + value1;

// Example: "platform123/XTLH?platformId=abc123"
```

### Pattern 3: Filter with Multiple Parameters

```java
String query = nonPlatformID + "/FILTER_NAME" 
    + "?param1=" + value1 
    + "&param2=" + value2
    + "&param3=" + value3;

// Example: "platform123/FILTER?status=active&type=user&limit=100"
```

### Pattern 4: Using Util.SetParam Helper

```java
String query = nonPlatformID + "/FILTER_NAME"
    + Util.SetParam("$param1", value1)
    + Util.SetParam("$param2", value2);

// Util.SetParam adds "?" for first param, "&" for subsequent params
```

### Pattern 5: Conditional Parameters

```java
String query = nonPlatformID + "/FILTER_NAME";

// Add parameters conditionally
if (!StringUtil.isNullOrEmpty(param1)) {
    query += "?param1=" + param1;
}

if (!StringUtil.isNullOrEmpty(param2)) {
    query += query.contains("?") ? "&param2=" : "?param2=";
    query += param2;
}
```

---

## Response Format

### Success Response (HTTP 200)

```json
{
  "code": 200,
  "body": [
    {
      "id": "123",
      "name": "John",
      "status": "active"
    },
    {
      "id": "456",
      "name": "Jane",
      "status": "active"
    }
  ]
}
```

**Key Difference**: Response is **JsonArray directly in body**, not `body.data`

### No Content Response (HTTP 204)

```json
{
  "code": 204
}
```

---

## Response Processing

### Extract Data from Response

```java
@Override
public void ok(JsonObject responseData) {
    try {
        // Get JsonArray from body
        JsonArray results = responseData.getArray(JsonKeyConstants.BODY);
        
        // Process each item
        for (int i = 0; i < results.size(); i++) {
            JsonObject item = results.get(i);
            String id = item.getString("id");
            String name = item.getString("name");
            // ... process item
        }
        
        // Reply with results
        message.reply(results.toString());
        
    } catch (Exception e) {
        container.logger().error(methodName + LogConstants.ERROR, e);
        message.reply(new JsonObject().putNumber("code", 500));
    }
}
```

### Transform Response

```java
@Override
public void ok(JsonObject responseData) {
    try {
        JsonArray results = responseData.getArray(JsonKeyConstants.BODY);
        
        // Transform to different format
        JsonArray transformed = new JsonArray();
        for (int i = 0; i < results.size(); i++) {
            JsonObject item = results.get(i);
            
            JsonObject newItem = new JsonObject();
            newItem.putString("value", item.getString("id"));
            newItem.putString("label", item.getString("name"));
            transformed.add(newItem);
        }
        
        message.reply(transformed.toString());
        
    } catch (Exception e) {
        container.logger().error(methodName + LogConstants.ERROR, e);
        message.reply(new JsonObject().putNumber("code", 500));
    }
}
```

### Filter Response

```java
@Override
public void ok(JsonObject responseData) {
    try {
        JsonArray results = responseData.getArray(JsonKeyConstants.BODY);
        
        // Filter results
        JsonArray filtered = new JsonArray();
        for (int i = 0; i < results.size(); i++) {
            JsonObject item = results.get(i);
            
            // Only include active items
            if ("active".equals(item.getString("status"))) {
                filtered.add(item);
            }
        }
        
        message.reply(filtered.toString());
        
    } catch (Exception e) {
        container.logger().error(methodName + LogConstants.ERROR, e);
        message.reply(new JsonObject().putNumber("code", 500));
    }
}
```

---

## Error Handling

### Standard Error Handling

```java
@Override
public void ok(JsonObject responseData) {
    try {
        // Process response
        message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
    } catch (Exception e) {
        // ALWAYS catch exceptions
        container.logger().error(methodName + LogConstants.ERROR, e);
        message.reply(new JsonObject().putNumber("code", 500));
    }
}

@Override
public void noContent(JsonObject responseData) {
    try {
        // Handle no content
        message.reply(responseData);
    } catch (Exception e) {
        container.logger().error(methodName + LogConstants.ERROR, e);
        message.reply(new JsonObject().putNumber("code", 500));
    }
}

@Override
public void fail(int code, JsonObject responseData) {
    // Handle other error codes
    container.logger().error(methodName + " - Failed with code: " + code);
    super.fail(code, responseData);
}
```

### Validate Query Before Call

```java
// Validate required parameters
String param1 = JsonUtil.getString(body, "param1");
if (StringUtil.isNullOrEmpty(param1)) {
    container.logger().error(methodName + " - param1 is required");
    message.reply(new JsonObject()
        .putNumber("code", 400)
        .putString("message", "param1 is required"));
    return;
}

// Build query
String query = nonPlatformID + "/FILTER_NAME?param1=" + param1;

// Call Filter-API
da.getFilterAPI(query, callback);
```

---

## Common Patterns

### Pattern 1: Pass-Through Query

```java
// Client sends complete query string
String query = JsonUtil.getString(message.body(), "query");

da.getFilterAPI(query, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
        } catch (Exception e) {
            container.logger().error(methodName + LogConstants.ERROR, e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

### Pattern 2: Build Query from Parameters

```java
// Build query from individual parameters
JsonObject body = message.body();
String nonPlatformID = container.config().getString(ScreenConstants.NON_PLATFORM);

String query = nonPlatformID + "/FILTER_NAME"
    + "?status=" + JsonUtil.getString(body, "status")
    + "&type=" + JsonUtil.getString(body, "type");

da.getFilterAPI(query, callback);
```

### Pattern 3: Pagination

```java
// Add pagination parameters
String query = nonPlatformID + "/FILTER_NAME"
    + "?limit=" + JsonUtil.getInteger(body, "limit", 100)
    + "&offset=" + JsonUtil.getInteger(body, "offset", 0);

da.getFilterAPI(query, callback);
```

### Pattern 4: Sorting

```java
// Add sort parameters
String query = nonPlatformID + "/FILTER_NAME"
    + "?sortBy=" + JsonUtil.getString(body, "sortBy", "id")
    + "&sortOrder=" + JsonUtil.getString(body, "sortOrder", "asc");

da.getFilterAPI(query, callback);
```

---

## Checklist

Before writing Filter-API code, verify:

- [ ] Used `getFilterAPI()` method (not `getDataAPI()`)
- [ ] Used `CallBackGet` (not generic `CallBack`)
- [ ] Query format: `{nonPlatformID}/FILTER_NAME?params`
- [ ] Logged query string for debugging
- [ ] Handled both `ok()` and `noContent()` callbacks
- [ ] Wrapped callback logic in try-catch
- [ ] Response accessed as `responseData.getArray(JsonKeyConstants.BODY)`
- [ ] NOT `responseData.getObject(BODY).getArray(DATA)`
- [ ] Validated required parameters before call
- [ ] Logged errors with method name

---

## Common Mistakes

### ❌ Mistake 1: Using Wrong Response Path

```java
// WRONG: Filter-API doesn't have body.data
JsonArray data = responseData.getObject(JsonKeyConstants.BODY)
    .getArray(JsonKeyConstants.DATA);
```

### ✅ Fix: Use Correct Path

```java
// CORRECT: Response is JsonArray directly in body
JsonArray data = responseData.getArray(JsonKeyConstants.BODY);
```

### ❌ Mistake 2: Using Generic CallBack

```java
// WRONG: Should use CallBackGet
da.getFilterAPI(query, new CallBack() {
    public void callBack(int code, JsonObject responseData, Throwable th) {
        // Manual status code handling
    }
});
```

### ✅ Fix: Use CallBackGet

```java
// CORRECT: Use specialized callback
da.getFilterAPI(query, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        // Automatic 200 handling
    }
    
    @Override
    public void noContent(JsonObject responseData) {
        // Automatic 204 handling
    }
});
```

### ❌ Mistake 3: Wrong Query Format

```java
// WRONG: Using Data-API format
String query = "TABLE_NAME/" + nonPlatformID + "/" + id;
```

### ✅ Fix: Use Filter-API Format

```java
// CORRECT: Filter-API format
String query = nonPlatformID + "/FILTER_NAME?param=value";
```

### ❌ Mistake 4: Not Catching Exceptions

```java
// WRONG: No exception handling
@Override
public void ok(JsonObject responseData) {
    message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
}
```

### ✅ Fix: Always Catch Exceptions

```java
// CORRECT: Wrap in try-catch
@Override
public void ok(JsonObject responseData) {
    try {
        message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
    } catch (Exception e) {
        container.logger().error(methodName + LogConstants.ERROR, e);
        message.reply(new JsonObject().putNumber("code", 500));
    }
}
```

---

## Filter-API vs Data-API Summary

| Feature | Filter-API | Data-API |
|---------|-----------|----------|
| **Method** | `getFilterAPI(query, callback)` | `getDataAPI(param, callback)` |
| **Query Format** | `{platform}/FILTER?params` | `TABLE/{platform}/{id}` |
| **Response Path** | `body` (JsonArray) | `body.data` (JsonArray) |
| **Callback** | `CallBackGet` only | `CallBack`, `CallBackGet`, `CallBackPut`, `CallBackDelete` |
| **Operations** | GET only | GET, PUT, DELETE |
| **Use Case** | Complex filtered queries | CRUD operations |

---

**Related**: 
- Quick start: `00-quick-start.md`
- Data-API: `../data-api/01-get-templates.md`
