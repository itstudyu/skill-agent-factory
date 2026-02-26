# Data-API Quick Start Guide

**FOR AI**: Read this first, then refer to specific guides as needed.

## What is Data-API?

Data-API is a RESTful API service for CRUD operations in the P3 system. All calls go through the `DataAccess` class using Vert.x async callbacks.

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Main wrapper class
├── APIClientPool.java           # HTTP client pool
├── CallBack.java                # Generic callback
├── CallBackGet.java             # GET callback
├── CallBackPut.java             # PUT callback
└── CallBackDelete.java          # DELETE callback
```

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **ALWAYS check `th != null` BEFORE checking status code**
2. ⚠️ **ALWAYS wrap callback logic in try-catch**
3. ⚠️ **ALWAYS handle status codes: 200, 204, 404, 500, 900**
4. ⚠️ **NEVER perform blocking operations in callbacks**
5. ⚠️ **ALWAYS log method name, parameters, and response codes**

## Quick Decision Tree

```
Need to call Data-API?
│
├─ GET request?
│  ├─ Simple fetch → Read: 01-get-templates.md
│  └─ Master data → Read: 04-slkey-template.md
│
├─ PUT request?
│  └─ Create/Update → Read: 02-put-templates.md
│
├─ DELETE request?
│  └─ Delete → Read: 03-delete-templates.md
│
└─ Multiple calls?
   └─ Sequential → Read: 05-chaining-template.md
```

## Basic Pattern (All Methods)

```java
final DataAccess da = new DataAccess(container, vertx);

da.getDataAPI(param, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            // STEP 1: Check exception FIRST
            if (th != null) {
                replyFail(message, th, code);
                return;
            }
            
            // STEP 2: Handle status codes
            switch (code) {
                case 200: // Success
                case 204: // No content
                case 404: // Not found
                case 500: // Server error
                default:  // Unexpected
            }
        } catch (Throwable e) {
            replyFail(message, e, HttpConstants.HTTP_CODE_ERROR);
        }
    }
});
```

## Related Guides

- **GET requests**: `01-get-templates.md`
- **PUT requests**: `02-put-templates.md`
- **DELETE requests**: `03-delete-templates.md`
- **SLkey (master data)**: `04-slkey-template.md`
- **Chaining calls**: `05-chaining-template.md`
- **Error handling**: `06-error-handling.md`
- **Status codes**: `07-status-codes.md`
- **Real examples**: `08-real-examples.md`

---

**Start here, then navigate to specific guides as needed.**
