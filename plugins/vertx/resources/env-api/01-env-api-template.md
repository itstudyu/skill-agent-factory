# Env-API Template

## Template 1: Get Module Configuration

**Use this to get module configuration for async jobs.**

```java
public void getModuleConfig(String moduleId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build query
        String param = "module?name=" + moduleId;
        
        container.logger().debug("Getting env config for module: " + moduleId);
        
        da.getEnvAPI(param, new CallBackEnv(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                    
                    // Extract configuration using helper
                    JsonObject config = ApiUtil.getEnvParams(responseData, moduleId);
                    
                    String queueName = config.getString("queue");
                    String version = config.getString("version");
                    String moduleIdFromEnv = config.getString("moduleid");
                    
                    container.logger().info("Module config - Queue: " + queueName + ", Version: " + version);
                    
                    // Return configuration
                    JsonObject result = new JsonObject();
                    result.putNumber("code", 200);
                    result.putString("queueName", queueName);
                    result.putString("version", version);
                    result.putString("moduleId", moduleIdFromEnv);
                    message.reply(result);
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void fail(int code, JsonObject responseData) {
                container.logger().error(methodName + " - Failed: " + code);
                message.reply(responseData);
            }
        });
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Template 2: Get Config for Async Job (Complete Pattern)

**Use this pattern from AsyncJob.java - get env then submit job.**

```java
public void submitJobWithEnv(String moduleId, String params, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Step 1: Get environment configuration
        String envParam = "module?name=" + moduleId;
        
        da.getEnvAPI(envParam, new CallBackEnv(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().debug(methodName + " - Env config retrieved");
                    
                    // Extract config
                    JsonObject config = ApiUtil.getEnvParams(responseData, moduleId);
                    String queueName = config.getString("queue");
                    String version = config.getString("version");
                    
                    // Step 2: Submit async job with config
                    JsonObject jobBody = new JsonObject();
                    jobBody.putString("queueName", queueName);
                    jobBody.putString("moduleId", moduleId);
                    jobBody.putString("moduleVersion", version);
                    jobBody.putString("mode", "0");
                    jobBody.putString("param", params);
                    
                    da.postAsyncAPI("job", jobBody, new CallBackAsync(BUS_NAME, container, message) {
                        @Override
                        public void created(JsonObject asyncResponse) {
                            container.logger().info("Job submitted successfully");
                            message.reply(asyncResponse);
                        }
                        
                        @Override
                        public void fail(int code, JsonObject asyncResponse) {
                            container.logger().error("Job submission failed: " + code);
                            message.reply(asyncResponse);
                        }
                    });
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void fail(int code, JsonObject responseData) {
                container.logger().error(methodName + " - Env API failed: " + code);
                message.reply(responseData);
            }
        });
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Real Example from Codebase

**File**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/AsyncJob.java`  
**Line**: 87

```java
private void getEnv(final Message<JsonObject> message, final Param prm,
        final CallBackAsync callback) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);

    if (!StringUtil.isNullOrEmpty(prm.queueName)
            && !StringUtil.isNullOrEmpty(prm.moduleVersion)) {
        // Queue name and version already specified - skip EnvAPI
        postAsync(message, prm, callback);
    } else {
        // Get queue name and version from EnvAPI
        new DataAccess(container, vertx).getEnvAPI(prm.getEnvParam(),
            new CallBackEnv(methodName, container, message) {

                @Override
                public void ok(JsonObject responseData) {
                    try {
                        container.logger()
                            .debug(methodName + LogConstants.RETURN + responseData.toString());
                        
                        // Set env config and proceed to job submission
                        postAsync(message, prm.setEnv(responseData), callback);
                        
                    } catch (Throwable e) {
                        container.logger().error(e.getMessage());
                        message.reply(JsonUtil.createReplyObjectFail(e));
                    }
                }

                @Override
                public void fail(int code, JsonObject responseData) {
                    try {
                        container.logger()
                            .error(methodName + LogConstants.RETURN + responseData.toString());
                        callback.fail(code, responseData);
                    } catch (Throwable e) {
                        container.logger().error(e.getMessage());
                        message.reply(JsonUtil.createReplyObjectFail(e));
                    }
                }
            });
    }
}
```

---

## Helper Methods

### ApiUtil.getEnvParams()

**Extract configuration from nested response structure.**

```java
// Method 1: Get "output" field (deprecated)
JsonObject config = ApiUtil.getEnvParams(responseData);

// Method 2: Get specific field by name (recommended)
JsonObject config = ApiUtil.getEnvParams(responseData, "module-id");

// Method 3: Get specific field with group
JsonObject config = ApiUtil.getEnvParams(responseData, "module-id", "group-id");
```

**Implementation** (from ApiUtil.java):

```java
// Get output field (deprecated)
public static JsonObject getEnvParams(JsonObject res) {
    JsonObject ret;
    ret = ((JsonObject) res.getObject(JsonKeyConstants.BODY)
        .getArray(JsonKeyConstants.DATA).get(0))
        .getObject("output").getObject("z");
    return ret;
}

// Get specific field
public static JsonObject getEnvParams(JsonObject res, String name) {
    JsonObject ret;
    ret = ((JsonObject) res.getObject(JsonKeyConstants.BODY)
        .getArray(JsonKeyConstants.DATA).get(0))
        .getObject(name).getObject("z");
    return ret;
}

// Get with group
public static JsonObject getEnvParams(JsonObject res, String name, String id) {
    JsonObject ret;
    ret = ((JsonObject) res.getObject(JsonKeyConstants.BODY)
        .getArray(JsonKeyConstants.DATA).get(0))
        .getObject(name).getObject(id);
    return ret;
}
```

---

## Common Patterns

### Pattern 1: Cache Configuration

```java
// Cache env config to avoid repeated API calls
private static Map<String, JsonObject> envCache = new HashMap<>();

public void getCachedEnvConfig(String moduleId, final Message<JsonObject> message) {
    // Check cache first
    if (envCache.containsKey(moduleId)) {
        JsonObject cached = envCache.get(moduleId);
        message.reply(cached);
        return;
    }
    
    // Fetch from API
    final DataAccess da = new DataAccess(container, vertx);
    String param = "module?name=" + moduleId;
    
    da.getEnvAPI(param, new CallBackEnv(BUS_NAME, container, message) {
        @Override
        public void ok(JsonObject responseData) {
            JsonObject config = ApiUtil.getEnvParams(responseData, moduleId);
            
            // Store in cache
            envCache.put(moduleId, config);
            
            message.reply(config);
        }
    });
}
```

### Pattern 2: Conditional Env Fetch

```java
// Only fetch env if queue name not provided
if (StringUtil.isNullOrEmpty(queueName)) {
    // Fetch from Env-API
    da.getEnvAPI(param, callback);
} else {
    // Use provided queue name
    proceedWithJob(queueName, version);
}
```

### Pattern 3: Multiple Module Configs

```java
// Get configs for multiple modules
public void getMultipleConfigs(List<String> moduleIds, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    final JsonObject allConfigs = new JsonObject();
    final AtomicInteger counter = new AtomicInteger(moduleIds.size());
    
    for (String moduleId : moduleIds) {
        String param = "module?name=" + moduleId;
        
        da.getEnvAPI(param, new CallBackEnv(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                JsonObject config = ApiUtil.getEnvParams(responseData, moduleId);
                
                synchronized (allConfigs) {
                    allConfigs.putObject(moduleId, config);
                }
                
                if (counter.decrementAndGet() == 0) {
                    message.reply(allConfigs);
                }
            }
        });
    }
}
```

---

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Configuration retrieved successfully |
| 404 | Not Found | Module configuration not found |
| 500 | Server Error | Internal error |

---

## Response Format

### Raw Response

```json
{
  "code": 200,
  "body": {
    "data": [
      {
        "module-id": {
          "z": {
            "queue": "queue-name",
            "version": "1.0.0",
            "moduleid": "module-id",
            "timeout": "30000"
          }
        }
      }
    ]
  }
}
```

### Extracted Config

```json
{
  "queue": "queue-name",
  "version": "1.0.0",
  "moduleid": "module-id",
  "timeout": "30000"
}
```

---

## Checklist

Before writing Env-API code, verify:

- [ ] Used `getEnvAPI()` method
- [ ] Used `CallBackEnv` callback
- [ ] Query format: `module?name={moduleId}`
- [ ] Used `ApiUtil.getEnvParams()` to extract config
- [ ] Handled both `ok()` and `fail()` callbacks
- [ ] Wrapped callback logic in try-catch
- [ ] Logged module ID being queried
- [ ] Considered caching config for repeated use

---

**Related**: 
- Quick start: `00-quick-start.md`
- Complete template: `01-env-api-template.md`
- Async-API: `../async-api/01-async-api-template.md`
