# Error Handling Guide

## The Golden Rule

**ALWAYS check `if (th != null)` BEFORE checking status code.**

```java
// ✅ CORRECT ORDER
if (th != null) {
    replyFail(message, th, code);
    return; // MUST return here
}

if (code == 200) {
    // Process success
}

// ❌ WRONG ORDER
if (code == 200) {
    // Process success
}
if (th != null) {
    // Too late! May have already processed invalid data
}
```

---

## Standard Error Handling Pattern

```java
da.getDataAPI(param, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            container.logger().debug(LogConstants.CODE + code);
            
            // STEP 1: Check exception FIRST
            if (th != null) {
                container.logger().error(methodName + " - Exception occurred", th);
                replyFail(message, th, code);
                return; // Stop processing
            }
            
            // STEP 2: Handle status codes
            switch (code) {
                case HttpConstants.HTTP_CODE_SUCCESS_200:
                    // Success handling
                    break;
                    
                case HttpConstants.HTTP_CODE_SUCCESS_204:
                    // No content handling
                    break;
                    
                case HttpConstants.HTTP_STATUS_CODE_NOT_FOUND:
                    // Not found handling
                    break;
                    
                case HttpConstants.HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR:
                    // Server error handling
                    break;
                    
                case HttpConstants.HTTP_STATUS_CODE_TIMEOUT_ERROR:
                    // Timeout handling
                    break;
                    
                default:
                    // Unexpected error
                    container.logger().error(methodName + " - Unexpected code: " + code);
                    JsonObject error = new JsonObject(responseData.toString());
                    error.putNumber(JsonKeyConstants.CODE, code);
                    message.reply(error);
                    break;
            }
            
        } catch (Throwable e) {
            // STEP 3: Catch any processing errors
            container.logger().error(methodName + " - Processing error", e);
            replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
        }
    }
});
```

---

## Common Error Scenarios

### Scenario 1: Network Timeout

```java
if (th != null) {
    if (code == HttpConstants.HTTP_STATUS_CODE_TIMEOUT_ERROR) {
        container.logger().error(methodName + " - Request timed out");
        
        JsonObject timeout = new JsonObject();
        timeout.putNumber("code", 900);
        timeout.putString("message", "Request timed out. Please try again.");
        message.reply(timeout);
    } else {
        replyFail(message, th, code);
    }
    return;
}
```

### Scenario 2: Resource Not Found

```java
case HttpConstants.HTTP_STATUS_CODE_NOT_FOUND:
    container.logger().warn(methodName + " - Resource not found");
    
    JsonObject notFound = new JsonObject();
    notFound.putNumber("code", 404);
    notFound.putString("message", "Resource does not exist");
    notFound.putString("resourceId", param1);
    message.reply(notFound);
    break;
```

### Scenario 3: Server Error

```java
case HttpConstants.HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR:
    container.logger().error(methodName + " - Server error: " + responseData.toString());
    
    JsonObject serverError = new JsonObject();
    serverError.putNumber("code", 500);
    serverError.putString("message", "Internal server error. Please contact support.");
    serverError.putString("timestamp", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
    message.reply(serverError);
    break;
```

### Scenario 4: Optimistic Locking Conflict

```java
case HttpConstants.HTTP_STATUS_CODE_CONFLICTS:
    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
    if (bodyObj != null && bodyObj.containsField(JsonKeyConstants.MESSAGE)) {
        JsonObject msgObj = bodyObj.getObject(JsonKeyConstants.MESSAGE);
        int errorCode = msgObj.getInteger(JsonKeyConstants.CODE);
        
        if (errorCode == HttpConstants.HTTP_STATUS_CODE_ROUSOURCE_CHANGED) {
            container.logger().warn(methodName + " - Optimistic locking conflict");
            
            JsonObject conflict = new JsonObject();
            conflict.putNumber("code", 40909);
            conflict.putString("message", "Resource was modified by another user. Please refresh and try again.");
            message.reply(conflict);
        }
    }
    break;
```

### Scenario 5: Validation Error

```java
case 400: // Bad Request
    container.logger().warn(methodName + " - Validation error");
    
    // Extract validation errors from response
    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
    JsonArray errors = bodyObj.getArray("errors");
    
    JsonObject validationError = new JsonObject();
    validationError.putNumber("code", 400);
    validationError.putString("message", "Validation failed");
    validationError.putArray("errors", errors);
    message.reply(validationError);
    break;
```

---

## Retry Logic

### Pattern: Retry on Timeout

```java
private void callWithRetry(String param, Message<JsonObject> message, int retryCount) {
    final String methodName = "callWithRetry";
    final int MAX_RETRIES = 3;
    
    final DataAccess da = new DataAccess(container, vertx);
    
    da.getDataAPI(param, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (th != null && code == HttpConstants.HTTP_STATUS_CODE_TIMEOUT_ERROR) {
                    if (retryCount < MAX_RETRIES) {
                        container.logger().warn(methodName + " - Timeout, retrying (" + (retryCount + 1) + "/" + MAX_RETRIES + ")");
                        
                        // Retry after delay
                        vertx.setTimer(1000 * retryCount, timerId -> {
                            callWithRetry(param, message, retryCount + 1);
                        });
                        return;
                    } else {
                        container.logger().error(methodName + " - Max retries exceeded");
                        JsonObject error = new JsonObject();
                        error.putNumber("code", 900);
                        error.putString("message", "Request timed out after " + MAX_RETRIES + " retries");
                        message.reply(error);
                        return;
                    }
                }
                
                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }
                
                // Process success
                if (code == 200) {
                    message.reply(responseData);
                }
                
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}

// Initial call
callWithRetry(param, message, 0);
```

---

## Logging Best Practices

### What to Log

```java
// ✅ DO: Log these
container.logger().debug(methodName + LogConstants.START);
container.logger().debug(LogConstants.PARAMETAR + param);
container.logger().debug(LogConstants.CODE + code);
container.logger().error(methodName + LogConstants.ERROR + error, exception);
container.logger().info(methodName + " - Resource created: " + id);
container.logger().warn(methodName + " - Resource not found: " + id);

// ❌ DON'T: Log these
container.logger().debug("Entering method"); // Use methodName instead
container.logger().debug("Code: " + code); // Use LogConstants
container.logger().debug(responseData.toString()); // Too verbose, log only on error
```

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| `debug` | Method entry, parameters, response codes | `container.logger().debug(methodName + LogConstants.START)` |
| `info` | Important business events | `container.logger().info("User created: " + userId)` |
| `warn` | Recoverable errors, not found | `container.logger().warn("Resource not found")` |
| `error` | Exceptions, server errors | `container.logger().error("API call failed", th)` |

---

## Error Response Format

### Standard Error Response

```java
JsonObject error = new JsonObject();
error.putNumber("code", statusCode);
error.putString("message", "Human-readable error message");
error.putString("timestamp", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
error.putString("path", param);

// Optional: Add details
error.putString("errorType", "VALIDATION_ERROR");
error.putArray("details", errorDetails);

message.reply(error);
```

### Example Error Responses

**404 Not Found:**
```json
{
  "code": 404,
  "message": "Resource not found",
  "timestamp": "2026-02-25 10:30:45",
  "path": "USER/platform123/user456"
}
```

**400 Validation Error:**
```json
{
  "code": 400,
  "message": "Validation failed",
  "errors": [
    {"field": "email", "message": "Invalid email format"},
    {"field": "age", "message": "Must be between 18 and 100"}
  ]
}
```

**500 Server Error:**
```json
{
  "code": 500,
  "message": "Internal server error",
  "timestamp": "2026-02-25 10:30:45",
  "errorId": "ERR-2026-02-25-103045-ABC123"
}
```

---

## Checklist

Before deploying error handling code, verify:

- [ ] Check `if (th != null)` FIRST, before status code
- [ ] Call `return;` after handling exception
- [ ] Wrap entire callback in try-catch
- [ ] Handle all expected status codes (200, 204, 404, 500, 900)
- [ ] Include `default:` case for unexpected codes
- [ ] Log errors with context (method name, parameters)
- [ ] Use appropriate log levels (debug, info, warn, error)
- [ ] Return meaningful error messages to user
- [ ] Don't expose sensitive information in error messages
- [ ] Consider retry logic for timeouts
- [ ] Test with both success and failure scenarios

---

## Common Mistakes

### ❌ Mistake 1: Checking Code Before Exception

```java
// WRONG
if (code == 200) {
    // Process
}
if (th != null) {
    // Handle error
}
```

### ✅ Fix: Check Exception First

```java
// CORRECT
if (th != null) {
    replyFail(message, th, code);
    return;
}
if (code == 200) {
    // Process
}
```

### ❌ Mistake 2: Not Wrapping in Try-Catch

```java
// WRONG
public void callBack(int code, JsonObject responseData, Throwable th) {
    if (th != null) return;
    
    JsonObject data = responseData.getObject("body"); // May throw exception!
}
```

### ✅ Fix: Wrap in Try-Catch

```java
// CORRECT
public void callBack(int code, JsonObject responseData, Throwable th) {
    try {
        if (th != null) {
            replyFail(message, th, code);
            return;
        }
        
        JsonObject data = responseData.getObject("body");
    } catch (Throwable e) {
        replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
    }
}
```

### ❌ Mistake 3: Swallowing Exceptions

```java
// WRONG
try {
    // ... code ...
} catch (Exception e) {
    // Silent failure - no logging, no reply
}
```

### ✅ Fix: Log and Reply

```java
// CORRECT
try {
    // ... code ...
} catch (Throwable e) {
    container.logger().error(methodName + " - Error", e);
    replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
}
```

---

**Related**: 
- Status codes: `07-status-codes.md`
- Templates: `01-get-templates.md`, `02-put-templates.md`, `03-delete-templates.md`
