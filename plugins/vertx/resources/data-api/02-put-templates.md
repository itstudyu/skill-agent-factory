# PUT Request Templates

## Template 1: Basic PUT with CallBack

**Use this for custom logic and validation.**

```java
public void methodName(String param1, JsonObject inputData, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    // Validate input
    if (StringUtil.isNullOrEmpty(param1)) {
        replyFail(message, new Throwable("Parameter required"), HttpConstants.HTTP_CODE_ERROR);
        return;
    }
    
    final DataAccess da = new DataAccess(container, vertx);
    
    String param = "TABLE_NAME/" + nonPlatformID + "/" + param1;
    
    // Build request body
    JsonObject body = new JsonObject();
    body.putString("field1", inputData.getString("field1"));
    body.putString("field2", inputData.getString("field2"));
    body.putNumber("field3", inputData.getInteger("field3"));
    
    container.logger().debug(LogConstants.PARAMETAR + param);
    container.logger().debug("Request body: " + body.toString());
    
    da.putDataAPI(param, body, new CallBack() {
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
                    case HttpConstants.HTTP_CODE_SUCCESS_201:
                        container.logger().info(methodName + " - Resource created/updated");
                        message.reply(responseData);
                        break;
                        
                    case HttpConstants.HTTP_STATUS_CODE_CONFLICTS:
                        // Resource already changed (optimistic locking)
                        container.logger().warn(methodName + " - Resource already changed");
                        JsonObject conflict = new JsonObject();
                        conflict.putNumber("code", code);
                        conflict.putString("message", "Resource was modified by another user");
                        message.reply(conflict);
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

## Template 2: PUT with CallBackPut (Auto-Reply)

**Use this for standard create/update with automatic handling.**

```java
public void methodName(String param1, JsonObject inputData, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    String param = "TABLE_NAME/" + nonPlatformID + "/" + param1;
    
    JsonObject body = new JsonObject();
    body.putString("field1", inputData.getString("field1"));
    body.putString("field2", inputData.getString("field2"));
    
    container.logger().debug(LogConstants.PARAMETAR + param);
    
    da.putDataAPI(param, body, new CallBackPut(methodName, container, message) {
        @Override
        public void created(JsonObject responseData) {
            // HTTP 201: Successfully created/updated
            container.logger().info(methodName + " - Resource created");
            super.created(responseData);
        }
        
        @Override
        public void resourceAlreadyChanged(JsonObject responseData) {
            // HTTP 409: Optimistic locking conflict
            container.logger().warn(methodName + " - Resource already changed");
            super.resourceAlreadyChanged(responseData);
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
| Need input validation | Template 1 (CallBack) | Can validate before API call |
| Custom conflict handling | Template 1 (CallBack) | Full control over 409 response |
| Standard create/update | Template 2 (CallBackPut) | Automatic reply handling |
| Need to log specific fields | Template 1 (CallBack) | Can access response data |

---

## Common Patterns

### Pattern 1: Input Validation

```java
// Validate required fields
if (StringUtil.isNullOrEmpty(param1)) {
    replyFail(message, new Throwable("Parameter required"), HttpConstants.HTTP_CODE_ERROR);
    return;
}

// Validate input data
if (!inputData.containsField("field1")) {
    replyFail(message, new Throwable("field1 is required"), HttpConstants.HTTP_CODE_ERROR);
    return;
}
```

### Pattern 2: Build Request Body

```java
JsonObject body = new JsonObject();

// String fields
body.putString("name", inputData.getString("name"));
body.putString("email", inputData.getString("email"));

// Number fields
body.putNumber("age", inputData.getInteger("age"));
body.putNumber("salary", inputData.getLong("salary"));

// Boolean fields
body.putBoolean("active", inputData.getBoolean("active"));

// Nested objects
JsonObject address = new JsonObject();
address.putString("city", inputData.getString("city"));
body.putObject("address", address);

// Arrays
JsonArray tags = inputData.getArray("tags");
body.putArray("tags", tags);
```

### Pattern 3: Handle Optimistic Locking

```java
case HttpConstants.HTTP_STATUS_CODE_CONFLICTS:
    // Check if it's optimistic locking (40909)
    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
    if (bodyObj != null && bodyObj.containsField(JsonKeyConstants.MESSAGE)) {
        JsonObject msgObj = bodyObj.getObject(JsonKeyConstants.MESSAGE);
        int errorCode = msgObj.getInteger(JsonKeyConstants.CODE);
        
        if (errorCode == HttpConstants.HTTP_STATUS_CODE_ROUSOURCE_CHANGED) {
            // Resource was modified by another user
            container.logger().warn(methodName + " - Optimistic locking conflict");
            JsonObject conflict = new JsonObject();
            conflict.putNumber("code", 40909);
            conflict.putString("message", "Resource was modified. Please refresh and try again.");
            message.reply(conflict);
        }
    }
    break;
```

### Pattern 4: Add Audit Fields

```java
JsonObject body = new JsonObject();
body.putString("field1", inputData.getString("field1"));
body.putString("field2", inputData.getString("field2"));

// Add audit fields
body.putString("updatedBy", container.config().getString("currentUser"));
body.putString("updatedAt", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
```

---

## HTTP Status Codes for PUT

| Code | Meaning | Action |
|------|---------|--------|
| 201 | Created | Resource successfully created/updated |
| 409 | Conflict | Resource already exists or was modified |
| 40909 | Resource Changed | Optimistic locking conflict (specific) |
| 40910 | Integrity Violation | Database constraint violation |
| 400 | Bad Request | Invalid input data |
| 500 | Server Error | Internal server error |

---

## Checklist

Before writing PUT request code, verify:

- [ ] Used `final DataAccess da = new DataAccess(container, vertx)`
- [ ] Validated required parameters before API call
- [ ] Built param as `"TABLE/" + nonPlatformID + "/" + id`
- [ ] Created JsonObject body with all required fields
- [ ] Logged param: `container.logger().debug(LogConstants.PARAMETAR + param)`
- [ ] Logged body: `container.logger().debug("Request body: " + body.toString())`
- [ ] Checked `if (th != null)` FIRST
- [ ] Called `return;` after handling exception
- [ ] Wrapped callback in `try-catch`
- [ ] Handled HTTP 201 (Created)
- [ ] Handled HTTP 409 (Conflict)
- [ ] Included `default:` case
- [ ] Logged response code: `container.logger().debug(LogConstants.CODE + code)`

---

## Common Mistakes

### ❌ Bad: Not Validating Input

```java
// Missing validation
JsonObject body = new JsonObject();
body.putString("field1", inputData.getString("field1")); // May be null!
```

### ✅ Good: Validate Before Use

```java
if (!inputData.containsField("field1") || StringUtil.isNullOrEmpty(inputData.getString("field1"))) {
    replyFail(message, new Throwable("field1 is required"), HttpConstants.HTTP_CODE_ERROR);
    return;
}

JsonObject body = new JsonObject();
body.putString("field1", inputData.getString("field1"));
```

### ❌ Bad: Not Handling Conflicts

```java
switch (code) {
    case 201:
        message.reply(responseData);
        break;
    // Missing 409 handling!
}
```

### ✅ Good: Handle All Expected Codes

```java
switch (code) {
    case HttpConstants.HTTP_CODE_SUCCESS_201:
        message.reply(responseData);
        break;
    case HttpConstants.HTTP_STATUS_CODE_CONFLICTS:
        // Handle conflict
        break;
    default:
        // Handle unexpected
        break;
}
```

---

**Related**: 
- Error handling: `06-error-handling.md`
- Status codes: `07-status-codes.md`
- GET templates: `01-get-templates.md`
