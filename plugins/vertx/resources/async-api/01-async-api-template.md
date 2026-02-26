# Async-API Template

## Template 1: Using AsyncJob Helper (Recommended)

**Use this for most async job submissions.**

```java
public void methodName(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        JsonObject body = message.body();
        
        // Extract parameters
        String platformId = JsonUtil.getString(body, "platformId");
        String param1 = JsonUtil.getString(body, "param1");
        String param2 = JsonUtil.getString(body, "param2");
        
        // Build async parameters (space-separated)
        String asyncParams = Util.makeAsyncParam(platformId, param1, param2);
        
        // Submit job using AsyncJob helper
        new AsyncJob(container, vertx).exec(message,
            new AsyncJob.Param("module-id", asyncParams, AsyncJob.RunMode.Run),
            new CallBackAsync(BUS_NAME, container, message) {
                
                @Override
                public void created(JsonObject responseData) {
                    try {
                        container.logger().info(methodName + " - Job created successfully");
                        container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                        
                        // Extract jobId
                        String jobId = responseData.getObject("body")
                            .getObject("data")
                            .getString("jobId");
                        
                        container.logger().info("JobID: " + jobId);
                        
                        // Reply with success
                        message.reply(createReplyObject(201, "Job submitted", container));
                        
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(JsonUtil.createReplyObjectFail(e));
                    }
                }
                
                @Override
                public void exclusive(JsonObject responseData) {
                    try {
                        container.logger().warn(methodName + " - Job already running (exclusive control)");
                        message.reply(createReplyObject(40926, "Job already running", container));
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(JsonUtil.createReplyObjectFail(e));
                    }
                }
                
                @Override
                public void fail(int code, JsonObject responseData) {
                    try {
                        container.logger().error(methodName + " - Job submission failed: " + code);
                        container.logger().error(methodName + LogConstants.RETURN + responseData.toString());
                        message.reply(responseData);
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(JsonUtil.createReplyObjectFail(e));
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

## Template 2: Direct API Call (Advanced)

**Use this when you need full control over parameters.**

```java
public void methodName(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build request body
        JsonObject body = new JsonObject();
        body.putString("queueName", "queue-name");
        body.putString("moduleId", "module-id");
        body.putString("moduleVersion", "1.0.0");
        body.putString("mode", "0"); // 0=Run, 1=Deploy, 2=Exclusive
        body.putString("param", "platformId param1 param2");
        
        container.logger().debug("Async job body: " + body.toString());
        
        da.postAsyncAPI("job", body, new CallBackAsync(BUS_NAME, container, message) {
            @Override
            public void created(JsonObject responseData) {
                try {
                    container.logger().info(methodName + " - Job created");
                    message.reply(responseData);
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(JsonUtil.createReplyObjectFail(e));
                }
            }
            
            @Override
            public void exclusive(JsonObject responseData) {
                try {
                    container.logger().warn(methodName + " - Exclusive control");
                    message.reply(responseData);
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(JsonUtil.createReplyObjectFail(e));
                }
            }
            
            @Override
            public void fail(int code, JsonObject responseData) {
                try {
                    container.logger().error(methodName + " - Failed: " + code);
                    message.reply(responseData);
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(JsonUtil.createReplyObjectFail(e));
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

## Template 3: Check Job Status

**Use this to check the status of a submitted job.**

```java
public void checkJobStatus(String jobId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // GET job status
        String param = "job/" + jobId;
        
        da.getAsyncAPI(param, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    if (code == 200) {
                        JsonObject jobStatus = responseData.getObject("body")
                            .getObject("data");
                        
                        String status = jobStatus.getString("status");
                        container.logger().info("Job status: " + status);
                        
                        // Status: "running", "completed", "failed"
                        message.reply(jobStatus);
                    } else {
                        message.reply(responseData);
                    }
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(JsonUtil.createReplyObjectFail(e));
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

## Real Example from Codebase

**File**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/AsyncJob.java`

```java
public class AsyncJob extends BusModBase {

    public void exec(Message<JsonObject> message, Param prm, CallBackAsync callback) {
        getEnv(message, prm, callback);
    }

    private void getEnv(final Message<JsonObject> message, final Param prm,
            final CallBackAsync callback) {
        final String methodName = new Throwable().getStackTrace()[0].getMethodName();
        container.logger().debug(methodName + LogConstants.START);

        if (!StringUtil.isNullOrEmpty(prm.queueName)
                && !StringUtil.isNullOrEmpty(prm.moduleVersion)) {
            // Queue name and version specified - skip EnvAPI
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

    private void postAsync(final Message<JsonObject> message, final Param prm,
            final CallBackAsync callback) {
        final String methodName = Thread.currentThread().getStackTrace().clone()[1].getMethodName();
        container.logger().debug(methodName + LogConstants.START);

        new DataAccess(container, vertx).postAsyncAPI("job", prm.getAsyncParam(),
            new CallBackAsync(methodName, container, message) {

                @Override
                public void created(JsonObject responseData) {
                    try {
                        container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                        callback.created(responseData);
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR + responseData);
                        message.reply(JsonUtil.createReplyObjectFail(e));
                    }
                }

                @Override
                public void exclusive(JsonObject responseData) {
                    try {
                        container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                        callback.exclusive(responseData);
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR + responseData);
                        message.reply(JsonUtil.createReplyObjectFail(e));
                    }
                }

                @Override
                public void fail(int code, JsonObject responseData) {
                    try {
                        container.logger().error(methodName + LogConstants.RETURN + responseData.toString());
                        callback.fail(code, responseData);
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR + responseData);
                        message.reply(JsonUtil.createReplyObjectFail(e));
                    }
                }
            });
    }
}
```

---

## AsyncJob.Param Class

### Constructor

```java
new AsyncJob.Param(
    String moduleId,        // Module ID to execute
    String param,           // Parameters (space-separated)
    AsyncJob.RunMode mode   // Run mode (Run, Deploy, Exclusive)
)
```

### Optional Settings

```java
AsyncJob.Param param = new AsyncJob.Param("module-id", "params", AsyncJob.RunMode.Run)
    .setQueueName("custom-queue")      // Override queue name
    .setModuleVersion("2.0.0");        // Override module version
```

---

## Run Modes

### RunMode.Run (0)

**Normal execution** - Execute job immediately.

```java
new AsyncJob.Param("module-id", params, AsyncJob.RunMode.Run)
```

### RunMode.Deploy (1)

**Deploy only** - Deploy module without executing.

```java
new AsyncJob.Param("module-id", params, AsyncJob.RunMode.Deploy)
```

### RunMode.Exclusive (2)

**Exclusive execution** - Prevent duplicate runs.

```java
new AsyncJob.Param("module-id", params, AsyncJob.RunMode.Exclusive)
```

If job is already running, returns HTTP 40926 (exclusive control error).

---

## Parameter Building

### Using Util.makeAsyncParam

```java
// Build space-separated parameters
String params = Util.makeAsyncParam(
    platformId,
    param1,
    param2,
    param3
);

// Result: "platformId param1 param2 param3"
```

### Manual Parameter Building

```java
String params = platformId + " " + param1 + " " + param2;
```

---

## Response Handling

### Extract JobId from Response

```java
@Override
public void created(JsonObject responseData) {
    // Extract jobId
    String jobId = responseData.getObject("body")
        .getObject("data")
        .getString("jobId");
    
    container.logger().info("JobID: " + jobId);
    
    // Save jobId for status checking
    // ...
}
```

### Check Job Status

```java
// Later, check job status using jobId
da.getAsyncAPI("job/" + jobId, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        if (code == 200) {
            JsonObject status = responseData.getObject("body").getObject("data");
            String jobStatus = status.getString("status");
            
            switch (jobStatus) {
                case "running":
                    // Job is still running
                    break;
                case "completed":
                    // Job completed successfully
                    break;
                case "failed":
                    // Job failed
                    break;
            }
        }
    }
});
```

---

## Common Patterns

### Pattern 1: Submit and Forget

```java
// Submit job without waiting for completion
new AsyncJob(container, vertx).exec(message,
    new AsyncJob.Param("module-id", params, AsyncJob.RunMode.Run),
    new CallBackAsync(BUS_NAME, container, message) {
        @Override
        public void created(JsonObject responseData) {
            // Reply immediately - don't wait for job completion
            message.reply(createReplyObject(201, "Job submitted", container));
        }
    });
```

### Pattern 2: Submit and Poll

```java
// Submit job and save jobId for polling
new AsyncJob(container, vertx).exec(message,
    new AsyncJob.Param("module-id", params, AsyncJob.RunMode.Run),
    new CallBackAsync(BUS_NAME, container, message) {
        @Override
        public void created(JsonObject responseData) {
            String jobId = responseData.getObject("body")
                .getObject("data")
                .getString("jobId");
            
            // Save jobId to database or cache
            saveJobId(jobId);
            
            // Start polling (in separate handler)
            startPolling(jobId);
            
            message.reply(createReplyObject(201, "Job submitted", container));
        }
    });
```

### Pattern 3: Exclusive Execution

```java
// Prevent duplicate job execution
new AsyncJob(container, vertx).exec(message,
    new AsyncJob.Param("module-id", params, AsyncJob.RunMode.Exclusive),
    new CallBackAsync(BUS_NAME, container, message) {
        @Override
        public void created(JsonObject responseData) {
            message.reply(createReplyObject(201, "Job started", container));
        }
        
        @Override
        public void exclusive(JsonObject responseData) {
            // Job already running - inform user
            message.reply(createReplyObject(40926, 
                "Job is already running. Please wait.", container));
        }
    });
```

### Pattern 4: Custom Queue and Version

```java
// Override queue name and module version
AsyncJob.Param param = new AsyncJob.Param("module-id", params, AsyncJob.RunMode.Run)
    .setQueueName("priority-queue")
    .setModuleVersion("2.0.0");

new AsyncJob(container, vertx).exec(message, param, callback);
```

---

## HTTP Status Codes

| Code | Meaning | Callback Method | Description |
|------|---------|----------------|-------------|
| 201 | Created | `created()` | Job submitted successfully |
| 40926 | Exclusive Control | `exclusive()` | Job already running (Exclusive mode) |
| 400 | Bad Request | `fail()` | Invalid parameters |
| 500 | Server Error | `fail()` | Internal error |

---

## Checklist

Before writing Async-API code, verify:

- [ ] Used `AsyncJob` helper class (recommended)
- [ ] Used `CallBackAsync` callback
- [ ] Specified correct `RunMode` (Run, Deploy, Exclusive)
- [ ] Built parameters with `Util.makeAsyncParam()` or space-separated
- [ ] Handled all 3 callbacks: `created()`, `exclusive()`, `fail()`
- [ ] Extracted and logged `jobId` from response
- [ ] Wrapped callback logic in try-catch
- [ ] Logged job submission and status
- [ ] Considered using Exclusive mode to prevent duplicates
- [ ] Saved jobId if status checking is needed

---

## Common Mistakes

### ❌ Mistake 1: Using Wrong Callback

```java
// WRONG: Should use CallBackAsync
da.postAsyncAPI("job", body, new CallBack() {
    public void callBack(int code, JsonObject responseData, Throwable th) {
        // Manual status code handling
    }
});
```

### ✅ Fix: Use CallBackAsync

```java
// CORRECT: Use specialized callback
da.postAsyncAPI("job", body, new CallBackAsync(BUS_NAME, container, message) {
    @Override
    public void created(JsonObject responseData) {
        // Automatic 201 handling
    }
    
    @Override
    public void exclusive(JsonObject responseData) {
        // Automatic 40926 handling
    }
});
```

### ❌ Mistake 2: Not Handling Exclusive Control

```java
// WRONG: Missing exclusive() callback
new CallBackAsync(BUS_NAME, container, message) {
    @Override
    public void created(JsonObject responseData) {
        message.reply(responseData);
    }
    // Missing exclusive() - will use default behavior
}
```

### ✅ Fix: Handle All Callbacks

```java
// CORRECT: Handle all callbacks
new CallBackAsync(BUS_NAME, container, message) {
    @Override
    public void created(JsonObject responseData) {
        message.reply(responseData);
    }
    
    @Override
    public void exclusive(JsonObject responseData) {
        message.reply(createReplyObject(40926, "Job already running", container));
    }
    
    @Override
    public void fail(int code, JsonObject responseData) {
        message.reply(responseData);
    }
}
```

### ❌ Mistake 3: Wrong Parameter Format

```java
// WRONG: Using comma-separated
String params = "param1,param2,param3";
```

### ✅ Fix: Use Space-Separated

```java
// CORRECT: Space-separated parameters
String params = Util.makeAsyncParam("param1", "param2", "param3");
// Or manually:
String params = "param1 param2 param3";
```

---

## Async-API vs Data-API Summary

| Feature | Async-API | Data-API |
|---------|-----------|----------|
| **Purpose** | Long-running jobs | CRUD operations |
| **Method** | `postAsyncAPI()`, `getAsyncAPI()` | `getDataAPI()`, `putDataAPI()`, `deleteDataAPI()` |
| **Execution** | Asynchronous (background) | Synchronous (immediate) |
| **Response** | Job ID | Data |
| **Timeout** | No timeout | 5 seconds default |
| **Callback** | `CallBackAsync` | `CallBack`, `CallBackGet`, etc. |
| **Use Case** | Batch, reports, heavy tasks | Quick CRUD operations |

---

**Related**: 
- Quick start: `00-quick-start.md`
- Data-API: `../data-api/01-get-templates.md`
