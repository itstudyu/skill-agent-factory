# Employee-API Quick Start Guide

**FOR AI**: Read this first for Employee-API usage.

## What is Employee-API?

Employee-API is used for **employee-related operations** including:
- Employee number generation (empno/issue)
- Employee number validation (duplicate check)
- Employee data retrieval
- Employee data updates

**Key Use Case**: Employee number (社員番号) management and validation.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains getEmployeeAPI(), putEmployeeAPI()
└── CallBackGet.java             # Callback for Employee-API responses
```

**Real Examples:**
```
src/main/java/jp/co/payroll/p3/storerevampapplication/nyusyahatureview/custom/filter/
└── EMPNO.java                   # Employee number generation example

src/main/java/jp/co/payroll/p3/submodules/CommonScreen/validation/
└── EmpNoValidation.java         # Employee number validation example
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Always use CallBackGet for GET operations**
2. ⚠️ **Always use CallBackPut for PUT operations**
3. ⚠️ **Query format: `{platformId}/endpoint?params`**
4. ⚠️ **Handle both ok (200) and noContent (204) for validation**
5. ⚠️ **Employee number validation: 200=exists, 204=not exists**

---

## Basic Pattern: Get Employee Number (Issue)

```java
final DataAccess da = new DataAccess(container, vertx);

// Generate new employee number
String query = platformId + "/empno/issue";

da.getEmployeeAPI(query, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            String empNo = responseData.getObject("body")
                .getObject("data")
                .getString("empNo");
            
            container.logger().info("Generated empNo: " + empNo);
            message.reply(new JsonObject()
                .putNumber("code", 200)
                .putString("empNo", empNo));
        } catch (Exception e) {
            container.logger().error(methodName + LogConstants.ERROR, e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## Basic Pattern: Validate Employee Number

```java
final DataAccess da = new DataAccess(container, vertx);

// Check if employee number exists
String query = platformId + "/paynumber?_employeeNumber=" + empNo;

da.getEmployeeAPI(query, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        // HTTP 200: Employee number EXISTS (duplicate)
        message.reply(new JsonObject()
            .putNumber("code", 200)
            .putBoolean("exists", true)
            .putString("message", "Employee number already exists"));
    }
    
    @Override
    public void noContent(JsonObject responseData) {
        // HTTP 204: Employee number NOT EXISTS (available)
        message.reply(new JsonObject()
            .putNumber("code", 204)
            .putBoolean("exists", false)
            .putString("message", "Employee number available"));
    }
});
```

---

## Quick Method Reference

| Method | Purpose | Endpoint Example |
|--------|---------|------------------|
| `getEmployeeAPI()` | Get employee data or validate | `{platform}/empno/issue` |
| `getEmployeeAPI()` | Check employee number | `{platform}/paynumber?_employeeNumber={empNo}` |
| `putEmployeeAPI()` | Update employee data | `{platform}/employee/{id}` |

---

## When to Use Employee-API

✅ **Use Employee-API when:**
- Generating new employee numbers
- Validating employee number uniqueness
- Checking employee number format
- Retrieving employee-specific data
- Updating employee information

❌ **Don't use Employee-API for:**
- General data queries → Use Data-API
- Master data lookup → Use Data-API getSLkey()
- File operations → Use File-API

---

## Related Guide

- **Complete Template**: `01-employee-api-template.md`

---

**Start here, then read the complete template for detailed examples.**
