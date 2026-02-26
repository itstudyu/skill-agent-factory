# Notice-API Template

## Template 1: Send Email Notification

**Use this to send email notification using a template.**

```java
public void sendEmailNotification(String noticeId, String email, String payerId, 
        String payNumber, JsonObject customFields, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate required parameters
        if (StringUtil.isNullOrEmpty(email)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Email is required"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build receptions
        JsonArray receptions = new JsonArray();
        JsonObject reception = new JsonObject();
        reception.putString("to", email);
        reception.putString("payer", payerId);
        reception.putString("paynumber", payNumber);
        
        // Add custom fields if provided
        if (customFields != null && customFields.size() > 0) {
            reception.putObject("fields", customFields);
        }
        
        receptions.add(reception);
        
        // Build request body
        JsonObject requestBody = new JsonObject();
        requestBody.putString("applicationId", Constant.APP_ID);
        requestBody.putString("noticeId", noticeId);
        requestBody.putString("platform", platformId);
        requestBody.putArray("receptions", receptions);
        
        container.logger().debug("Sending notification: noticeId=" + noticeId + ", to=" + email);
        
        // Call Notice-API
        da.postNoticeAPI("epay", requestBody, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    container.logger().debug(LogConstants.CODE + code);
                    
                    // STEP 1: Check exception FIRST
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    // STEP 2: Check for 202 Accepted
                    if (code == HttpConstants.HTTP_CODE_SUCCESS_202) {
                        container.logger().info(methodName + " - Notification sent successfully");
                        message.reply(new JsonObject()
                            .putNumber("code", 200)
                            .putString("message", "Notification sent"));
                    } else {
                        container.logger().error(methodName + " - Notification failed: " + code);
                        message.reply(new JsonObject()
                            .putNumber("code", code)
                            .putString("message", "Notification failed"));
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

## Template 2: Send Email + SMS Notification

**Use this to send both email and SMS notifications.**

```java
public void sendEmailAndSMS(String noticeId, String email, String phone, 
        String payerId, String payNumber, JsonObject customFields, 
        final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate required parameters
        if (StringUtil.isNullOrEmpty(email)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Email is required"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build receptions
        JsonArray receptions = new JsonArray();
        JsonObject reception = new JsonObject();
        reception.putString("to", email);
        reception.putString("payer", payerId);
        reception.putString("paynumber", payNumber);
        
        // Add phone number for SMS
        if (!StringUtil.isNullOrEmpty(phone)) {
            reception.putString("toPhone", phone);
        } else {
            container.logger().warn("Phone number not provided - SMS will be skipped");
        }
        
        // Add custom fields
        if (customFields != null && customFields.size() > 0) {
            reception.putObject("fields", customFields);
        }
        
        receptions.add(reception);
        
        // Build request body
        JsonObject requestBody = new JsonObject();
        requestBody.putString("applicationId", Constant.APP_ID);
        requestBody.putString("noticeId", noticeId);
        requestBody.putString("platform", platformId);
        requestBody.putArray("receptions", receptions);
        
        container.logger().debug("Sending email+SMS: noticeId=" + noticeId);
        
        // Call Notice-API
        da.postNoticeAPI("epay", requestBody, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    if (code == HttpConstants.HTTP_CODE_SUCCESS_202) {
                        container.logger().info(methodName + " - Notification sent");
                        message.reply(new JsonObject().putNumber("code", 200));
                    } else {
                        container.logger().error(methodName + " - Failed: " + code);
                        message.reply(new JsonObject().putNumber("code", code));
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

## Template 3: Send to Multiple Recipients

**Use this to send notifications to multiple recipients.**

```java
public void sendBulkNotification(String noticeId, List<RecipientData> recipients, 
        JsonObject commonFields, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        if (recipients == null || recipients.isEmpty()) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Recipients list is empty"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build receptions for all recipients
        JsonArray receptions = new JsonArray();
        
        for (RecipientData recipient : recipients) {
            JsonObject reception = new JsonObject();
            reception.putString("to", recipient.email);
            reception.putString("payer", recipient.payerId);
            reception.putString("paynumber", recipient.payNumber);
            
            // Add phone if available
            if (!StringUtil.isNullOrEmpty(recipient.phone)) {
                reception.putString("toPhone", recipient.phone);
            }
            
            // Add recipient-specific fields
            if (recipient.fields != null && recipient.fields.size() > 0) {
                reception.putObject("fields", recipient.fields);
            }
            
            receptions.add(reception);
        }
        
        // Build request body
        JsonObject requestBody = new JsonObject();
        requestBody.putString("applicationId", Constant.APP_ID);
        requestBody.putString("noticeId", noticeId);
        requestBody.putString("platform", platformId);
        requestBody.putArray("receptions", receptions);
        
        // Add common fields if provided
        if (commonFields != null && commonFields.size() > 0) {
            requestBody.putObject("common_fields", commonFields);
        }
        
        container.logger().info("Sending bulk notification to " + recipients.size() + " recipients");
        
        // Call Notice-API
        da.postNoticeAPI("epay", requestBody, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    if (code == HttpConstants.HTTP_CODE_SUCCESS_202) {
                        container.logger().info(methodName + " - Bulk notification sent");
                        message.reply(new JsonObject()
                            .putNumber("code", 200)
                            .putNumber("recipientCount", recipients.size()));
                    } else {
                        container.logger().error(methodName + " - Failed: " + code);
                        message.reply(new JsonObject().putNumber("code", code));
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

// Helper class for recipient data
private static class RecipientData {
    String email;
    String phone;
    String payerId;
    String payNumber;
    JsonObject fields;
    
    RecipientData(String email, String payerId, String payNumber) {
        this.email = email;
        this.payerId = payerId;
        this.payNumber = payNumber;
    }
}
```

---

## Real Example from Codebase

**File**: `src/main/java/jp/co/payroll/p3/storerevampapplication/nyusyahatureview/service/mail/NoticeHandler.java`  
**Line**: 224

```java
private void sendNotice(final NoticeData data,
        final Handler<Void> successHandler, final Handler<Throwable> errorHandler) {

    logger.debug("sendNotice: Notice API呼び出し開始 ejsrak3=" + data.ejsrak3);

    // Build receptions
    JsonArray receptions = new JsonArray();
    JsonObject reception = new JsonObject();
    
    // Add email
    jp.co.payroll.p3.storerevampapplication.nyusyahatureview.util.JsonUtil
        .putIfNotEmpty(reception, "to", data.email);
    reception.putString("payer", data.payerId);
    reception.putString("paynumber", data.payNumber);

    // Add phone for SMS if notification type is 1000 (Email + SMS)
    if ("1000".equals(data.noticeType)) {
        if (!StringUtil.isNullOrEmpty(data.phone)) {
            reception.putString("toPhone", data.phone);
        } else {
            logger.warn("sendNotice: 通知種別=1000だが電話番号がありません ejsrak3=" + data.ejsrak3);
        }
    }

    // Build recipient-specific fields
    JsonObject fields = new JsonObject();
    fields.putString("recruit_name", data.recruitName);
    fields.putString("recruit_number", data.recruitNumber);
    fields.putString("ejsrak3", data.ejsrak3);
    fields.putString("target_application", data.targetApplication);
    fields.putString("rejection_reason", data.rejectionReason);
    reception.putObject("fields", fields);
    receptions.add(reception);

    // Build common fields (shared by all recipients)
    JsonObject commonFields = new JsonObject();
    commonFields.putString("company_code", data.companyCode);

    // Build request body
    JsonObject requestBody = new JsonObject();
    requestBody.putString("applicationId", Constant.APP_ID);
    requestBody.putString("noticeId", NOTICE_ID_REJECTION);  // "N0008"
    requestBody.putString("platform", data.platformId);
    requestBody.putObject("common_fields", commonFields);
    requestBody.putArray("receptions", receptions);

    // Call Notice-API
    new DataAccess(container, vertx).postNoticeAPI("epay", requestBody, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            if (th != null) {
                logger.error("sendNotice: Notice API呼び出しエラー", th);
                errorHandler.handle(th);
                return;
            }

            // 202 Accepted = success
            if (code == HttpConstants.HTTP_CODE_SUCCESS_202) {
                logger.info("sendNotice: 通知送信成功 ejsrak3=" + data.ejsrak3);
                successHandler.handle(null);
            } else {
                logger.error("sendNotice: 通知送信失敗 code=" + code + " ejsrak3=" + data.ejsrak3);
                errorHandler.handle(new Exception("通知送信失敗: code=" + code));
            }
        }
    });
}
```

---

## Common Patterns

### Pattern 1: Conditional SMS

```java
// Send SMS only if phone number is provided
JsonObject reception = new JsonObject();
reception.putString("to", email);
reception.putString("payer", payerId);
reception.putString("paynumber", payNumber);

// Add phone conditionally
if (!StringUtil.isNullOrEmpty(phone)) {
    reception.putString("toPhone", phone);
} else {
    container.logger().info("Phone not provided - email only");
}
```

### Pattern 2: Common Fields + Recipient Fields

```java
// Common fields (shared by all recipients)
JsonObject commonFields = new JsonObject();
commonFields.putString("company_name", "株式会社ABC");
commonFields.putString("support_email", "support@example.com");

// Recipient-specific fields
JsonObject fields = new JsonObject();
fields.putString("user_name", "田中太郎");
fields.putString("user_id", "U12345");

reception.putObject("fields", fields);
requestBody.putObject("common_fields", commonFields);
```

### Pattern 3: Async Notification with Callback

```java
// Send notification asynchronously
public void sendNotificationAsync(String noticeId, String email, 
        final Handler<Void> successHandler, final Handler<Throwable> errorHandler) {
    
    // ... build request body ...
    
    da.postNoticeAPI("epay", requestBody, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            if (th != null) {
                errorHandler.handle(th);
                return;
            }
            
            if (code == HttpConstants.HTTP_CODE_SUCCESS_202) {
                successHandler.handle(null);
            } else {
                errorHandler.handle(new Exception("Notification failed: " + code));
            }
        }
    });
}
```

### Pattern 4: Retry on Failure

```java
// Retry notification on failure
private void sendWithRetry(JsonObject requestBody, int retryCount, 
        final Message<JsonObject> message) {
    final int maxRetries = 3;
    
    da.postNoticeAPI("epay", requestBody, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            if (th != null || code != HttpConstants.HTTP_CODE_SUCCESS_202) {
                if (retryCount < maxRetries) {
                    container.logger().warn("Notification failed, retrying... (" 
                        + (retryCount + 1) + "/" + maxRetries + ")");
                    
                    // Retry after delay
                    vertx.setTimer(2000, new Handler<Long>() {
                        @Override
                        public void handle(Long timerId) {
                            sendWithRetry(requestBody, retryCount + 1, message);
                        }
                    });
                } else {
                    container.logger().error("Notification failed after " + maxRetries + " retries");
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            } else {
                container.logger().info("Notification sent successfully");
                message.reply(new JsonObject().putNumber("code", 200));
            }
        }
    });
}
```

---

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 202 | Accepted | Notification accepted and queued for delivery |
| 400 | Bad Request | Invalid request body or missing required fields |
| 404 | Not Found | Notice template (noticeId) not found |
| 500 | Server Error | Internal error |

---

## Request Body Fields

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `applicationId` | String | Application identifier |
| `noticeId` | String | Notification template ID (e.g., "N0001") |
| `platform` | String | Platform ID |
| `receptions` | Array | List of recipients |

### Reception Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | String | Yes | Email address |
| `payer` | String | Yes | Payer ID |
| `paynumber` | String | Yes | Pay number |
| `toPhone` | String | No | Phone number for SMS |
| `fields` | Object | No | Recipient-specific custom fields |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `common_fields` | Object | Fields shared by all recipients |

---

## Checklist

Before writing Notice-API code, verify:

- [ ] Used `postNoticeAPI()` method (POST only)
- [ ] Used generic `CallBack` (not specialized)
- [ ] Checked `if (th != null)` FIRST
- [ ] Success code is 202 Accepted (not 200)
- [ ] Request body includes: applicationId, noticeId, platform, receptions
- [ ] Each reception has: to, payer, paynumber
- [ ] Validated email address before sending
- [ ] Added phone number only if SMS is required
- [ ] Wrapped callback logic in try-catch
- [ ] Logged notification details

---

## Common Mistakes

### ❌ Mistake 1: Wrong Success Code

```java
// WRONG: Checking for 200 or 201
if (code == 200 || code == 201) {
    // Success
}
```

### ✅ Fix: Check for 202

```java
// CORRECT: Notice-API returns 202 Accepted
if (code == HttpConstants.HTTP_CODE_SUCCESS_202) {
    // Success
}
```

### ❌ Mistake 2: Missing Required Fields

```java
// WRONG: Missing payer or paynumber
JsonObject reception = new JsonObject();
reception.putString("to", email);
// Missing payer and paynumber!
```

### ✅ Fix: Include All Required Fields

```java
// CORRECT: All required fields
JsonObject reception = new JsonObject();
reception.putString("to", email);
reception.putString("payer", payerId);
reception.putString("paynumber", payNumber);
```

### ❌ Mistake 3: Not Validating Email

```java
// WRONG: Sending without validation
da.postNoticeAPI("epay", requestBody, callback);
```

### ✅ Fix: Validate Before Sending

```java
// CORRECT: Validate email first
if (StringUtil.isNullOrEmpty(email)) {
    message.reply(new JsonObject()
        .putNumber("code", 400)
        .putString("message", "Email is required"));
    return;
}

da.postNoticeAPI("epay", requestBody, callback);
```

---

## Notice-API Summary

| Operation | Method | Endpoint | Success Code | Response |
|-----------|--------|----------|--------------|----------|
| Send notification | `postNoticeAPI()` | `/epay` | 202 | Accepted |

**Key Points:**
- POST only (no GET)
- Success = 202 Accepted
- Template-based (noticeId)
- Supports email + SMS
- Supports bulk sending

---

**Related**: 
- Quick start: `00-quick-start.md`
- Mail-API: Direct email sending
- SMS-API: Direct SMS sending
