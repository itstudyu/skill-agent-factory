# SLkey (Master Data) Template

## What is SLkey?

SLkey (System Lookup Key) is used to fetch master data / lookup tables from the MPSL table. It returns key-value pairs for dropdown lists, radio buttons, and other selection UI components.

**Example**: User types (Admin, User, Guest), Status codes (Active, Inactive), etc.

---

## Template: Get SLkey with CallBackSLkey

**Use this to get master data as a TreeMap.**

```java
public void methodName(String classId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    da.getSLkey(classId, new CallBackSLkey() {
        @Override
        public void callBack(int code, TreeMap<String, String> map, Throwable th) {
            try {
                container.logger().debug(LogConstants.CODE + code);
                
                // STEP 1: Check exception FIRST
                if (th != null) {
                    replyFail(message, th, code);
                    return;
                }
                
                // STEP 2: Handle status codes
                if (code == HttpConstants.HTTP_CODE_SUCCESS_200) {
                    JsonArray resultArray = new JsonArray();
                    
                    // Convert TreeMap to JsonArray
                    for (Map.Entry<String, String> entry : map.entrySet()) {
                        JsonObject item = new JsonObject();
                        item.putString("code", entry.getKey());
                        item.putString("name", entry.getValue());
                        resultArray.add(item);
                    }
                    
                    JsonObject result = new JsonObject();
                    result.putNumber("code", 200);
                    result.putArray("data", resultArray);
                    
                    message.reply(result);
                } else {
                    JsonObject joErr = new JsonObject();
                    joErr.putNumber("code", code);
                    joErr.putString("message", "Failed to fetch SLkey");
                    container.logger().error(methodName + LogConstants.ERROR + joErr);
                    message.reply(joErr);
                }
            } catch (Throwable e) {
                replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
            }
        }
    });
}
```

---

## Template: Get SLkey with CallBackGet (Raw Response)

**Use this when you want the raw API response.**

```java
public void methodName(String classId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    da.getSLkey(classId, new CallBackGet(methodName, container, message) {
        @Override
        public void ok(JsonObject responseData) {
            container.logger().debug(methodName + " - Success");
            super.ok(responseData);
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

## Template: Get SLkey with Language Parameter

**Use this for multi-language support.**

```java
public void methodName(String classId, String lang, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().debug(methodName + LogConstants.START);
    
    final DataAccess da = new DataAccess(container, vertx);
    
    da.getSLkey(classId, lang, new CallBackGet(methodName, container, message) {
        @Override
        public void ok(JsonObject responseData) {
            container.logger().debug(methodName + " - Success (lang: " + lang + ")");
            super.ok(responseData);
        }
    });
}
```

---

## Real Example from Codebase

**File**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/filter/Common_CustomFilter_SLkey.java`  
**Line**: 101

```java
final String nonPlatformID = container.config().getString(ScreenConstants.NON_PLATFORM);
final String param = "MPSL" + "/" + nonPlatformID + "/" + classId;

final DataAccess da = new DataAccess(container, vertx);
da.getDataAPI(param, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            container.logger().debug(LogConstants.CODE + code);

            if (th != null) {
                replyFail(message, th, code);
                return;
            }

            switch (code) {
                case HttpConstants.HTTP_CODE_SUCCESS_200:
                    container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());

                    JsonArray ja = responseData.getObject(JsonKeyConstants.BODY)
                        .getArray(JsonKeyConstants.DATA);

                    List<SLkeyInfo> list = new ArrayList<SLkeyInfo>();
                    for (int i = 0; i < ja.size(); i++) {
                        JsonObject jo = ja.get(i);
                        if (jo.containsField("MPSLP")) {
                            JsonObject p = jo.getObject("MPSLP");
                            Iterator<String> ite = p.getFieldNames().iterator();
                            while (ite.hasNext()) {
                                JsonObject du = p.getObject(ite.next());
                                Iterator<String> duIte = du.getFieldNames().iterator();
                                while (duIte.hasNext()) {
                                    String value = duIte.next();
                                    JsonObject classValue = du.getObject(value);

                                    list.add(new SLkeyInfo(
                                        Integer.parseInt(classValue.getString("MPSLP03")),
                                        classValue.getString("MPSLP01"),
                                        value));
                                }
                            }
                        }
                    }
                    // ... process list
                    break;
            }
        } catch (Throwable e) {
            replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
        }
    }
});
```

---

## Common Patterns

### Pattern 1: Convert to Dropdown Options

```java
da.getSLkey(classId, new CallBackSLkey() {
    @Override
    public void callBack(int code, TreeMap<String, String> map, Throwable th) {
        if (code == 200) {
            JsonArray options = new JsonArray();
            
            for (Map.Entry<String, String> entry : map.entrySet()) {
                JsonObject option = new JsonObject();
                option.putString("value", entry.getKey());
                option.putString("label", entry.getValue());
                options.add(option);
            }
            
            JsonObject result = new JsonObject();
            result.putArray("options", options);
            message.reply(result);
        }
    }
});
```

### Pattern 2: Filter by Prefix

```java
da.getSLkey(classId, new CallBackSLkey() {
    @Override
    public void callBack(int code, TreeMap<String, String> map, Throwable th) {
        if (code == 200) {
            JsonArray filtered = new JsonArray();
            
            for (Map.Entry<String, String> entry : map.entrySet()) {
                // Only include codes starting with "A"
                if (entry.getKey().startsWith("A")) {
                    JsonObject item = new JsonObject();
                    item.putString("code", entry.getKey());
                    item.putString("name", entry.getValue());
                    filtered.add(item);
                }
            }
            
            message.reply(new JsonObject().putArray("data", filtered));
        }
    }
});
```

### Pattern 3: Add Default Option

```java
da.getSLkey(classId, new CallBackSLkey() {
    @Override
    public void callBack(int code, TreeMap<String, String> map, Throwable th) {
        if (code == 200) {
            JsonArray options = new JsonArray();
            
            // Add default "Please select" option
            JsonObject defaultOption = new JsonObject();
            defaultOption.putString("code", "");
            defaultOption.putString("name", "-- Please select --");
            options.add(defaultOption);
            
            // Add actual options
            for (Map.Entry<String, String> entry : map.entrySet()) {
                JsonObject option = new JsonObject();
                option.putString("code", entry.getKey());
                option.putString("name", entry.getValue());
                options.add(option);
            }
            
            message.reply(new JsonObject().putArray("options", options));
        }
    }
});
```

### Pattern 4: Cache SLkey Data

```java
// Class-level cache
private static Map<String, TreeMap<String, String>> slkeyCache = new HashMap<>();

public void getCachedSLkey(String classId, final Message<JsonObject> message) {
    // Check cache first
    if (slkeyCache.containsKey(classId)) {
        TreeMap<String, String> cached = slkeyCache.get(classId);
        
        JsonArray result = new JsonArray();
        for (Map.Entry<String, String> entry : cached.entrySet()) {
            JsonObject item = new JsonObject();
            item.putString("code", entry.getKey());
            item.putString("name", entry.getValue());
            result.add(item);
        }
        
        message.reply(new JsonObject().putArray("data", result));
        return;
    }
    
    // Fetch from API
    final DataAccess da = new DataAccess(container, vertx);
    da.getSLkey(classId, new CallBackSLkey() {
        @Override
        public void callBack(int code, TreeMap<String, String> map, Throwable th) {
            if (code == 200) {
                // Store in cache
                slkeyCache.put(classId, map);
                
                // Return result
                JsonArray result = new JsonArray();
                for (Map.Entry<String, String> entry : map.entrySet()) {
                    JsonObject item = new JsonObject();
                    item.putString("code", entry.getKey());
                    item.putString("name", entry.getValue());
                    result.add(item);
                }
                
                message.reply(new JsonObject().putArray("data", result));
            }
        }
    });
}
```

---

## Common Class IDs

| Class ID | Description | Example Values |
|----------|-------------|----------------|
| `USER_TYPE` | User types | Admin, User, Guest |
| `STATUS` | Status codes | Active, Inactive, Pending |
| `GENDER` | Gender | Male, Female, Other |
| `COUNTRY` | Country codes | JP, US, CN |
| `LANGUAGE` | Language codes | ja, en, zh |

**Note**: Actual class IDs depend on your MPSL table configuration.

---

## Response Format

### CallBackSLkey Response (TreeMap)

```java
TreeMap<String, String> map = {
    "01" -> "Admin",
    "02" -> "User",
    "03" -> "Guest"
}
```

### Raw API Response (CallBackGet)

```json
{
  "code": 200,
  "body": {
    "data": [
      {
        "MPSLP": {
          "field1": {
            "01": {
              "MPSLP01": "Admin",
              "MPSLP03": "1"
            },
            "02": {
              "MPSLP01": "User",
              "MPSLP03": "2"
            }
          }
        }
      }
    ]
  }
}
```

---

## Checklist

Before writing SLkey code, verify:

- [ ] Used `da.getSLkey(classId, callback)` method
- [ ] Used `CallBackSLkey` for TreeMap response
- [ ] Used `CallBackGet` for raw response
- [ ] Checked `if (th != null)` FIRST
- [ ] Handled HTTP 200 status code
- [ ] Converted TreeMap to JsonArray if needed
- [ ] Added default option if required
- [ ] Considered caching for frequently used data
- [ ] Logged class ID: `container.logger().debug("ClassId: " + classId)`

---

**Related**: 
- GET templates: `01-get-templates.md`
- Error handling: `06-error-handling.md`
- Status codes: `07-status-codes.md`
