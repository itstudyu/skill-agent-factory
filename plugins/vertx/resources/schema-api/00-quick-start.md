# Schema-API Quick Start Guide

**FOR AI**: Read this first for Schema-API usage.

## What is Schema-API?

Schema-API is used for **database schema information retrieval** including:
- Table schema definitions
- Column metadata
- Data types and constraints
- Table relationships

**Key Use Case**: Get table structure information for dynamic form generation or validation.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains getSchemaAPI()
└── CallBack.java                # Callback for Schema-API responses
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Always use generic CallBack (no specialized callback)**
2. ⚠️ **Query format: `{tableName}` or `{tableName}?params`**
3. ⚠️ **Response contains table structure metadata**
4. ⚠️ **Handle both 200 (found) and 204 (not found)**
5. ⚠️ **Use for metadata only, not for data retrieval**

---

## Basic Pattern

```java
final DataAccess da = new DataAccess(container, vertx);

// Get table schema
String param = "TABLE_NAME";

da.getSchemaAPI(param, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (th != null) {
                container.logger().error("Schema API error", th);
                message.reply(JsonUtil.createReplyObjectFail(th));
                return;
            }
            
            if (code == 200) {
                JsonObject schema = responseData.getObject("body")
                    .getObject("data");
                
                // Extract schema information
                JsonArray columns = schema.getArray("columns");
                String tableName = schema.getString("tableName");
                
                container.logger().info("Schema for " + tableName + ": " + columns.size() + " columns");
                
                message.reply(schema);
            } else if (code == 204) {
                container.logger().warn("Schema not found for table: " + param);
                message.reply(new JsonObject()
                    .putNumber("code", 404)
                    .putString("message", "Schema not found"));
            } else {
                message.reply(responseData);
            }
            
        } catch (Exception e) {
            container.logger().error("Error processing schema", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## When to Use Schema-API

✅ **Use Schema-API when:**
- Need table structure information
- Generating dynamic forms
- Validating data types
- Building query builders
- Understanding table relationships

❌ **Don't use Schema-API for:**
- Fetching actual data → Use Data-API
- Filtering data → Use Filter-API
- CRUD operations → Use Data-API

---

## Response Format

### Schema Response

```json
{
  "code": 200,
  "body": {
    "data": {
      "tableName": "USER",
      "columns": [
        {
          "name": "id",
          "type": "VARCHAR",
          "length": 50,
          "nullable": false,
          "primaryKey": true
        },
        {
          "name": "name",
          "type": "VARCHAR",
          "length": 100,
          "nullable": false
        },
        {
          "name": "email",
          "type": "VARCHAR",
          "length": 255,
          "nullable": true
        }
      ]
    }
  }
}
```

---

## Checklist

Before writing Schema-API code, verify:

- [ ] Used `getSchemaAPI()` method
- [ ] Used generic `CallBack` (not specialized)
- [ ] Checked `if (th != null)` FIRST
- [ ] Handled HTTP 200 (schema found)
- [ ] Handled HTTP 204 (schema not found)
- [ ] Wrapped callback logic in try-catch
- [ ] Logged table name being queried
- [ ] Used schema for metadata only (not data retrieval)

---

**Related**: 
- Quick start: `00-quick-start.md`
- Complete template: `01-schema-api-template.md`
