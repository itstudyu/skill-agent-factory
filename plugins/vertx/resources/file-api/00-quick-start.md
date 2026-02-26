# File-API Quick Start Guide

**FOR AI**: Read this first for File-API usage.

## What is File-API?

File-API is used for **file operations** including:
- File upload/download
- File ID generation (pre-allocation)
- File persistence (temp → permanent)
- File deletion (temp files only)
- File metadata retrieval

**Key Concept**: Get file ID first, upload file, then persist it.

---

## File Locations

```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Contains File-API methods
└── CallBackGet.java             # Callback for File-API responses
```

---

## 5 Critical Rules (NEVER VIOLATE)

1. ⚠️ **Always get file ID BEFORE uploading file**
2. ⚠️ **Use CallBackGet for most File-API operations**
3. ⚠️ **Persist file with putFileAPIPersist() to make it permanent**
4. ⚠️ **DELETE only works for temporary files (not persisted)**
5. ⚠️ **File paths use `/1.0/file` or `/1.0/fileid` endpoints**

---

## Basic Workflow

```
1. Get File ID (pre-allocate)
   ↓
2. Upload file (using file ID)
   ↓
3. Persist file (make permanent)
   ↓
4. Use file ID to retrieve/download
```

---

## Quick Method Reference

| Method | Purpose | Endpoint |
|--------|---------|----------|
| `getFileIdAPI()` | Get file ID (pre-allocate) | `/1.0/fileid` |
| `getFileAPI()` | Get file or metadata | `/1.0/file/{id}` |
| `putFileAPIPersist()` | Persist file (temp → permanent) | `/1.0/file/{id}` |
| `deleteFileAPI()` | Delete temp file | `/1.0/file/{id}` |

---

## Basic Pattern: Get File ID

```java
final DataAccess da = new DataAccess(container, vertx);

// Get file ID (no parameter = new ID)
da.getFileIdAPI("", new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            String fileId = responseData.getObject("body")
                .getObject("data")
                .getString("fileId");
            
            container.logger().info("File ID: " + fileId);
            message.reply(responseData);
        } catch (Exception e) {
            container.logger().error(methodName + LogConstants.ERROR, e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## Basic Pattern: Persist File

```java
final DataAccess da = new DataAccess(container, vertx);

String fileId = "file-12345-abcde";

// Persist file (make permanent)
da.putFileAPIPersist(fileId, new CallBackGet(BUS_NAME, container, message) {
    @Override
    public void ok(JsonObject responseData) {
        try {
            container.logger().info("File persisted: " + fileId);
            message.reply(responseData);
        } catch (Exception e) {
            container.logger().error(methodName + LogConstants.ERROR, e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## Basic Pattern: Delete Temp File

```java
final DataAccess da = new DataAccess(container, vertx);

String fileId = "temp-file-12345";

// Delete temporary file
da.deleteFileAPI(fileId, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (th != null) {
                container.logger().error("Delete failed", th);
                message.reply(JsonUtil.createReplyObjectFail(th));
                return;
            }
            
            if (code == 204) {
                container.logger().info("File deleted: " + fileId);
                message.reply(new JsonObject().putNumber("code", 204));
            } else {
                message.reply(responseData);
            }
        } catch (Exception e) {
            container.logger().error(methodName + LogConstants.ERROR, e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## File Lifecycle

```
┌─────────────────┐
│ Get File ID     │ ← getFileIdAPI()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Upload File     │ ← (External upload to file ID)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Temporary File  │ ← Can be deleted with deleteFileAPI()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Persist File    │ ← putFileAPIPersist()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Permanent File  │ ← Cannot be deleted
└─────────────────┘
```

---

## When to Use File-API

✅ **Use File-API when:**
- Uploading files (images, PDFs, Excel, etc.)
- Downloading files
- Managing file metadata
- Need to pre-allocate file IDs
- Need to make temp files permanent

❌ **Don't use File-API for:**
- Text data → Use Data-API
- Small JSON data → Use Data-API
- Database records → Use Data-API

---

## Related Guide

- **Complete Template**: `01-file-api-template.md`

---

**Start here, then read the complete template for detailed examples.**
