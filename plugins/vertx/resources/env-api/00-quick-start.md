# Env-API Quick Start Guide

**FOR AI**: Read this first for Env-API usage.

## What is Env-API?

Env-API is used for **environment configuration retrieval** including:
- Module configuration (queue name, version)
- Application settings
- Environment-specific parameters
- System configuration

**Key Use Case**: Get module configuration before submitting async jobs.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains getEnvAPI()
├── CallBackEnv.java             # Callback for Env-API responses
└── ApiUtil.java                 # Helper: getEnvParams()
```

**Real Example:**
```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/AsyncJob.java
- Line 87: getEnvAPI() usage for async job configuration
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Always use CallBackEnv callback (not generic CallBack)**
2. ⚠️ **Query format: `module?name={moduleId}`**
3. ⚠️ **Use ApiUtil.getEnvParams() to extract configuration**
4. ⚠️ **Response structure is nested: body.data[0].{moduleName}.z**
5. ⚠️ **Commonly used before async job submission**

---

## Basic Pattern

```java
final DataAccess da = new DataAccess(container, vertx);

// Get module configuration
String param = "module?name=" + moduleId;

da.getEnvAPI(param, new CallBackEnv(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            // Extract configuration using helper
            JsonObject config = ApiUtil.getEnvParams(responseData, moduleId);
            
            String queueName = config.getString("queue");
            String version = config.getString("version");
            
            container.logger().info("Module config - Queue: " + queueName + ", Version: " + version);
            
            message.reply(config);
        } catch (Exception e) {
            container.logger().error("Error", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
    
    @Override
    public void fail(int code, JsonObject responseData) {
        container.logger().error("Failed to get env: " + code);
        message.reply(responseData);
    }
});
```

---

## When to Use Env-API

✅ **Use Env-API when:**
- Getting module configuration for async jobs
- Retrieving queue names and versions
- Fetching environment-specific settings
- Getting system configuration

❌ **Don't use Env-API for:**
- User data → Use Data-API
- Master data → Use Data-API getSLkey()
- Employee data → Use Employee-API

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
            "moduleid": "module-id"
          }
        }
      }
    ]
  }
}
```

### Extracted Config (Using ApiUtil.getEnvParams)

```json
{
  "queue": "queue-name",
  "version": "1.0.0",
  "moduleid": "module-id"
}
```

---

## Related Guide

- **Complete Template**: `01-env-api-template.md`

---

**Start here, then read the complete template for detailed examples.**
