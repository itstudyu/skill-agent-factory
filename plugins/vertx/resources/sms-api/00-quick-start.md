# SMS-API Quick Start Guide

**FOR AI**: Read this first for SMS-API usage.

## What is SMS-API?

SMS-API is used for **SMS message delivery** including:
- Direct SMS sending
- SMS notifications
- Text message delivery

**Key Use Case**: Send SMS messages directly to phone numbers.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Would contain postSMSAPI()
└── CallBack.java                # Callback for SMS-API responses
```

**API Definition:**
```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/APIClientPool.java
- Line 58: SMS_API constant defined
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Likely uses POST method for SMS sending**
2. ⚠️ **Always use generic CallBack (no specialized callback)**
3. ⚠️ **Check if (th != null) FIRST in callback**
4. ⚠️ **Validate phone number format before sending**
5. ⚠️ **Success code likely 200 OK or 202 Accepted**

---

## Basic Pattern (Hypothetical)

```java
final DataAccess da = new DataAccess(container, vertx);

// Build SMS request
JsonObject requestBody = new JsonObject();
requestBody.putString("to", "090-1234-5678");
requestBody.putString("message", "Your verification code is: 123456");

// Call SMS-API
da.postSMSAPI("send", requestBody, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (th != null) {
                container.logger().error("SMS API error", th);
                message.reply(JsonUtil.createReplyObjectFail(th));
                return;
            }
            
            if (code == 200 || code == 202) {
                container.logger().info("SMS sent successfully");
                message.reply(new JsonObject()
                    .putNumber("code", 200)
                    .putString("message", "SMS sent"));
            } else {
                container.logger().error("SMS failed: " + code);
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

## When to Use SMS-API

✅ **Use SMS-API when:**
- Sending direct SMS messages
- Sending verification codes
- Sending alerts/notifications via SMS
- Sending SMS without templates

❌ **Don't use SMS-API for:**
- Template-based notifications → Use Notice-API
- Email notifications → Use Mail-API or Notice-API
- Combined email + SMS → Use Notice-API

---

## Request Body Structure (Hypothetical)

```json
{
  "to": "090-1234-5678",
  "message": "Your verification code is: 123456",
  "from": "Company Name"
}
```

---

## Important Notes

⚠️ **WARNING**: No actual usage examples found in the codebase.

Before using SMS-API:
1. Check DataAccess.java for actual method signatures
2. Verify endpoint format and parameters
3. Confirm request body structure
4. Validate phone number format
5. Check API documentation for specific requirements
6. Consider using Notice-API for template-based SMS

---

## Checklist

Before writing SMS-API code, verify:

- [ ] Confirmed actual method name in DataAccess.java
- [ ] Validated phone number format
- [ ] Used generic `CallBack`
- [ ] Checked `if (th != null)` FIRST
- [ ] Handled success codes (200/202)
- [ ] Wrapped callback logic in try-catch
- [ ] Logged SMS details
- [ ] Considered Notice-API as alternative

---

**Related**: 
- Complete template: `01-sms-api-template.md`
- Notice-API: For template-based SMS + email

---

**⚠️ IMPORTANT**: This is a hypothetical guide based on API naming conventions. Please verify actual implementation in your codebase before use.
