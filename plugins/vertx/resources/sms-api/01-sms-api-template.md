# SMS-API Template

**⚠️ WARNING**: No actual usage examples found in the codebase. This template is based on common SMS API patterns.

---

## Template 1: Send SMS (Hypothetical)

**Use this to send SMS message.**

```java
public void sendSMS(String phoneNumber, String message, final Message<JsonObject> messageObj) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate phone number
        if (StringUtil.isNullOrEmpty(phoneNumber)) {
            messageObj.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Phone number is required"));
            return;
        }
        
        // Validate message
        if (StringUtil.isNullOrEmpty(message)) {
            messageObj.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Message content is required"));
            return;
        }
        
        // Validate message length (typical SMS limit: 160 characters)
        if (message.length() > 160) {
            container.logger().warn("Message exceeds 160 characters: " + message.length());
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build request body
        JsonObject requestBody = new JsonObject();
        requestBody.putString("to", phoneNumber);
        requestBody.putString("message", message);
        
        container.logger().debug("Sending SMS to: " + phoneNumber);
        
        // Call SMS-API (method name may vary - check DataAccess.java)
        da.postSMSAPI("send", requestBody, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    container.logger().debug(LogConstants.CODE + code);
                    
                    // STEP 1: Check exception FIRST
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        messageObj.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    // STEP 2: Handle status codes
                    if (code == 200 || code == 202) {
                        container.logger().info(methodName + " - SMS sent successfully");
                        messageObj.reply(new JsonObject()
                            .putNumber("code", 200)
                            .putString("message", "SMS sent successfully"));
                    } else {
                        container.logger().error(methodName + " - SMS failed: " + code);
                        messageObj.reply(new JsonObject()
                            .putNumber("code", code)
                            .putString("message", "SMS sending failed"));
                    }
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    messageObj.reply(new JsonObject().putNumber("code", 500));
                }
            }
        });
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        messageObj.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Template 2: Send Verification Code (Hypothetical)

**Use this to send verification code via SMS.**

```java
public void sendVerificationCode(String phoneNumber, String code, 
        final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate inputs
        if (StringUtil.isNullOrEmpty(phoneNumber)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Phone number is required"));
            return;
        }
        
        if (StringUtil.isNullOrEmpty(code)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Verification code is required"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build message
        String messageText = "Your verification code is: " + code + ". Valid for 5 minutes.";
        
        // Build request body
        JsonObject requestBody = new JsonObject();
        requestBody.putString("to", phoneNumber);
        requestBody.putString("message", messageText);
        requestBody.putString("type", "verification");
        
        container.logger().info("Sending verification code to: " + phoneNumber);
        
        // Call SMS-API
        da.postSMSAPI("send", requestBody, new CallBack() {
            @Override
            public void callBack(int responseCode, JsonObject responseData, Throwable th) {
                try {
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    if (responseCode == 200 || responseCode == 202) {
                        container.logger().info(methodName + " - Verification code sent");
                        message.reply(new JsonObject()
                            .putNumber("code", 200)
                            .putString("message", "Verification code sent"));
                    } else {
                        container.logger().error(methodName + " - Failed: " + responseCode);
                        message.reply(new JsonObject()
                            .putNumber("code", responseCode)
                            .putString("message", "Failed to send verification code"));
                    }
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
        });
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Template 3: Bulk SMS (Hypothetical)

**Use this to send SMS to multiple recipients.**

```java
public void sendBulkSMS(List<String> phoneNumbers, String message, 
        final Message<JsonObject> messageObj) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate inputs
        if (phoneNumbers == null || phoneNumbers.isEmpty()) {
            messageObj.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Phone numbers list is empty"));
            return;
        }
        
        if (StringUtil.isNullOrEmpty(message)) {
            messageObj.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Message content is required"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        final AtomicInteger successCount = new AtomicInteger(0);
        final AtomicInteger failCount = new AtomicInteger(0);
        final AtomicInteger completedCount = new AtomicInteger(0);
        final int totalCount = phoneNumbers.size();
        
        container.logger().info("Sending bulk SMS to " + totalCount + " recipients");
        
        // Send to each recipient
        for (final String phoneNumber : phoneNumbers) {
            JsonObject requestBody = new JsonObject();
            requestBody.putString("to", phoneNumber);
            requestBody.putString("message", message);
            
            da.postSMSAPI("send", requestBody, new CallBack() {
                @Override
                public void callBack(int code, JsonObject responseData, Throwable th) {
                    try {
                        if (th != null || (code != 200 && code != 202)) {
                            failCount.incrementAndGet();
                            container.logger().warn("SMS failed for: " + phoneNumber);
                        } else {
                            successCount.incrementAndGet();
                        }
                        
                        // Check if all completed
                        if (completedCount.incrementAndGet() == totalCount) {
                            container.logger().info("Bulk SMS completed - Success: " 
                                + successCount.get() + ", Failed: " + failCount.get());
                            
                            messageObj.reply(new JsonObject()
                                .putNumber("code", 200)
                                .putNumber("total", totalCount)
                                .putNumber("success", successCount.get())
                                .putNumber("failed", failCount.get()));
                        }
                        
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        if (completedCount.get() == totalCount) {
                            messageObj.reply(new JsonObject().putNumber("code", 500));
                        }
                    }
                }
            });
        }
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        messageObj.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Common Patterns (Hypothetical)

### Pattern 1: Phone Number Validation

```java
// Validate phone number format
private boolean isValidPhoneNumber(String phoneNumber) {
    if (StringUtil.isNullOrEmpty(phoneNumber)) {
        return false;
    }
    
    // Remove hyphens and spaces
    String cleaned = phoneNumber.replaceAll("[\\s-]", "");
    
    // Check Japanese mobile format (090/080/070)
    return cleaned.matches("^(090|080|070)\\d{8}$");
}

// Usage
if (!isValidPhoneNumber(phoneNumber)) {
    message.reply(new JsonObject()
        .putNumber("code", 400)
        .putString("message", "Invalid phone number format"));
    return;
}
```

### Pattern 2: Message Length Check

```java
// Check and truncate message if needed
private String prepareMessage(String message) {
    final int MAX_LENGTH = 160;
    
    if (message.length() > MAX_LENGTH) {
        container.logger().warn("Message truncated from " + message.length() + " to " + MAX_LENGTH);
        return message.substring(0, MAX_LENGTH - 3) + "...";
    }
    
    return message;
}
```

### Pattern 3: Retry on Failure

```java
// Retry SMS sending on failure
private void sendSMSWithRetry(String phoneNumber, String message, int retryCount,
        final Message<JsonObject> messageObj) {
    final int maxRetries = 3;
    
    da.postSMSAPI("send", requestBody, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            if (th != null || (code != 200 && code != 202)) {
                if (retryCount < maxRetries) {
                    container.logger().warn("SMS failed, retrying... (" 
                        + (retryCount + 1) + "/" + maxRetries + ")");
                    
                    // Retry after delay
                    vertx.setTimer(2000, new Handler<Long>() {
                        @Override
                        public void handle(Long timerId) {
                            sendSMSWithRetry(phoneNumber, message, retryCount + 1, messageObj);
                        }
                    });
                } else {
                    container.logger().error("SMS failed after " + maxRetries + " retries");
                    messageObj.reply(new JsonObject().putNumber("code", 500));
                }
            } else {
                container.logger().info("SMS sent successfully");
                messageObj.reply(new JsonObject().putNumber("code", 200));
            }
        }
    });
}
```

---

## HTTP Status Codes (Expected)

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | SMS sent successfully |
| 202 | Accepted | SMS accepted and queued for delivery |
| 400 | Bad Request | Invalid phone number or message |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal error |

---

## Request Body Structure (Hypothetical)

```json
{
  "to": "090-1234-5678",
  "message": "Your verification code is: 123456",
  "from": "Company Name",
  "type": "verification"
}
```

---

## Response Format (Expected)

```json
{
  "code": 200,
  "messageId": "msg_12345",
  "status": "sent"
}
```

---

## Checklist

Before writing SMS-API code, verify:

- [ ] **Confirmed actual method name in DataAccess.java**
- [ ] **Checked endpoint format and parameters**
- [ ] Validated phone number format
- [ ] Checked message length (typically 160 chars)
- [ ] Used generic `CallBack`
- [ ] Checked `if (th != null)` FIRST
- [ ] Handled success codes (200/202)
- [ ] Wrapped callback logic in try-catch
- [ ] Logged SMS details (without sensitive data)
- [ ] Considered Notice-API as alternative

---

## Common Mistakes

### ❌ Mistake 1: Not Validating Phone Number

```java
// WRONG: Sending without validation
da.postSMSAPI("send", requestBody, callback);
```

### ✅ Fix: Validate First

```java
// CORRECT: Validate phone number
if (StringUtil.isNullOrEmpty(phoneNumber)) {
    message.reply(new JsonObject()
        .putNumber("code", 400)
        .putString("message", "Phone number is required"));
    return;
}

if (!isValidPhoneNumber(phoneNumber)) {
    message.reply(new JsonObject()
        .putNumber("code", 400)
        .putString("message", "Invalid phone number format"));
    return;
}

da.postSMSAPI("send", requestBody, callback);
```

### ❌ Mistake 2: Ignoring Message Length

```java
// WRONG: Sending long message without checking
requestBody.putString("message", veryLongMessage);
```

### ✅ Fix: Check and Truncate

```java
// CORRECT: Check length
final int MAX_LENGTH = 160;
String message = originalMessage;

if (message.length() > MAX_LENGTH) {
    container.logger().warn("Message truncated");
    message = message.substring(0, MAX_LENGTH - 3) + "...";
}

requestBody.putString("message", message);
```

---

## SMS-API vs Notice-API

| Feature | SMS-API | Notice-API |
|---------|---------|------------|
| Purpose | Direct SMS sending | Template-based notifications |
| Templates | No | Yes (noticeId) |
| Email support | No | Yes |
| Bulk sending | Manual loop | Built-in (receptions array) |
| Use case | Simple SMS | Complex notifications |

**Recommendation**: Use Notice-API for template-based notifications with SMS + email support.

---

## Important Notes

⚠️ **CRITICAL**: This documentation is hypothetical. Before using SMS-API:

1. **Check DataAccess.java** for actual method signatures:
   ```java
   // Look for methods like:
   public void postSMSAPI(String param, JsonObject body, CallBack callback)
   public void getSMSAPI(String param, CallBack callback)
   ```

2. **Verify API endpoint format** in your API documentation

3. **Test with your own phone number** first

4. **Check rate limits** to avoid throttling

5. **Consider Notice-API** for template-based SMS

6. **Consult API documentation** for specific requirements

---

**Related**: 
- Quick start: `00-quick-start.md`
- Notice-API: For template-based SMS + email
- Mail-API: For email notifications

---

**⚠️ REMINDER**: No actual usage examples found in the codebase. This is a hypothetical guide based on common patterns. Always verify actual implementation before use.
