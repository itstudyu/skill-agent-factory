# Chaining Multiple API Calls

## When to Chain API Calls

Chain API calls when:
- Need data from first call to make second call
- Need to enrich data with related information
- Need to perform sequential operations (GET → PUT → DELETE)
- Need to validate before performing action

---

## Template: Sequential GET Calls

**Use this to fetch related data.**

```java
public void methodName(String param1, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    // First API call
    String param1st = "TABLE1/" + nonPlatformID + "/" + param1;
    
    da.getDataAPI(param1st, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }
                
                if (code != HttpConstants.HTTP_CODE_SUCCESS_200) {
                    message.reply(responseData);
                    return;
                }
                
                // Extract data from first call
                JsonObject firstData = responseData.getObject(JsonKeyConstants.BODY)
                    .getArray(JsonKeyConstants.DATA)
                    .get(0);
                
                String relatedId = firstData.getString("relatedId");
                
                // Second API call
                String param2nd = "TABLE2/" + nonPlatformID + "/" + relatedId;
                
                da.getDataAPI(param2nd, new CallBack() {
                    @Override
                    public void callBack(int code2, JsonObject responseData2, Throwable th2) {
                        try {
                            if (th2 != null) {
                                // Return first data even if second call fails
                                container.logger().warn(methodName + " - Second call failed, returning partial data");
                                message.reply(firstData);
                                return;
                            }
                            
                            if (code2 == HttpConstants.HTTP_CODE_SUCCESS_200) {
                                JsonObject secondData = responseData2.getObject(JsonKeyConstants.BODY)
                                    .getArray(JsonKeyConstants.DATA)
                                    .get(0);
                                
                                // Merge data
                                firstData.putObject("relatedData", secondData);
                            }
                            
                            message.reply(firstData);
                            
                        } catch (Throwable e) {
                            container.logger().error(methodName + " - Error in second call", e);
                            message.reply(firstData); // Return partial data
                        }
                    }
                });
                
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}
```

---

## Template: GET → Validate → PUT

**Use this to validate before updating.**

```java
public void methodName(String id, JsonObject updateData, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    // Step 1: GET current data
    String getParam = "TABLE/" + nonPlatformID + "/" + id;
    
    da.getDataAPI(getParam, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }
                
                if (code != HttpConstants.HTTP_CODE_SUCCESS_200) {
                    message.reply(responseData);
                    return;
                }
                
                JsonObject currentData = responseData.getObject(JsonKeyConstants.BODY)
                    .getArray(JsonKeyConstants.DATA)
                    .get(0);
                
                // Step 2: Validate
                boolean canUpdate = currentData.getBoolean("canUpdate", true);
                String status = currentData.getString("status");
                
                if (!canUpdate || "LOCKED".equals(status)) {
                    JsonObject error = new JsonObject();
                    error.putNumber("code", 400);
                    error.putString("message", "Resource cannot be updated");
                    message.reply(error);
                    return;
                }
                
                // Step 3: PUT update
                String putParam = "TABLE/" + nonPlatformID + "/" + id;
                
                JsonObject body = new JsonObject();
                body.putString("field1", updateData.getString("field1"));
                body.putString("field2", updateData.getString("field2"));
                
                da.putDataAPI(putParam, body, new CallBack() {
                    @Override
                    public void callBack(int code2, JsonObject responseData2, Throwable th2) {
                        try {
                            if (th2 != null) {
                                replyFail(message, th2, code2);
                                return;
                            }
                            
                            message.reply(responseData2);
                            
                        } catch (Throwable e) {
                            replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
                        }
                    }
                });
                
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}
```

---

## Template: GET → DELETE (with Confirmation)

**Use this to check before deleting.**

```java
public void methodName(String id, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    // Step 1: GET to check if exists
    String getParam = "TABLE/" + nonPlatformID + "/" + id;
    
    da.getDataAPI(getParam, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }
                
                if (code == HttpConstants.HTTP_CODE_SUCCESS_204) {
                    // Resource doesn't exist
                    JsonObject notFound = new JsonObject();
                    notFound.putNumber("code", 404);
                    notFound.putString("message", "Resource not found");
                    message.reply(notFound);
                    return;
                }
                
                if (code != HttpConstants.HTTP_CODE_SUCCESS_200) {
                    message.reply(responseData);
                    return;
                }
                
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
                
                // Step 2: DELETE
                String deleteParam = "TABLE/" + nonPlatformID + "/" + id;
                
                da.deleteDataAPI(deleteParam, new CallBack() {
                    @Override
                    public void callBack(int code2, JsonObject responseData2, Throwable th2) {
                        try {
                            if (th2 != null) {
                                replyFail(message, th2, code2);
                                return;
                            }
                            
                            if (code2 == HttpConstants.HTTP_CODE_SUCCESS_204) {
                                JsonObject result = new JsonObject();
                                result.putNumber("code", 204);
                                result.putString("message", "Deleted successfully");
                                message.reply(result);
                            } else {
                                message.reply(responseData2);
                            }
                            
                        } catch (Throwable e) {
                            replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
                        }
                    }
                });
                
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}
```

---

## Template: Multiple Parallel Fetches (Using Counter)

**Use this to fetch multiple independent resources.**

```java
public void methodName(List<String> ids, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    final JsonArray results = new JsonArray();
    final AtomicInteger counter = new AtomicInteger(ids.size());
    final AtomicBoolean hasError = new AtomicBoolean(false);
    
    for (String id : ids) {
        String param = "TABLE/" + nonPlatformID + "/" + id;
        
        da.getDataAPI(param, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    if (th == null && code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                        JsonObject data = responseData.getObject(JsonKeyConstants.BODY)
                            .getArray(JsonKeyConstants.DATA)
                            .get(0);
                        
                        synchronized (results) {
                            results.add(data);
                        }
                    } else {
                        hasError.set(true);
                    }
                    
                    // Check if all calls completed
                    if (counter.decrementAndGet() == 0) {
                        if (hasError.get()) {
                            JsonObject error = new JsonObject();
                            error.putNumber("code", 500);
                            error.putString("message", "Some requests failed");
                            error.putArray("partialResults", results);
                            message.reply(error);
                        } else {
                            JsonObject result = new JsonObject();
                            result.putNumber("code", 200);
                            result.putArray("data", results);
                            message.reply(result);
                        }
                    }
                    
                } catch (Throwable e) {
                    container.logger().error(methodName + " - Error", e);
                    hasError.set(true);
                    
                    if (counter.decrementAndGet() == 0) {
                        replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
                    }
                }
            }
        });
    }
}
```

---

## Common Patterns

### Pattern 1: Graceful Degradation

```java
// If second call fails, return first data anyway
if (th2 != null) {
    container.logger().warn("Second call failed, returning partial data");
    message.reply(firstData); // Return what we have
    return;
}
```

### Pattern 2: Early Return on Error

```java
if (code != HttpConstants.HTTP_CODE_SUCCESS_200) {
    message.reply(responseData); // Don't proceed to second call
    return;
}
```

### Pattern 3: Data Enrichment

```java
// Add related data to main object
firstData.putObject("department", departmentData);
firstData.putObject("manager", managerData);
firstData.putArray("projects", projectsArray);
```

### Pattern 4: Conditional Chaining

```java
// Only fetch related data if flag is set
if (firstData.getBoolean("hasRelatedData", false)) {
    // Make second call
} else {
    // Return first data only
    message.reply(firstData);
}
```

---

## Best Practices

### ✅ DO: Handle Partial Failures

```java
if (th2 != null) {
    // Log error but return partial data
    container.logger().warn("Related data fetch failed: " + th2.getMessage());
    message.reply(firstData);
    return;
}
```

### ✅ DO: Use Meaningful Variable Names

```java
// Good: Clear what each variable represents
JsonObject userData = ...;
JsonObject departmentData = ...;
JsonObject projectData = ...;

// Bad: Unclear naming
JsonObject data1 = ...;
JsonObject data2 = ...;
JsonObject data3 = ...;
```

### ✅ DO: Log Each Step

```java
container.logger().debug(methodName + " - Step 1: Fetching user data");
// ... first call ...

container.logger().debug(methodName + " - Step 2: Fetching department data");
// ... second call ...

container.logger().debug(methodName + " - Step 3: Merging data");
```

### ❌ DON'T: Chain More Than 3 Levels

```java
// Bad: Too deeply nested (hard to read and maintain)
da.getDataAPI(param1, new CallBack() {
    public void callBack(...) {
        da.getDataAPI(param2, new CallBack() {
            public void callBack(...) {
                da.getDataAPI(param3, new CallBack() {
                    public void callBack(...) {
                        da.getDataAPI(param4, new CallBack() {
                            // This is too deep!
                        });
                    }
                });
            }
        });
    }
});

// Good: Extract to separate methods
fetchUserData(id, message);

private void fetchUserData(String id, Message<JsonObject> message) {
    // First call
}

private void fetchDepartmentData(String deptId, JsonObject userData, Message<JsonObject> message) {
    // Second call
}
```

---

## Checklist

Before writing chained API calls, verify:

- [ ] Each call checks `if (th != null)` FIRST
- [ ] Each call has try-catch wrapper
- [ ] Early return on error (don't proceed if first call fails)
- [ ] Graceful degradation (return partial data if possible)
- [ ] Logged each step for debugging
- [ ] Used meaningful variable names
- [ ] Not nested more than 3 levels deep
- [ ] Considered extracting to separate methods
- [ ] Handled all expected status codes
- [ ] Tested with both success and failure scenarios

---

**Related**: 
- GET templates: `01-get-templates.md`
- PUT templates: `02-put-templates.md`
- DELETE templates: `03-delete-templates.md`
- Error handling: `06-error-handling.md`
