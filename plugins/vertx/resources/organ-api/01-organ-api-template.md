# Organ-API Template

## Template 1: Get Organization (LGAN)

**Use this to retrieve organization information.**

```java
public void getOrganization(String platformId, String payerId, String organCode, 
        String date, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate required parameters
        if (StringUtil.isNullOrEmpty(platformId) || StringUtil.isNullOrEmpty(payerId) 
                || StringUtil.isNullOrEmpty(organCode)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Required parameters missing"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build query string
        String queryString = "organization"
            + Util.SetParam("_platformId", platformId,
                "_payerId", payerId,
                "_organCode", organCode,
                "_date", date,
                "_wip", "true");
        
        container.logger().debug("Getting organization: " + organCode);
        
        // Call Organ-API
        da.getOrganAPI(queryString, new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                    
                    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
                    JsonArray dataArray = bodyObj.getArray("data");
                    
                    if (dataArray != null && dataArray.size() > 0) {
                        JsonObject lganData = dataArray.get(0);
                        
                        // Extract organization data
                        String organCodeResult = lganData.getString("LGANC02");
                        String organName = lganData.getString("LGANP01");
                        String parentOrganCode = lganData.getString("LGANC05");
                        String hierarchyLevel = lganData.getString("LGANC03");
                        
                        container.logger().info("Organization found: " + organName 
                            + " (Level: " + hierarchyLevel + ")");
                        
                        // Build response
                        JsonObject response = new JsonObject();
                        response.putNumber("code", 200);
                        
                        JsonObject body = new JsonObject();
                        body.putObject("data", lganData);
                        response.putObject(JsonKeyConstants.BODY, body);
                        
                        message.reply(response);
                    } else {
                        container.logger().warn(methodName + " - No data found");
                        message.reply(new JsonObject().putNumber("code", 204));
                    }
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void noContent(JsonObject responseData) {
                container.logger().warn(methodName + " - Organization not found (204)");
                message.reply(new JsonObject()
                    .putNumber("code", 404)
                    .putString("message", "Organization not found"));
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

## Template 2: Get Manager (LMAG)

**Use this to retrieve manager information.**

```java
public void getManager(String platformId, String payerId, String managerCode, 
        String date, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate required parameters
        if (StringUtil.isNullOrEmpty(platformId) || StringUtil.isNullOrEmpty(payerId) 
                || StringUtil.isNullOrEmpty(managerCode)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Required parameters missing"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build query string
        String queryString = "manager"
            + Util.SetParam("_platformId", platformId,
                "_payerId", payerId,
                "_managerCode", managerCode,
                "_date", date,
                "_wip", "true");
        
        container.logger().debug("Getting manager: " + managerCode);
        
        // Call Organ-API
        da.getOrganAPI(queryString, new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                    
                    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
                    JsonArray dataArray = bodyObj.getArray("data");
                    
                    if (dataArray != null && dataArray.size() > 0) {
                        JsonObject lmagData = dataArray.get(0);
                        
                        // Extract manager data
                        String managerCodeResult = lmagData.getString("LMAGC02");
                        String managerName = lmagData.getString("LMAGP01");
                        
                        container.logger().info("Manager found: " + managerName);
                        
                        // Build response
                        JsonObject response = new JsonObject();
                        response.putNumber("code", 200);
                        
                        JsonObject body = new JsonObject();
                        JsonArray dataArray2 = new JsonArray();
                        dataArray2.add(lmagData);
                        body.putArray("data", dataArray2);
                        
                        response.putObject(JsonKeyConstants.BODY, body);
                        
                        message.reply(response);
                    } else {
                        container.logger().warn(methodName + " - No data found");
                        message.reply(new JsonObject().putNumber("code", 204));
                    }
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void noContent(JsonObject responseData) {
                container.logger().warn(methodName + " - Manager not found (204)");
                message.reply(new JsonObject()
                    .putNumber("code", 404)
                    .putString("message", "Manager not found"));
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

## Template 3: Recursive Parent Organization Lookup

**Use this to get organization hierarchy by recursively fetching parent organizations.**

```java
public void getOrganizationHierarchy(String platformId, String payerId, 
        String organCode, String date, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Hierarchy data storage
        final List<JsonObject> hierarchyData = new ArrayList<JsonObject>();
        
        // Start recursive lookup
        getOrganizationRecursive(message, platformId, payerId, organCode, date, 
            hierarchyData, 0);
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}

private void getOrganizationRecursive(final Message<JsonObject> message, 
        final String platformId, final String payerId, final String organCode, 
        final String date, final List<JsonObject> hierarchyData, final int depth) {
    
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    final int MAX_DEPTH = 9;  // Maximum recursion depth
    
    // Build query string
    String queryString = "organization"
        + Util.SetParam("_platformId", platformId,
            "_payerId", payerId,
            "_organCode", organCode,
            "_date", date,
            "_wip", "true");
    
    container.logger().debug("Getting organization (depth=" + depth + "): " + organCode);
    
    // Call Organ-API
    new DataAccess(container, vertx).getOrganAPI(queryString,
        new CallBackGet(BUS_NAME, container, message) {
            
            @Override
            public void ok(JsonObject responseData) {
                try {
                    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
                    JsonArray dataArray = bodyObj.getArray("data");
                    
                    if (dataArray != null && dataArray.size() > 0) {
                        JsonObject lganData = dataArray.get(0);
                        
                        // Save hierarchy data
                        JsonObject hierarchyItem = new JsonObject();
                        hierarchyItem.putString("organCode", lganData.getString("LGANC02"));
                        hierarchyItem.putString("organName", lganData.getString("LGANP01"));
                        hierarchyItem.putString("hierarchyLevel", lganData.getString("LGANC03"));
                        hierarchyItem.putNumber("depth", depth);
                        hierarchyData.add(hierarchyItem);
                        
                        // Check for parent organization
                        String parentOrganCode = lganData.getString("LGANC05", "");
                        String hierarchyLevel = lganData.getString("LGANC03", "1");
                        
                        // Continue recursion if:
                        // 1. Parent organization code exists
                        // 2. Hierarchy level is not 1 (top level)
                        // 3. Not exceeded max depth
                        if (!StringUtil.isNullOrEmpty(parentOrganCode) 
                                && !"1".equals(hierarchyLevel)
                                && depth < MAX_DEPTH) {
                            
                            container.logger().debug("Found parent organization: " + parentOrganCode);
                            
                            // Recursive call for parent organization
                            getOrganizationRecursive(message, platformId, payerId, 
                                parentOrganCode, date, hierarchyData, depth + 1);
                        } else {
                            // Recursion complete - return hierarchy
                            container.logger().info("Organization hierarchy complete: " 
                                + hierarchyData.size() + " levels");
                            
                            JsonObject response = new JsonObject();
                            response.putNumber("code", 200);
                            
                            JsonObject body = new JsonObject();
                            body.putObject("rootOrganization", lganData);
                            
                            JsonArray hierarchyArray = new JsonArray();
                            for (JsonObject item : hierarchyData) {
                                hierarchyArray.add(item);
                            }
                            body.putArray("hierarchy", hierarchyArray);
                            
                            response.putObject(JsonKeyConstants.BODY, body);
                            message.reply(response);
                        }
                    } else {
                        container.logger().error(methodName + " - No data found");
                        message.reply(new JsonObject().putNumber("code", 204));
                    }
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void noContent(JsonObject responseData) {
                container.logger().error(methodName + " - Organization not found (204)");
                message.reply(JsonUtil.createReplyObjectFail("Organization not found"));
            }
        });
}
```

---

## Real Example 1: Organization with Recursive Lookup

**File**: `src/main/java/jp/co/payroll/p3/storerevampapplication/nyusyahatureview/custom/filter/LGAN.java`

```java
private void getLGAN(final Message<JsonObject> message, final String platformId,
        final String payerId, final String organCode, final String dataOfJoining,
        final List<JsonObject> hierarchyData) {

    // Build query string
    String queryString = buildQueryString(platformId, payerId, organCode, dataOfJoining);

    // Call organ-api
    new DataAccess(container, vertx).getOrganAPI(queryString,
        new CallBackGet(BUS_NAME, container, message) {

            @Override
            public void ok(JsonObject responseData) {
                processLGANResponse(message, responseData, platformId, payerId, dataOfJoining,
                    organCode, hierarchyData);
            }

            @Override
            public void noContent(JsonObject responseData) {
                container.logger().error(BUS_NAME + " - 組織情報が見つかりません (204)");
                message.reply(JsonUtil.createReplyObjectFail(responseData.toString()));
            }
        });
}

private String buildQueryString(String platformId, String payerId, String organCode,
        String dataOfJoining) {
    return "organization"
        + Util.SetParam("_platformId", platformId,
            "_payerId", payerId,
            "_organCode", organCode,
            "_date", dataOfJoining,
            "_wip", "true");
}

private void processLGANResponse(final Message<JsonObject> message, JsonObject responseData,
        final String platformId, final String payerId, final String dataOfJoining,
        final String organCode, final List<JsonObject> hierarchyData) {

    try {
        JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
        JsonArray dataArray = bodyObj.getArray("data");

        if (dataArray != null && dataArray.size() > 0) {
            JsonObject lganData = dataArray.get(0);

            // Save hierarchy data
            boolean isFirst = hierarchyData.isEmpty();
            saveHierarchyData(lganData, hierarchyData, isFirst);

            // Check for parent organization (LGANC05)
            String parentOrganCode = lganData.getString("LGANC05", "");
            if (hasValidParentOrganCode(parentOrganCode) 
                    && hierarchyData.size() < MAX_RECURSION_DEPTH) {
                // Recursive call
                getLGAN(message, platformId, payerId, parentOrganCode, dataOfJoining,
                    hierarchyData);
            } else {
                // Recursion complete
                replyWithData(message, lganData, hierarchyData);
            }
        }
    } catch (Exception e) {
        container.logger().error("Error", e);
        message.reply(new JsonObject().putNumber("code", 500));
    }
}
```

---

## Real Example 2: Manager Retrieval

**File**: `src/main/java/jp/co/payroll/p3/storerevampapplication/nyusyahatureview/custom/filter/LMAG.java`

```java
private void getLMAG(final Message<JsonObject> message, final String platformId,
        final String payerId, final String managerCode, final String dataOfJoining) {

    final String methodName = new Throwable().getStackTrace()[0].getMethodName();

    // Build query string
    String queryString = "manager"
        + Util.SetParam("_platformId", platformId,
            "_payerId", payerId,
            "_managerCode", managerCode,
            "_date", dataOfJoining,
            "_wip", "true");

    // Call organ-api
    new DataAccess(container, vertx).getOrganAPI(queryString,
        new CallBackGet(BUS_NAME, container, message) {

            @Override
            public void ok(JsonObject responseData) {
                try {
                    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
                    JsonArray dataArray = bodyObj.getArray("data");

                    if (dataArray != null && dataArray.size() > 0) {
                        JsonObject lmagData = dataArray.get(0);

                        // Build response
                        JsonObject response = new JsonObject();
                        response.putNumber("code", 200);

                        JsonObject body = new JsonObject();
                        JsonArray dataArray2 = new JsonArray();
                        dataArray2.add(lmagData);
                        body.putArray("data", dataArray2);

                        response.putObject(JsonKeyConstants.BODY, body);

                        message.reply(response);
                    } else {
                        message.reply(new JsonObject().putNumber("code", 204));
                    }
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }

            @Override
            public void noContent(JsonObject responseData) {
                message.reply(new JsonObject().putNumber("code", 204));
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

## Common Patterns

### Pattern 1: Build Query with Util.SetParam

```java
// Use Util.SetParam for clean query building
String queryString = "organization"
    + Util.SetParam("_platformId", platformId,
        "_payerId", payerId,
        "_organCode", organCode,
        "_date", date,
        "_wip", "true");

// Results in: organization?_platformId=xxx&_payerId=yyy&_organCode=zzz&_date=2024-01-01&_wip=true
```

### Pattern 2: Check Hierarchy Level

```java
// Check if organization is top level
String hierarchyLevel = lganData.getString("LGANC03", "1");

if ("1".equals(hierarchyLevel)) {
    // Top level organization - no parent
    container.logger().info("Top level organization");
} else {
    // Has parent organization
    String parentOrganCode = lganData.getString("LGANC05");
    // Fetch parent...
}
```

### Pattern 3: Validate Parent Organization Code

```java
// Check if parent organization code is valid
private boolean hasValidParentOrganCode(String parentOrganCode) {
    return !StringUtil.isNullOrEmpty(parentOrganCode) 
        && !parentOrganCode.trim().isEmpty();
}
```

### Pattern 4: Limit Recursion Depth

```java
// Prevent infinite recursion
private static final int MAX_RECURSION_DEPTH = 9;

if (depth < MAX_RECURSION_DEPTH && hasParent) {
    // Continue recursion
    getOrganizationRecursive(..., depth + 1);
} else {
    // Stop recursion
    container.logger().warn("Max recursion depth reached or no parent");
    replyWithData(message, data);
}
```

---

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Organization/Manager data retrieved |
| 204 | No Content | Organization/Manager not found |
| 400 | Bad Request | Invalid parameters |
| 500 | Server Error | Internal error |

---

## LGAN Fields

| Field | Description |
|-------|-------------|
| `LGANC02` | Organization code |
| `LGANP01` | Organization name |
| `LGANC03` | Hierarchy level (1=top) |
| `LGANC05` | Parent organization code |

---

## LMAG Fields

| Field | Description |
|-------|-------------|
| `LMAGC02` | Manager code |
| `LMAGP01` | Manager name |

---

## Checklist

Before writing Organ-API code, verify:

- [ ] Used `getOrganAPI()` method (GET only)
- [ ] Used `CallBackGet` callback
- [ ] Query format: `organization?params` or `manager?params`
- [ ] Included all required parameters: _platformId, _payerId, _organCode/_managerCode, _date, _wip
- [ ] Set `_wip` to "true"
- [ ] Handled both `ok()` (200) and `noContent()` (204)
- [ ] For LGAN: Implemented recursive parent lookup if needed
- [ ] Limited recursion depth (max 9 levels)
- [ ] Wrapped callback logic in try-catch
- [ ] Logged organization/manager operations

---

## Common Mistakes

### ❌ Mistake 1: Missing _wip Parameter

```java
// WRONG: Missing _wip parameter
String queryString = "organization"
    + Util.SetParam("_platformId", platformId,
        "_payerId", payerId,
        "_organCode", organCode,
        "_date", date);
```

### ✅ Fix: Include _wip=true

```java
// CORRECT: Include _wip parameter
String queryString = "organization"
    + Util.SetParam("_platformId", platformId,
        "_payerId", payerId,
        "_organCode", organCode,
        "_date", date,
        "_wip", "true");
```

### ❌ Mistake 2: No Recursion Limit

```java
// WRONG: Infinite recursion possible
if (!StringUtil.isNullOrEmpty(parentOrganCode)) {
    getOrganizationRecursive(...);  // No depth check!
}
```

### ✅ Fix: Limit Recursion Depth

```java
// CORRECT: Check depth
private static final int MAX_DEPTH = 9;

if (!StringUtil.isNullOrEmpty(parentOrganCode) && depth < MAX_DEPTH) {
    getOrganizationRecursive(..., depth + 1);
}
```

### ❌ Mistake 3: Wrong Endpoint

```java
// WRONG: Using data-api instead of organ-api
da.getDataAPI(queryString, callback);
```

### ✅ Fix: Use getOrganAPI

```java
// CORRECT: Use organ-api
da.getOrganAPI(queryString, callback);
```

---

## Organ-API Summary

| Operation | Method | Endpoint | Response |
|-----------|--------|----------|----------|
| Get organization | `getOrganAPI()` | `organization?params` | LGAN data |
| Get manager | `getOrganAPI()` | `manager?params` | LMAG data |

**Key Points:**
- GET only
- Always include _wip=true
- LGAN supports recursive parent lookup
- Limit recursion to 9 levels
- Check LGANC03 for hierarchy level

---

**Related**: 
- Quick start: `00-quick-start.md`
- Data-API: For general table queries
