# Employee-API Template

## Template 1: Generate Employee Number

**Use this to generate a new employee number.**

```java
public void issueEmployeeNumber(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        JsonObject body = message.body();
        final String platformId = JsonUtil.getString(body, "platformId");
        
        // Build query
        String query = platformId + "/empno/issue";
        
        // Optional: Add parameters for specific numbering rules
        String empNoMethod = JsonUtil.getString(body, "empNoMethod");
        if ("3".equals(empNoMethod)) {
            String payerId = JsonUtil.getString(body, "payerId");
            String laborId = JsonUtil.getString(body, "laborId");
            query += "?payerId=" + payerId + "&laborId=" + laborId;
        }
        
        // Optional: Add group parameter
        String group = JsonUtil.getString(body, "group");
        if (!StringUtil.isNullOrEmpty(group)) {
            query += (query.contains("?") ? "&" : "?") + "group=" + group;
        }
        
        container.logger().debug("Employee API query: " + query);
        
        // Call Employee-API
        new DataAccess(container, vertx).getEmployeeAPI(query,
            new CallBackGet(BUS_NAME, container, message) {
                
                @Override
                public void ok(JsonObject responseData) {
                    try {
                        // Extract employee number
                        String empNo = responseData.getObject("body")
                            .getObject("data")
                            .getString("empNo");
                        
                        if (StringUtil.isNullOrEmpty(empNo)) {
                            container.logger().error("empNo not found in response");
                            message.reply(new JsonObject().putNumber("code", 500));
                            return;
                        }
                        
                        container.logger().info("Generated empNo: " + empNo);
                        
                        // Return employee number
                        JsonObject result = new JsonObject();
                        result.putNumber("code", 200);
                        result.putString("empNo", empNo);
                        message.reply(result);
                        
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }
                
                @Override
                public void fail(int code, JsonObject responseData) {
                    container.logger().error(methodName + " - Failed: " + code);
                    super.fail(code, responseData);
                }
            });
            
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Template 2: Validate Employee Number (Check Duplicate)

**Use this to check if employee number already exists.**

```java
public void validateEmployeeNumber(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        JsonObject body = message.body();
        final String platformId = JsonUtil.getString(body, "platformId");
        final String empNo = JsonUtil.getString(body, "empNo");
        
        // Validate required parameters
        if (StringUtil.isNullOrEmpty(empNo)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Employee number is required"));
            return;
        }
        
        // Build query
        String query = platformId + "/paynumber?_employeeNumber=" + empNo;
        
        // Optional: Add date parameter
        String mDate = JsonUtil.getString(body, "mDate");
        if (!StringUtil.isNullOrEmpty(mDate)) {
            query += "&_date=" + mDate;
        }
        
        container.logger().debug("Validation query: " + query);
        
        // Call Employee-API
        new DataAccess(container, vertx).getEmployeeAPI(query,
            new CallBackGet(BUS_NAME, container, message) {
                
                @Override
                public void ok(JsonObject responseData) {
                    try {
                        // HTTP 200: Employee number EXISTS (duplicate)
                        container.logger().warn("Employee number already exists: " + empNo);
                        
                        JsonObject result = new JsonObject();
                        result.putNumber("code", 200);
                        result.putBoolean("exists", true);
                        result.putBoolean("valid", false);
                        result.putString("message", "Employee number already exists");
                        message.reply(result);
                        
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }
                
                @Override
                public void noContent(JsonObject responseData) {
                    try {
                        // HTTP 204: Employee number NOT EXISTS (available)
                        container.logger().info("Employee number available: " + empNo);
                        
                        JsonObject result = new JsonObject();
                        result.putNumber("code", 204);
                        result.putBoolean("exists", false);
                        result.putBoolean("valid", true);
                        result.putString("message", "Employee number available");
                        message.reply(result);
                        
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        message.reply(new JsonObject().putNumber("code", 500));
                    }
                }
                
                @Override
                public void fail(int code, JsonObject responseData) {
                    container.logger().error(methodName + " - Validation failed: " + code);
                    super.fail(code, responseData);
                }
            });
            
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Template 3: Update Employee Data

**Use this to update employee information.**

```java
public void updateEmployee(String employeeId, JsonObject updateData, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        String param = platformId + "/employee/" + employeeId;
        
        // Build request body
        JsonObject body = new JsonObject();
        body.putString("empNo", updateData.getString("empNo"));
        body.putString("name", updateData.getString("name"));
        body.putString("department", updateData.getString("department"));
        
        container.logger().debug("Update employee: " + param);
        
        da.putEmployeeAPI(param, body, new CallBackPut(BUS_NAME, container, message) {
            @Override
            public void created(JsonObject responseData) {
                try {
                    container.logger().info("Employee updated successfully");
                    super.created(responseData);
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void resourceAlreadyChanged(JsonObject responseData) {
                try {
                    container.logger().warn("Employee data was modified by another user");
                    super.resourceAlreadyChanged(responseData);
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void fail(int code, JsonObject responseData) {
                container.logger().error(methodName + " - Update failed: " + code);
                super.fail(code, responseData);
            }
        });
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Real Example 1: Employee Number Generation

**File**: `src/main/java/jp/co/payroll/p3/storerevampapplication/nyusyahatureview/custom/filter/EMPNO.java`

```java
private void issueEmpNo(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();

    JsonObject body = message.body();
    final String platformId = JsonUtil.getString(body, "platformId");
    final String empNoMethod = JsonUtil.getString(body, "empNoMethod");
    final String payerId = JsonUtil.getString(body, "payerId");
    final String laborId = JsonUtil.getString(body, "laborId");
    final String group = JsonUtil.getString(body, "group");

    // Build query parameters
    List<String> params = new ArrayList<String>();

    if ("3".equals(empNoMethod)) {
        params.add("payerId");
        params.add(payerId);
        params.add("laborId");
        params.add(laborId);
    }

    if (group != null && !group.isEmpty()) {
        params.add("group");
        params.add(group);
    }

    final String query = platformId + "/empno/issue"
        + (params.isEmpty() ? "" : Util.SetParam(params.toArray(new String[0])));

    new DataAccess(container, vertx).getEmployeeAPI(query,
        new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    String empNo = responseData.getObject("body")
                        .getObject("data")
                        .getString("empNo");
                    
                    if (empNo == null || empNo.isEmpty()) {
                        container.logger().error("empNo not found in response");
                        message.reply(new JsonObject().putNumber("code", 500));
                        return;
                    }

                    JsonObject result = new JsonObject()
                        .putNumber("code", 200)
                        .putString("empNo", empNo);
                    message.reply(result);
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }

            @Override
            public void fail(int code, JsonObject responseData) {
                container.logger().error(methodName + " - Failed: " + code);
                super.fail(code, responseData);
            }
        });
}
```

---

## Real Example 2: Employee Number Validation

**File**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/validation/EmpNoValidation.java`

```java
private void checkEmpNumber(final Message<JsonObject> message, final Param prm,
        final CallBackEmpNoValidation callback) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);

    String queryString = prm.platformId + "/paynumber?_employeeNumber="
        + prm.newEmpNumber + (StringUtil.isNullOrEmpty(prm.mDate) ? "" : "&_date=" + prm.mDate);

    new DataAccess(container, vertx).getEmployeeAPI(queryString,
        new CallBackGet(BUS_NAME(), container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    // Employee number exists (duplicate)
                    callback.EmpNoExist();
                } catch (Throwable e) {
                    container.logger().error(e.getMessage());
                    message.reply(JsonUtil.createReplyObjectFail(e));
                }
            }

            @Override
            public void noContent(JsonObject responseData) {
                try {
                    // Employee number not exists (available)
                    callback.EmpNoNotExist();
                } catch (Throwable e) {
                    container.logger().error(e.getMessage());
                    message.reply(JsonUtil.createReplyObjectFail(e));
                }
            }

            @Override
            public void fail(int code, JsonObject responseData) {
                try {
                    container.logger().error(methodName + LogConstants.RETURN + responseData.toString());
                    callback.fail();
                } catch (Throwable e) {
                    container.logger().error(e.getMessage());
                    message.reply(JsonUtil.createReplyObjectFail(e));
                }
            }
        });
}
```

---

## Common Patterns

### Pattern 1: Employee Number with Group

```java
// Generate employee number for specific group
String query = platformId + "/empno/issue?group=" + groupCode;

da.getEmployeeAPI(query, callback);
```

### Pattern 2: Employee Number with Payer/Labor

```java
// Generate employee number for specific payer and labor
String query = platformId + "/empno/issue"
    + "?payerId=" + payerId
    + "&laborId=" + laborId;

da.getEmployeeAPI(query, callback);
```

### Pattern 3: Validate with Date

```java
// Check employee number existence at specific date
String query = platformId + "/paynumber"
    + "?_employeeNumber=" + empNo
    + "&_date=" + date; // Format: YYYY-MM-DD

da.getEmployeeAPI(query, callback);
```

### Pattern 4: Batch Validation

```java
// Validate multiple employee numbers
public void validateBatch(List<String> empNos, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    final JsonArray results = new JsonArray();
    final AtomicInteger counter = new AtomicInteger(empNos.size());
    
    for (String empNo : empNos) {
        String query = platformId + "/paynumber?_employeeNumber=" + empNo;
        
        da.getEmployeeAPI(query, new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                // Exists
                synchronized (results) {
                    results.add(new JsonObject()
                        .putString("empNo", empNo)
                        .putBoolean("exists", true));
                }
                
                if (counter.decrementAndGet() == 0) {
                    message.reply(new JsonObject()
                        .putNumber("code", 200)
                        .putArray("results", results));
                }
            }
            
            @Override
            public void noContent(JsonObject responseData) {
                // Not exists
                synchronized (results) {
                    results.add(new JsonObject()
                        .putString("empNo", empNo)
                        .putBoolean("exists", false));
                }
                
                if (counter.decrementAndGet() == 0) {
                    message.reply(new JsonObject()
                        .putNumber("code", 200)
                        .putArray("results", results));
                }
            }
        });
    }
}
```

---

## HTTP Status Codes

| Code | Meaning | Context | Action |
|------|---------|---------|--------|
| 200 | OK | Employee number exists | Duplicate - cannot use |
| 200 | OK | Employee data retrieved | Process data |
| 201 | Created | Employee updated | Success |
| 204 | No Content | Employee number not exists | Available - can use |
| 400 | Bad Request | Invalid parameters | Show validation error |
| 404 | Not Found | Employee not found | Show not found |
| 500 | Server Error | Internal error | Show error |

---

## Response Formats

### Employee Number Generation Response

```json
{
  "code": 200,
  "body": {
    "data": {
      "empNo": "EMP001234"
    }
  }
}
```

### Validation Response (Exists)

```json
{
  "code": 200,
  "body": {
    "data": {
      "empNo": "EMP001234",
      "exists": true
    }
  }
}
```

### Validation Response (Not Exists)

```json
{
  "code": 204
}
```

---

## Checklist

Before writing Employee-API code, verify:

- [ ] Used `getEmployeeAPI()` for GET operations
- [ ] Used `putEmployeeAPI()` for PUT operations
- [ ] Used `CallBackGet` for GET callbacks
- [ ] Used `CallBackPut` for PUT callbacks
- [ ] Query format: `{platformId}/endpoint?params`
- [ ] Handled both `ok()` (200) and `noContent()` (204)
- [ ] Understood 200=exists, 204=not exists for validation
- [ ] Extracted `empNo` from `body.data.empNo`
- [ ] Validated required parameters before call
- [ ] Wrapped callback logic in try-catch
- [ ] Logged employee operations

---

## Common Mistakes

### ❌ Mistake 1: Wrong Validation Logic

```java
// WRONG: Treating 200 as "available"
@Override
public void ok(JsonObject responseData) {
    // This means employee number EXISTS (duplicate)
    message.reply("Employee number is available"); // WRONG!
}
```

### ✅ Fix: Correct Logic

```java
// CORRECT: 200 = exists, 204 = not exists
@Override
public void ok(JsonObject responseData) {
    // Employee number EXISTS (duplicate)
    message.reply("Employee number already exists");
}

@Override
public void noContent(JsonObject responseData) {
    // Employee number NOT EXISTS (available)
    message.reply("Employee number is available");
}
```

### ❌ Mistake 2: Wrong Response Path

```java
// WRONG: Employee-API uses body.data, not body.data array
String empNo = responseData.getObject("body")
    .getArray("data")
    .get(0)
    .getString("empNo");
```

### ✅ Fix: Correct Path

```java
// CORRECT: Direct object access
String empNo = responseData.getObject("body")
    .getObject("data")
    .getString("empNo");
```

---

## Employee-API Summary

| Operation | Method | Query Format | Response |
|-----------|--------|--------------|----------|
| Generate empNo | `getEmployeeAPI()` | `{platform}/empno/issue?params` | `body.data.empNo` |
| Validate empNo | `getEmployeeAPI()` | `{platform}/paynumber?_employeeNumber={empNo}` | 200=exists, 204=not exists |
| Update employee | `putEmployeeAPI()` | `{platform}/employee/{id}` | 201=success |

---

**Related**: 
- Quick start: `00-quick-start.md`
- Data-API: `../data-api/02-put-templates.md`
