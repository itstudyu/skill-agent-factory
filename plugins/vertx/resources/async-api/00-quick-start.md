# Async-API Quick Start Guide

**FOR AI**: Read this first for Async-API usage.

## What is Async-API?

Async-API is used for **long-running asynchronous jobs** that should not block the main thread. It's commonly used for:
- Batch processing
- Report generation
- Data import/export
- Heavy computation tasks
- File processing

**Key Concept**: POST to start a job, GET to check status.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains postAsyncAPI(), getAsyncAPI()
├── AsyncJob.java                # Helper class for job submission
└── CallBackAsync.java           # Callback for Async-API responses
```

**Real Example:**
```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/AsyncJob.java
- Complete async job submission implementation
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Use AsyncJob helper class for job submission (recommended)**
2. ⚠️ **Always use CallBackAsync callback (not generic CallBack)**
3. ⚠️ **POST returns jobId - save it to check status later**
4. ⚠️ **Handle 3 responses: created (201), exclusive (40926), fail**
5. ⚠️ **Use RunMode: Run (0), Deploy (1), or Exclusive (2)**

---

## Basic Pattern (Using AsyncJob Helper)

```java
// Recommended: Use AsyncJob helper class
new AsyncJob(container, vertx).exec(message,
    new AsyncJob.Param("module-id", 
        Util.makeAsyncParam(platformId, param1, param2), 
        AsyncJob.RunMode.Run),
    new CallBackAsync(BUS_NAME, container, message) {
        
        @Override
        public void created(JsonObject responseData) {
            // Job submitted successfully (HTTP 201)
            container.logger().info("Job created: " + responseData.toString());
            message.reply(responseData);
        }
        
        @Override
        public void exclusive(JsonObject responseData) {
            // Exclusive control error (HTTP 40926)
            container.logger().warn("Job already running");
            message.reply(responseData);
        }
        
        @Override
        public void fail(int code, JsonObject responseData) {
            // Other errors
            container.logger().error("Job failed: " + code);
            message.reply(responseData);
        }
    });
```

---

## Basic Pattern (Direct API Call)

```java
// Alternative: Direct API call (not recommended)
final DataAccess da = new DataAccess(container, vertx);

JsonObject body = new JsonObject();
body.putString("queueName", "queue-name");
body.putString("moduleId", "module-id");
body.putString("moduleVersion", "1.0.0");
body.putString("mode", "0"); // 0=Run, 1=Deploy, 2=Exclusive
body.putString("param", "param1 param2 param3");

da.postAsyncAPI("job", body, new CallBackAsync(BUS_NAME, container, message) {
    @Override
    public void created(JsonObject responseData) {
        // Job submitted
    }
    
    @Override
    public void exclusive(JsonObject responseData) {
        // Already running
    }
    
    @Override
    public void fail(int code, JsonObject responseData) {
        // Failed
    }
});
```

---

## Run Modes

| Mode | Value | Description | Use Case |
|------|-------|-------------|----------|
| **Run** | "0" | Execute job immediately | Normal job execution |
| **Deploy** | "1" | Deploy module only (don't run) | Module deployment |
| **Exclusive** | "2" | Exclusive execution (prevent duplicate) | Prevent concurrent runs |

---

## Quick Comparison: Async-API vs Data-API

| Aspect | Async-API | Data-API |
|--------|-----------|----------|
| **Purpose** | Long-running jobs | CRUD operations |
| **Methods** | POST (start), GET (status) | GET, PUT, DELETE |
| **Response** | Job ID | Data |
| **Execution** | Asynchronous | Synchronous |
| **Callback** | CallBackAsync | CallBack, CallBackGet, etc. |
| **Timeout** | No timeout (job runs in background) | 5 seconds default |

---

## When to Use Async-API

✅ **Use Async-API when:**
- Task takes more than 5 seconds
- Batch processing (1000+ records)
- Report generation
- File import/export
- Heavy computation
- User should not wait for completion

❌ **Don't use Async-API for:**
- Simple CRUD operations → Use Data-API
- Quick queries (< 1 second) → Use Data-API
- Real-time updates → Use Data-API

---

## Response Format

### Success Response (HTTP 201)

```json
{
  "code": 201,
  "body": {
    "data": {
      "jobId": "job-12345-abcde"
    }
  }
}
```

**Save the jobId** to check job status later.

### Exclusive Control Response (HTTP 40926)

```json
{
  "code": 40926,
  "message": "Job is already running"
}
```

---

## Related Guide

- **Complete Template**: `01-async-api-template.md`

---

**Start here, then read the complete template for detailed examples.**
