# DELETE Request Templates

## Template 1: Basic DELETE with CallBack

**Use this for custom logic and confirmation.**

```java
public void methodName(String param1, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    // Validate input
    if (StringUtil.isNullOrEmpty(param1)) {
        replyFail(message, new Throwable("Parameter required"), HttpConstants.HTTP_CODE_ERROR);
        return;
    }
    
    final DataAccess da = new DataAccess(container, vertx);
    
    String param = "TABLE_NAME/" + nonPlatformID + "/" + param1;
    
    container.logger().debug(LogConstants.PARAMETAR + param);
    container.logger().info(methodName + " - Deleting resource: " + param1);
    
    da.deleteDataAPI(param, new CallBack() {
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
                    case HttpConstants.HTTP_CODE_SUCCESS_204:
                        container.logger().info(methodName + " - Resource deleted successfully");
                        JsonObject result = new JsonObject();
                        result.putNumber("code", 204);
                        result.putString("message", "Deleted successfully");
                        message.reply(result);
                        break;
                        
                    case HttpConstants.HTTP_STATUS_CODE_NOT_FOUND:
                        container.logger().warn(methodName + " - Resource not found");
                        JsonObject notFound = new JsonObject();
                        notFound.putNumber("code", 404);
                        notFound.putString("message", "Resource does not exist");
                        message.reply(notFound);
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

## Template 2: DELETE with CallBackDelete (Auto-Reply)

**Use this for standard delete with automatic handling.**

```java
public void methodName(String param1, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    String param = "TABLE_NAME/" + nonPlatformID + "/" + param1;
    
    container.logger().debug(LogConstants.PARAMETAR + param);
    
    da.deleteDataAPI(param, new CallBackDelete(methodName, container, message) {
        @Override
        public void noContent(JsonObject responseData) {
            // HTTP 204: Successfully deleted
            container.logger().info(methodName + " - Resource deleted");
            super.noContent(responseData);
        }
        
        @Override
        public void resourceDoesNotExits(JsonObject responseData) {
            // HTTP 404: Resource not found
            container.logger().warn(methodName + " - Resource not found");
            super.resourceDoesNotExits(responseData);
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
| Need custom confirmation | Template 1 (CallBack) | Can add custom messages |
| Need to log deleted data | Template 1 (CallBack) | Full control over response |
| Standard delete | Template 2 (CallBackDelete) | Automatic reply handling |
| Simple pass-through | Template 2 (CallBackDelete) | Less boilerplate |

---

## Common Patterns

### Pattern 1: Soft Delete (Update Instead of Delete)

```java
// Instead of DELETE, use PUT to mark as deleted
public void softDelete(String id, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    
    String param = "TABLE/" + nonPlatformID + "/" + id;
    
    JsonObject body = new JsonObject();
    body.putBoolean("deleted", true);
    body.putString("deletedAt", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
    body.putString("deletedBy", container.config().getString("currentUser"));
    
    da.putDataAPI(param, body, new CallBack() {
        // Handle response
    });
}
```

### Pattern 2: Cascade Delete (Delete Related Records)

```java
public void deleteWithRelated(String id, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    
    // First, delete related records
    String relatedParam = "RELATED_TABLE/" + nonPlatformID + "/" + id;
    
    da.deleteDataAPI(relatedParam, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            // Ignore if related records don't exist
            if (th != null && code != 404) {
                replyFail(message, th, code);
                return;
            }
            
            // Then, delete main record
            String mainParam = "MAIN_TABLE/" + nonPlatformID + "/" + id;
            
            da.deleteDataAPI(mainParam, new CallBack() {
                @Override
                public void callBack(int code2, JsonObject responseData2, Throwable th2) {
                    try {
                        if (th2 != null) {
                            replyFail(message, th2, code2);
                            return;
                        }
                        
                        if (code2 == HttpConstants.HTTP_CODE_SUCCESS_204) {
                            message.reply(new JsonObject().putNumber("code", 204));
                        } else {
                            message.reply(responseData2);
                        }
                    } catch (Throwable e) {
                        replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
                    }
                }
            });
        }
    });
}
```

### Pattern 3: Conditional Delete (Check Before Delete)

```java
public void conditionalDelete(String id, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    
    // First, check if resource exists and can be deleted
    String getParam = "TABLE/" + nonPlatformID + "/" + id;
    
    da.getDataAPI(getParam, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }
                
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    JsonObject data = responseData.getObject(JsonKeyConstants.BODY)
                        .getArray(JsonKeyConstants.DATA)
                        .get(0);
                    
                    // Check if can be deleted
                    boolean canDelete = data.getBoolean("canDelete", true);
                    
                    if (!canDelete) {
                        JsonObject error = new JsonObject();
                        error.putNumber("code", 400);
                        error.putString("message", "Resource cannot be deleted");
                        message.reply(error);
                        return;
                    }
                    
                    // Proceed with delete
                    String deleteParam = "TABLE/" + nonPlatformID + "/" + id;
                    da.deleteDataAPI(deleteParam, new CallBack() {
                        @Override
                        public void callBack(int code2, JsonObject responseData2, Throwable th2) {
                            // Handle delete response
                        }
                    });
                } else {
                    message.reply(responseData);
                }
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}
```

---

## HTTP Status Codes for DELETE

| Code | Meaning | Action |
|------|---------|--------|
| 204 | No Content | Resource successfully deleted |
| 404 | Not Found | Resource does not exist |
| 40410 | Resource Not Exist | Specific error for missing resource |
| 400 | Bad Request | Invalid request (e.g., missing ID) |
| 409 | Conflict | Resource cannot be deleted (has dependencies) |
| 500 | Server Error | Internal server error |

---

## Checklist

Before writing DELETE request code, verify:

- [ ] Used `final DataAccess da = new DataAccess(container, vertx)`
- [ ] Validated required parameters before API call
- [ ] Built param as `"TABLE/" + nonPlatformID + "/" + id`
- [ ] Logged param: `container.logger().debug(LogConstants.PARAMETAR + param)`
- [ ] Logged delete action: `container.logger().info(methodName + " - Deleting resource: " + id)`
- [ ] Checked `if (th != null)` FIRST
- [ ] Called `return;` after handling exception
- [ ] Wrapped callback in `try-catch`
- [ ] Handled HTTP 204 (No Content)
- [ ] Handled HTTP 404 (Not Found)
- [ ] Included `default:` case
- [ ] Logged response code: `container.logger().debug(LogConstants.CODE + code)`

---

## Common Mistakes

### ❌ Bad: Not Handling 404

```java
switch (code) {
    case 204:
        message.reply(new JsonObject().putNumber("code", 204));
        break;
    // Missing 404 handling - what if resource doesn't exist?
}
```

### ✅ Good: Handle Not Found

```java
switch (code) {
    case HttpConstants.HTTP_CODE_SUCCESS_204:
        message.reply(new JsonObject().putNumber("code", 204));
        break;
    case HttpConstants.HTTP_STATUS_CODE_NOT_FOUND:
        JsonObject notFound = new JsonObject();
        notFound.putNumber("code", 404);
        notFound.putString("message", "Resource not found");
        message.reply(notFound);
        break;
    default:
        message.reply(responseData);
        break;
}
```

### ❌ Bad: Not Logging Delete Actions

```java
// Missing audit log
da.deleteDataAPI(param, callback);
```

### ✅ Good: Log Important Actions

```java
container.logger().info(methodName + " - Deleting resource: " + id);
container.logger().info("User: " + container.config().getString("currentUser"));

da.deleteDataAPI(param, callback);
```

---

## Delete vs Soft Delete

| Aspect | Hard Delete (DELETE API) | Soft Delete (PUT API) |
|--------|-------------------------|----------------------|
| Data | Permanently removed | Marked as deleted |
| Recovery | Not possible | Can be restored |
| Audit | Harder to track | Full audit trail |
| Performance | Frees up space | Data accumulates |
| Use Case | Test data, temp files | User data, business records |

**Recommendation**: Use soft delete for business-critical data, hard delete for temporary/test data.

---

**Related**: 
- Error handling: `06-error-handling.md`
- Status codes: `07-status-codes.md`
- PUT templates: `02-put-templates.md` (for soft delete)
