# Notice-API Quick Start Guide

**FOR AI**: Read this first for Notice-API usage.

## What is Notice-API?

Notice-API is used for **notification delivery** including:
- Email notifications
- SMS notifications
- Combined email + SMS notifications
- Template-based notifications

**Key Use Case**: Send notifications (mail/SMS) to users using predefined templates.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains postNoticeAPI()
└── CallBack.java                # Callback for Notice-API responses
```

**Real Example:**
```
src/main/java/jp/co/payroll/p3/storerevampapplication/nyusyahatureview/service/mail/
└── NoticeHandler.java           # Notice-API usage for rejection notifications
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Always use POST method (postNoticeAPI)**
2. ⚠️ **Always use generic CallBack (no specialized callback)**
3. ⚠️ **Success code is 202 Accepted (not 200 or 201)**
4. ⚠️ **Request body must include: applicationId, noticeId, platform, receptions**
5. ⚠️ **Each reception must have: to (email), payer, paynumber**

---

## Basic Pattern

```java
final DataAccess da = new DataAccess(container, vertx);

// Build request body
JsonObject requestBody = new JsonObject();
requestBody.putString("applicationId", Constant.APP_ID);
requestBody.putString("noticeId", "N0001");  // Template ID
requestBody.putString("platform", platformId);

// Build receptions (recipients)
JsonArray receptions = new JsonArray();
JsonObject reception = new JsonObject();
reception.putString("to", "user@example.com");
reception.putString("payer", payerId);
reception.putString("paynumber", payNumber);

// Optional: Add custom fields
JsonObject fields = new JsonObject();
fields.putString("user_name", "田中太郎");
fields.putString("message", "承認されました");
reception.putObject("fields", fields);

receptions.add(reception);
requestBody.putArray("receptions", receptions);

// Call Notice-API
da.postNoticeAPI("epay", requestBody, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (th != null) {
                container.logger().error("Notice API error", th);
                message.reply(JsonUtil.createReplyObjectFail(th));
                return;
            }
            
            if (code == 202) {  // 202 Accepted
                container.logger().info("Notification sent successfully");
                message.reply(new JsonObject().putNumber("code", 200));
            } else {
                container.logger().error("Notification failed: " + code);
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

## When to Use Notice-API

✅ **Use Notice-API when:**
- Sending email notifications
- Sending SMS notifications
- Using predefined notification templates
- Sending notifications to multiple recipients
- Sending notifications with dynamic fields

❌ **Don't use Notice-API for:**
- Direct email sending without templates → Use Mail-API
- SMS without templates → Use SMS-API
- Real-time messaging → Use different mechanism

---

## Request Body Structure

```json
{
  "applicationId": "app-id",
  "noticeId": "N0001",
  "platform": "platform-id",
  "common_fields": {
    "company_code": "COMP001"
  },
  "receptions": [
    {
      "to": "user@example.com",
      "toPhone": "090-1234-5678",
      "payer": "payer-id",
      "paynumber": "pay-number",
      "fields": {
        "user_name": "田中太郎",
        "custom_field": "value"
      }
    }
  ]
}
```

---

## Response Format

### Success Response (202 Accepted)

```json
{
  "code": 202,
  "message": "Notification accepted"
}
```

---

## Related Guide

- **Complete Template**: `01-notice-api-template.md`

---

**Start here, then read the complete template for detailed examples.**
