# Organ-API Quick Start Guide

**FOR AI**: Read this first for Organ-API usage.

## What is Organ-API?

Organ-API is used for **organization and manager information retrieval** including:
- Organization (組織) data retrieval
- Manager (役職) data retrieval
- Hierarchical organization structure
- Recursive parent organization lookup

**Key Use Case**: Get organization and manager information for employee management.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains getOrganAPI()
└── CallBackGet.java             # Callback for Organ-API responses
```

**Real Examples:**
```
src/main/java/jp/co/payroll/p3/storerevampapplication/nyusyahatureview/custom/filter/
├── LGAN.java                    # Organization (LGAN) retrieval with recursive parent lookup
└── LMAG.java                    # Manager (LMAG) retrieval
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Always use GET method (getOrganAPI)**
2. ⚠️ **Always use CallBackGet callback**
3. ⚠️ **Query format: `organization?params` or `manager?params`**
4. ⚠️ **Always include: _platformId, _payerId, _date, _wip=true**
5. ⚠️ **Handle recursive parent organization lookup for LGAN**

---

## Basic Pattern: Get Organization (LGAN)

```java
final DataAccess da = new DataAccess(container, vertx);

// Build query for organization
String queryString = "organization"
    + Util.SetParam("_platformId", platformId,
        "_payerId", payerId,
        "_organCode", organCode,
        "_date", date,
        "_wip", "true");

da.getOrganAPI(queryString, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            JsonObject bodyObj = responseData.getObject("body");
            JsonArray dataArray = bodyObj.getArray("data");
            
            if (dataArray != null && dataArray.size() > 0) {
                JsonObject lganData = dataArray.get(0);
                
                // Extract organization data
                String organCode = lganData.getString("LGANC02");
                String organName = lganData.getString("LGANP01");
                String parentOrganCode = lganData.getString("LGANC05");
                
                container.logger().info("Organization: " + organName);
                
                message.reply(new JsonObject()
                    .putNumber("code", 200)
                    .putObject("data", lganData));
            }
        } catch (Exception e) {
            container.logger().error("Error", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
    
    @Override
    public void noContent(JsonObject responseData) {
        container.logger().warn("Organization not found (204)");
        message.reply(new JsonObject().putNumber("code", 404));
    }
});
```

---

## Basic Pattern: Get Manager (LMAG)

```java
final DataAccess da = new DataAccess(container, vertx);

// Build query for manager
String queryString = "manager"
    + Util.SetParam("_platformId", platformId,
        "_payerId", payerId,
        "_managerCode", managerCode,
        "_date", date,
        "_wip", "true");

da.getOrganAPI(queryString, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            JsonObject bodyObj = responseData.getObject("body");
            JsonArray dataArray = bodyObj.getArray("data");
            
            if (dataArray != null && dataArray.size() > 0) {
                JsonObject lmagData = dataArray.get(0);
                
                // Extract manager data
                String managerCode = lmagData.getString("LMAGC02");
                String managerName = lmagData.getString("LMAGP01");
                
                container.logger().info("Manager: " + managerName);
                
                message.reply(new JsonObject()
                    .putNumber("code", 200)
                    .putObject("data", lmagData));
            }
        } catch (Exception e) {
            container.logger().error("Error", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
    
    @Override
    public void noContent(JsonObject responseData) {
        container.logger().warn("Manager not found (204)");
        message.reply(new JsonObject().putNumber("code", 404));
    }
});
```

---

## When to Use Organ-API

✅ **Use Organ-API when:**
- Retrieving organization (LGAN) information
- Retrieving manager (LMAG) information
- Building organization hierarchy
- Getting parent organization recursively
- Displaying organization structure

❌ **Don't use Organ-API for:**
- Employee data → Use Employee-API or Data-API
- Master data lookup → Use Data-API getSLkey()
- General table queries → Use Data-API

---

## Query Parameters

### Organization Query

| Parameter | Required | Description |
|-----------|----------|-------------|
| `_platformId` | Yes | Platform ID |
| `_payerId` | Yes | Payer ID |
| `_organCode` | Yes | Organization code |
| `_date` | Yes | Date (YYYY-MM-DD) |
| `_wip` | Yes | Set to "true" |

### Manager Query

| Parameter | Required | Description |
|-----------|----------|-------------|
| `_platformId` | Yes | Platform ID |
| `_payerId` | Yes | Payer ID |
| `_managerCode` | Yes | Manager code |
| `_date` | Yes | Date (YYYY-MM-DD) |
| `_wip` | Yes | Set to "true" |

---

## Response Format

### Organization (LGAN) Response

```json
{
  "code": 200,
  "body": {
    "data": [
      {
        "LGANC02": "ORG001",
        "LGANP01": "営業部",
        "LGANC05": "ORG000",
        "LGANC03": "2"
      }
    ]
  }
}
```

### Manager (LMAG) Response

```json
{
  "code": 200,
  "body": {
    "data": [
      {
        "LMAGC02": "MGR001",
        "LMAGP01": "部長"
      }
    ]
  }
}
```

---

## Related Guide

- **Complete Template**: `01-organ-api-template.md`

---

**Start here, then read the complete template for detailed examples including recursive parent lookup.**
