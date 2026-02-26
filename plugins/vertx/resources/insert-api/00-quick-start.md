# Insert-API Quick Start Guide

**FOR AI**: Read this first for Insert-API usage.

## What is Insert-API?

Insert-API is used for **bulk data insertion operations**. Based on the API name and common patterns, it is likely used for:
- Batch data insertion
- Bulk record creation
- Mass data import

**Note**: No actual usage examples found in the codebase. This documentation is based on common API patterns.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Would contain getInsertAPI() or postInsertAPI()
└── CallBack.java                # Callback for Insert-API responses
```

**API Definition:**
```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/APIClientPool.java
- Line 50: INSERT_API constant defined
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Likely uses POST method for bulk insertion**
2. ⚠️ **Always use generic CallBack (no specialized callback)**
3. ⚠️ **Check if (th != null) FIRST in callback**
4. ⚠️ **Success code likely 201 Created or 200 OK**
5. ⚠️ **Validate data before bulk insertion**

---

## Basic Pattern (Hypothetical)

```java
final DataAccess da = new DataAccess(container, vertx);

// Build bulk insert data
JsonArray records = new JsonArray();
for (DataItem item : dataList) {
    JsonObject record = new JsonObject();
    record.putString("field1", item.field1);
    record.putString("field2", item.field2);
    records.add(record);
}

JsonObject requestBody = new JsonObject();
requestBody.putArray("records", records);

// Call Insert-API (method name may vary)
da.postInsertAPI("endpoint", requestBody, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (th != null) {
                container.logger().error("Insert API error", th);
                message.reply(JsonUtil.createReplyObjectFail(th));
                return;
            }
            
            if (code == 201 || code == 200) {
                container.logger().info("Bulk insert successful");
                message.reply(new JsonObject()
                    .putNumber("code", 200)
                    .putNumber("insertedCount", records.size()));
            } else {
                container.logger().error("Insert failed: " + code);
                message.reply(new JsonObject().putNumber("code", code));
            }
            
        } catch (Exception e) {
            container.logger().error("Error", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## When to Use Insert-API

✅ **Use Insert-API when:**
- Bulk inserting multiple records
- Batch data import
- Mass data creation
- Performance-critical insertions

❌ **Don't use Insert-API for:**
- Single record creation → Use Data-API PUT
- Data updates → Use Data-API PUT
- Data deletion → Use Data-API DELETE
- Data queries → Use Data-API GET or Filter-API

---

## Important Notes

⚠️ **WARNING**: No actual usage examples found in the codebase.

Before using Insert-API:
1. Check DataAccess.java for actual method signatures
2. Verify endpoint format and parameters
3. Confirm request body structure
4. Test with small dataset first
5. Check API documentation for specific requirements

---

## Checklist

Before writing Insert-API code, verify:

- [ ] Confirmed actual method name in DataAccess.java
- [ ] Validated all data before insertion
- [ ] Used generic `CallBack`
- [ ] Checked `if (th != null)` FIRST
- [ ] Handled success codes (200/201)
- [ ] Wrapped callback logic in try-catch
- [ ] Logged insertion details
- [ ] Tested with small dataset first

---

**Related**: 
- Complete template: `01-insert-api-template.md`
- Data-API PUT: For single record creation

---

**⚠️ IMPORTANT**: This is a hypothetical guide based on API naming conventions. Please verify actual implementation in your codebase before use.
