# Filter-API Quick Start Guide

**FOR AI**: Read this first for Filter-API usage.

## What is Filter-API?

Filter-API is a specialized API for fetching filtered data using predefined filter queries. It's commonly used for:
- List screens with complex filtering
- Search results with multiple criteria
- Predefined data queries

**Key Difference from Data-API**: Filter-API uses **query strings** instead of table/ID paths.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains getFilterAPI() methods
└── CallBackGet.java             # Callback for Filter-API responses
```

**Real Examples:**
```
src/main/java/jp/co/payroll/p3/storerevampapplication/
├── applicantlist/custom/filter/XTLGTask.java           # Filter usage example
└── recruitmentstatuslist/custom/filter/XTLH.java       # Filter with params
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Filter-API only supports GET requests**
2. ⚠️ **Always use CallBackGet (not generic CallBack)**
3. ⚠️ **Query string format: `{nonPlatformID}/{filterName}?params`**
4. ⚠️ **Response is JsonArray, not JsonObject with data field**
5. ⚠️ **ALWAYS handle both 200 (ok) and 204 (noContent)**

---

## Basic Pattern

```java
final DataAccess da = new DataAccess(container, vertx);

// Build query string
String query = nonPlatformID + "/FILTER_NAME" + "?param1=value1&param2=value2";

da.getFilterAPI(query, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            // Response is JsonArray directly in body
            message.reply(responseData.getArray(JsonKeyConstants.BODY).toString());
        } catch (Exception e) {
            container.logger().error(methodName + LogConstants.ERROR, e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
    
    @Override
    public void noContent(JsonObject responseData) {
        try {
            message.reply(responseData);
        } catch (Exception e) {
            container.logger().error(methodName + LogConstants.ERROR, e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## Quick Comparison: Filter-API vs Data-API

| Aspect | Filter-API | Data-API |
|--------|-----------|----------|
| **Methods** | GET only | GET, PUT, DELETE |
| **Path Format** | `{platform}/FILTER_NAME?params` | `TABLE/{platform}/{id}` |
| **Response** | JsonArray in body | JsonArray in body.data |
| **Use Case** | Complex filtered queries | CRUD operations |
| **Callback** | CallBackGet only | CallBack, CallBackGet, CallBackPut, CallBackDelete |

---

## When to Use Filter-API

✅ **Use Filter-API when:**
- Fetching list data with complex filters
- Using predefined filter queries
- Need to combine multiple table data
- Search functionality with multiple criteria

❌ **Don't use Filter-API for:**
- Single record fetch by ID → Use Data-API GET
- Create/Update/Delete operations → Use Data-API PUT/DELETE
- Simple table queries → Use Data-API GET

---

## Related Guide

- **Complete Template**: `01-filter-api-template.md`

---

**Start here, then read the complete template for detailed examples.**
