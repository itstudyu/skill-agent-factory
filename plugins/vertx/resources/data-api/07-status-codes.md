# HTTP Status Codes Reference

## Quick Reference Table

| Code | Constant | Meaning | When It Occurs | Action |
|------|----------|---------|----------------|--------|
| 200 | `HTTP_CODE_SUCCESS_200` | OK | Data retrieved successfully | Process data |
| 201 | `HTTP_CODE_SUCCESS_201` | Created | Resource created/updated | Return success |
| 204 | `HTTP_CODE_SUCCESS_204` | No Content | No data found or deleted | Handle empty response |
| 400 | - | Bad Request | Invalid input | Show validation errors |
| 404 | `HTTP_STATUS_CODE_NOT_FOUND` | Not Found | Resource doesn't exist | Show not found message |
| 409 | `HTTP_STATUS_CODE_CONFLICTS` | Conflict | Resource already exists or modified | Handle conflict |
| 40410 | `HTTP_STATUS_CODE_RESOURCE_DOES_NOT_EXIST` | Resource Not Exist | Specific not found error | Show not found message |
| 40909 | `HTTP_STATUS_CODE_ROUSOURCE_CHANGED` | Resource Changed | Optimistic locking conflict | Ask user to refresh |
| 40910 | - | Integrity Violation | Database constraint violated | Show constraint error |
| 40926 | `HTTP_STATUS_CODE_EXCLUSIVE_CONTROL` | Exclusive Control | Resource locked by another user | Show locked message |
| 500 | `HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR` | Server Error | Internal server error | Show error, contact support |
| 900 | `HTTP_STATUS_CODE_TIMEOUT_ERROR` | Timeout | Request timed out | Retry or show timeout message |

---

## Success Codes (2xx)

### 200 OK

**When**: GET request returns data successfully

**Response Structure**:
```json
{
  "code": 200,
  "body": {
    "data": [
      { "id": "123", "name": "John" }
    ]
  }
}
```

**Handling**:
```java
case HttpConstants.HTTP_CODE_SUCCESS_200:
    JsonArray data = responseData.getObject(JsonKeyConstants.BODY)
        .getArray(JsonKeyConstants.DATA);
    
    if (data.size() > 0) {
        JsonObject result = data.get(0);
        message.reply(result);
    } else {
        // Empty array - treat as 204
        message.reply(new JsonObject().putNumber("code", 204));
    }
    break;
```

---

### 201 Created

**When**: PUT request creates or updates resource successfully

**Response Structure**:
```json
{
  "code": 201,
  "body": {
    "data": {
      "id": "123",
      "status": "created"
    }
  }
}
```

**Handling**:
```java
case HttpConstants.HTTP_CODE_SUCCESS_201:
    container.logger().info(methodName + " - Resource created");
    message.reply(responseData);
    break;
```

---

### 204 No Content

**When**: 
- GET request finds no data
- DELETE request succeeds

**Response Structure**:
```json
{
  "code": 204
}
```

**Handling for GET**:
```java
case HttpConstants.HTTP_CODE_SUCCESS_204:
    container.logger().debug(methodName + " - No content found");
    
    JsonObject empty = new JsonObject();
    empty.putNumber("code", 204);
    empty.putString("message", "No data found");
    message.reply(empty);
    break;
```

**Handling for DELETE**:
```java
case HttpConstants.HTTP_CODE_SUCCESS_204:
    container.logger().info(methodName + " - Resource deleted");
    
    JsonObject result = new JsonObject();
    result.putNumber("code", 204);
    result.putString("message", "Deleted successfully");
    message.reply(result);
    break;
```

---

## Client Error Codes (4xx)

### 400 Bad Request

**When**: Invalid input data, validation failed

**Response Structure**:
```json
{
  "code": 400,
  "body": {
    "message": "Validation failed",
    "errors": [
      {"field": "email", "message": "Invalid format"}
    ]
  }
}
```

**Handling**:
```java
case 400:
    container.logger().warn(methodName + " - Bad request");
    
    JsonObject error = new JsonObject();
    error.putNumber("code", 400);
    error.putString("message", "Invalid request");
    
    // Extract validation errors if available
    if (responseData.containsField(JsonKeyConstants.BODY)) {
        JsonObject body = responseData.getObject(JsonKeyConstants.BODY);
        if (body.containsField("errors")) {
            error.putArray("errors", body.getArray("errors"));
        }
    }
    
    message.reply(error);
    break;
```

---

### 404 Not Found

**When**: Resource doesn't exist

**Response Structure**:
```json
{
  "code": 404,
  "body": {
    "message": "Resource not found"
  }
}
```

**Handling**:
```java
case HttpConstants.HTTP_STATUS_CODE_NOT_FOUND:
    container.logger().warn(methodName + " - Resource not found");
    
    JsonObject notFound = new JsonObject();
    notFound.putNumber("code", 404);
    notFound.putString("message", "Resource does not exist");
    message.reply(notFound);
    break;
```

---

### 409 Conflict

**When**: 
- Resource already exists
- Optimistic locking conflict (40909)
- Database constraint violation (40910)

**Response Structure**:
```json
{
  "code": 409,
  "body": {
    "message": {
      "code": 40909,
      "text": "Resource was modified"
    }
  }
}
```

**Handling**:
```java
case HttpConstants.HTTP_STATUS_CODE_CONFLICTS:
    JsonObject bodyObj = responseData.getObject(JsonKeyConstants.BODY);
    
    if (bodyObj != null && bodyObj.containsField(JsonKeyConstants.MESSAGE)) {
        JsonObject msgObj = bodyObj.getObject(JsonKeyConstants.MESSAGE);
        int errorCode = msgObj.getInteger(JsonKeyConstants.CODE);
        
        if (errorCode == HttpConstants.HTTP_STATUS_CODE_ROUSOURCE_CHANGED) {
            // 40909: Optimistic locking conflict
            container.logger().warn(methodName + " - Optimistic locking conflict");
            
            JsonObject conflict = new JsonObject();
            conflict.putNumber("code", 40909);
            conflict.putString("message", "Resource was modified by another user. Please refresh and try again.");
            message.reply(conflict);
            
        } else if (errorCode == HttpConstants.HTTP_STATUS_CODE_DATABASE_INTEGRITY_CONSTRAINT_VIOLATION) {
            // 40910: Database constraint violation
            container.logger().warn(methodName + " - Database constraint violation");
            
            JsonObject constraint = new JsonObject();
            constraint.putNumber("code", 40910);
            constraint.putString("message", "Database constraint violated. Cannot perform operation.");
            message.reply(constraint);
            
        } else {
            // Generic conflict
            container.logger().warn(methodName + " - Conflict");
            message.reply(responseData);
        }
    } else {
        message.reply(responseData);
    }
    break;
```

---

### 40410 Resource Does Not Exist

**When**: DELETE request for non-existent resource

**Handling**:
```java
case HttpConstants.HTTP_STATUS_CODE_RESOURCE_DOES_NOT_EXIST:
    container.logger().warn(methodName + " - Resource does not exist");
    
    JsonObject notExist = new JsonObject();
    notExist.putNumber("code", 40410);
    notExist.putString("message", "Resource does not exist");
    message.reply(notExist);
    break;
```

---

### 40926 Exclusive Control

**When**: Resource is locked by another user

**Handling**:
```java
case HttpConstants.HTTP_STATUS_CODE_EXCLUSIVE_CONTROL:
    container.logger().warn(methodName + " - Resource locked");
    
    JsonObject locked = new JsonObject();
    locked.putNumber("code", 40926);
    locked.putString("message", "Resource is locked by another user. Please try again later.");
    message.reply(locked);
    break;
```

---

## Server Error Codes (5xx)

### 500 Internal Server Error

**When**: Server-side error, data-api down, database error

**Response Structure**:
```json
{
  "code": 500,
  "body": {
    "message": "Internal server error"
  }
}
```

**Handling**:
```java
case HttpConstants.HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR:
    container.logger().error(methodName + " - Server error: " + responseData.toString());
    
    JsonObject serverError = new JsonObject();
    serverError.putNumber("code", 500);
    serverError.putString("message", "Internal server error. Please contact support.");
    serverError.putString("timestamp", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
    message.reply(serverError);
    break;
```

---

### 900 Timeout Error

**When**: Request exceeds timeout (default 5000ms)

**Handling**:
```java
case HttpConstants.HTTP_STATUS_CODE_TIMEOUT_ERROR:
    container.logger().error(methodName + " - Request timed out");
    
    JsonObject timeout = new JsonObject();
    timeout.putNumber("code", 900);
    timeout.putString("message", "Request timed out. Please try again.");
    message.reply(timeout);
    break;
```

**With Retry Logic**:
```java
if (th != null && code == HttpConstants.HTTP_STATUS_CODE_TIMEOUT_ERROR) {
    if (retryCount < MAX_RETRIES) {
        container.logger().warn(methodName + " - Timeout, retrying");
        vertx.setTimer(1000, timerId -> {
            callWithRetry(param, message, retryCount + 1);
        });
        return;
    }
}
```

---

## Default Case (Unexpected Codes)

**Always include a default case** to handle unexpected status codes:

```java
default:
    container.logger().error(methodName + " - Unexpected code: " + code);
    container.logger().error(methodName + " - Response: " + responseData.toString());
    
    JsonObject unexpected = new JsonObject();
    unexpected.putNumber("code", code);
    unexpected.putString("message", "Unexpected error occurred");
    unexpected.putObject("details", responseData);
    message.reply(unexpected);
    break;
```

---

## Constants Location

All HTTP status code constants are defined in:

**File**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/constants/HttpConstants.java`

```java
public class HttpConstants {
    public static final int HTTP_CODE_SUCCESS_200 = 200;
    public static final int HTTP_CODE_SUCCESS_201 = 201;
    public static final int HTTP_CODE_SUCCESS_204 = 204;
    public static final int HTTP_STATUS_CODE_NOT_FOUND = 404;
    public static final int HTTP_STATUS_CODE_CONFLICTS = 409;
    public static final int HTTP_STATUS_CODE_RESOURCE_DOES_NOT_EXIST = 40410;
    public static final int HTTP_STATUS_CODE_ROUSOURCE_CHANGED = 40909;
    public static final int HTTP_STATUS_CODE_DATABASE_INTEGRITY_CONSTRAINT_VIOLATION = 40910;
    public static final int HTTP_STATUS_CODE_EXCLUSIVE_CONTROL = 40926;
    public static final int HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR = 500;
    public static final int HTTP_STATUS_CODE_TIMEOUT_ERROR = 900;
}
```

---

## Decision Tree

```
Response received
│
├─ th != null?
│  ├─ Yes → Check code
│  │  ├─ 900 → Timeout (retry?)
│  │  └─ Other → Server error
│  └─ No → Check code
│
└─ Check code:
   ├─ 200 → Success (process data)
   ├─ 201 → Created (return success)
   ├─ 204 → No content (handle empty)
   ├─ 400 → Bad request (validation error)
   ├─ 404 → Not found (show message)
   ├─ 409 → Conflict (check sub-code)
   │  ├─ 40909 → Optimistic locking
   │  └─ 40910 → Constraint violation
   ├─ 500 → Server error (log and notify)
   ├─ 900 → Timeout (retry or fail)
   └─ Other → Unexpected (log and fail)
```

---

## Checklist

When handling status codes, verify:

- [ ] Handled 200 (Success)
- [ ] Handled 201 (Created) for PUT
- [ ] Handled 204 (No Content) for GET/DELETE
- [ ] Handled 404 (Not Found)
- [ ] Handled 409 (Conflict) with sub-codes
- [ ] Handled 500 (Server Error)
- [ ] Handled 900 (Timeout)
- [ ] Included `default:` case
- [ ] Used constants from `HttpConstants.java`
- [ ] Logged appropriate level (debug/info/warn/error)
- [ ] Returned meaningful error messages

---

**Related**: 
- Error handling: `06-error-handling.md`
- Templates: `01-get-templates.md`, `02-put-templates.md`, `03-delete-templates.md`
