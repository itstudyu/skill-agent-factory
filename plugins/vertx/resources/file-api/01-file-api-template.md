# File-API Template

## Template 1: Get File ID (Pre-allocate)

**Use this to get a new file ID before uploading.**

```java
public void getNewFileId(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Get new file ID (empty parameter)
        da.getFileIdAPI("", new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                    
                    // Extract file ID
                    String fileId = responseData.getObject("body")
                        .getObject("data")
                        .getString("fileId");
                    
                    container.logger().info("Generated File ID: " + fileId);
                    
                    // Return file ID to client
                    JsonObject result = new JsonObject();
                    result.putNumber("code", 200);
                    result.putString("fileId", fileId);
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

## Template 2: Get Multiple File IDs

**Use this to get multiple file IDs at once.**

```java
public void getMultipleFileIds(int count, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Get multiple file IDs
        // Parameter: number of IDs to generate
        da.getFileIdAPI(String.valueOf(count), new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                    
                    // Extract file IDs array
                    JsonArray fileIds = responseData.getObject("body")
                        .getObject("data")
                        .getArray("fileIds");
                    
                    container.logger().info("Generated " + fileIds.size() + " File IDs");
                    
                    // Return file IDs to client
                    JsonObject result = new JsonObject();
                    result.putNumber("code", 200);
                    result.putArray("fileIds", fileIds);
                    message.reply(result);
                    
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

## Template 3: Get File Metadata

**Use this to get file information without downloading.**

```java
public void getFileMetadata(String fileId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Get file metadata
        da.getFileAPI(fileId, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    if (code == 200) {
                        JsonObject fileInfo = responseData.getObject("body")
                            .getObject("data");
                        
                        String fileName = fileInfo.getString("fileName");
                        String fileSize = fileInfo.getString("fileSize");
                        String contentType = fileInfo.getString("contentType");
                        
                        container.logger().info("File: " + fileName + ", Size: " + fileSize);
                        
                        message.reply(fileInfo);
                    } else if (code == 404) {
                        container.logger().warn(methodName + " - File not found: " + fileId);
                        message.reply(new JsonObject()
                            .putNumber("code", 404)
                            .putString("message", "File not found"));
                    } else {
                        message.reply(responseData);
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

## Template 4: Persist File (Make Permanent)

**Use this to convert temporary file to permanent.**

```java
public void persistFile(String fileId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        container.logger().info("Persisting file: " + fileId);
        
        // Persist file
        da.putFileAPIPersist(fileId, new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().info("File persisted successfully: " + fileId);
                    container.logger().debug(methodName + LogConstants.RETURN + responseData.toString());
                    
                    JsonObject result = new JsonObject();
                    result.putNumber("code", 200);
                    result.putString("message", "File persisted successfully");
                    result.putString("fileId", fileId);
                    message.reply(result);
                    
                } catch (Exception e) {
                    container.logger().error(methodName + LogConstants.ERROR, e);
                    message.reply(new JsonObject().putNumber("code", 500));
                }
            }
            
            @Override
            public void fail(int code, JsonObject responseData) {
                container.logger().error(methodName + " - Persist failed: " + code);
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

## Template 5: Delete Temporary File

**Use this to delete a temporary (non-persisted) file.**

```java
public void deleteTempFile(String fileId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        container.logger().info("Deleting temporary file: " + fileId);
        
        // Delete file (only works for temp files)
        da.deleteFileAPI(fileId, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    if (code == 204) {
                        container.logger().info("File deleted successfully: " + fileId);
                        
                        JsonObject result = new JsonObject();
                        result.putNumber("code", 204);
                        result.putString("message", "File deleted successfully");
                        message.reply(result);
                        
                    } else if (code == 404) {
                        container.logger().warn(methodName + " - File not found: " + fileId);
                        message.reply(new JsonObject()
                            .putNumber("code", 404)
                            .putString("message", "File not found"));
                            
                    } else if (code == 400) {
                        container.logger().warn(methodName + " - Cannot delete persisted file: " + fileId);
                        message.reply(new JsonObject()
                            .putNumber("code", 400)
                            .putString("message", "Cannot delete persisted file"));
                            
                    } else {
                        message.reply(responseData);
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

## Complete Workflow Example

**Complete file upload workflow from ID generation to persistence.**

```java
public void uploadFileWorkflow(final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Step 1: Get file ID
        da.getFileIdAPI("", new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    final String fileId = responseData.getObject("body")
                        .getObject("data")
                        .getString("fileId");
                    
                    container.logger().info("Step 1: File ID generated: " + fileId);
                    
                    // Step 2: Return file ID to client for upload
                    // Client uploads file using this file ID
                    JsonObject uploadInfo = new JsonObject();
                    uploadInfo.putString("fileId", fileId);
                    uploadInfo.putString("uploadUrl", "/upload/" + fileId);
                    uploadInfo.putString("nextStep", "Upload file, then call persistFile()");
                    
                    message.reply(uploadInfo);
                    
                    // Note: Client uploads file here (outside this code)
                    // Then client calls persistFile() to make it permanent
                    
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

// After client uploads file, they call this:
public void completeUpload(String fileId, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Step 3: Persist uploaded file
        da.putFileAPIPersist(fileId, new CallBackGet(BUS_NAME, container, message) {
            @Override
            public void ok(JsonObject responseData) {
                try {
                    container.logger().info("Step 3: File persisted: " + fileId);
                    
                    JsonObject result = new JsonObject();
                    result.putNumber("code", 200);
                    result.putString("message", "Upload complete");
                    result.putString("fileId", fileId);
                    message.reply(result);
                    
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

## Common Patterns

### Pattern 1: Batch File ID Generation

```java
// Generate multiple file IDs for batch upload
public void prepareBatchUpload(int fileCount, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    
    da.getFileIdAPI(String.valueOf(fileCount), new CallBackGet(BUS_NAME, container, message) {
        @Override
        public void ok(JsonObject responseData) {
            try {
                JsonArray fileIds = responseData.getObject("body")
                    .getObject("data")
                    .getArray("fileIds");
                
                container.logger().info("Generated " + fileIds.size() + " file IDs for batch upload");
                
                message.reply(new JsonObject()
                    .putNumber("code", 200)
                    .putArray("fileIds", fileIds));
                    
            } catch (Exception e) {
                container.logger().error("Error", e);
                message.reply(new JsonObject().putNumber("code", 500));
            }
        }
    });
}
```

### Pattern 2: Conditional Persistence

```java
// Persist file only if validation passes
public void validateAndPersist(String fileId, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    
    // First, get file metadata to validate
    da.getFileAPI(fileId, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == 200) {
                    JsonObject fileInfo = responseData.getObject("body").getObject("data");
                    
                    // Validate file
                    long fileSize = fileInfo.getLong("fileSize");
                    String contentType = fileInfo.getString("contentType");
                    
                    if (fileSize > 10_000_000) {
                        message.reply(new JsonObject()
                            .putNumber("code", 400)
                            .putString("message", "File too large (max 10MB)"));
                        return;
                    }
                    
                    if (!contentType.startsWith("image/")) {
                        message.reply(new JsonObject()
                            .putNumber("code", 400)
                            .putString("message", "Only images allowed"));
                        return;
                    }
                    
                    // Validation passed - persist file
                    da.putFileAPIPersist(fileId, new CallBackGet(BUS_NAME, container, message));
                } else {
                    message.reply(responseData);
                }
            } catch (Exception e) {
                container.logger().error("Error", e);
                message.reply(new JsonObject().putNumber("code", 500));
            }
        }
    });
}
```

### Pattern 3: Cleanup Temp Files

```java
// Delete temporary files that were never persisted
public void cleanupTempFiles(List<String> tempFileIds, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    final AtomicInteger counter = new AtomicInteger(tempFileIds.size());
    final JsonArray deletedFiles = new JsonArray();
    
    for (String fileId : tempFileIds) {
        da.deleteFileAPI(fileId, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                if (code == 204) {
                    synchronized (deletedFiles) {
                        deletedFiles.add(fileId);
                    }
                    container.logger().info("Deleted temp file: " + fileId);
                }
                
                if (counter.decrementAndGet() == 0) {
                    // All deletions completed
                    message.reply(new JsonObject()
                        .putNumber("code", 200)
                        .putArray("deletedFiles", deletedFiles)
                        .putNumber("deletedCount", deletedFiles.size()));
                }
            }
        });
    }
}
```

### Pattern 4: File Download URL Generation

```java
// Generate download URL for persisted file
public void getDownloadUrl(String fileId, final Message<JsonObject> message) {
    final DataAccess da = new DataAccess(container, vertx);
    
    // Get file metadata
    da.getFileAPI(fileId, new CallBack() {
        @Override
        public void callBack(int code, JsonObject responseData, Throwable th) {
            try {
                if (code == 200) {
                    JsonObject fileInfo = responseData.getObject("body").getObject("data");
                    
                    String fileName = fileInfo.getString("fileName");
                    boolean isPersisted = fileInfo.getBoolean("persisted", false);
                    
                    if (!isPersisted) {
                        message.reply(new JsonObject()
                            .putNumber("code", 400)
                            .putString("message", "File not persisted yet"));
                        return;
                    }
                    
                    // Generate download URL
                    String downloadUrl = "/api/file/download/" + fileId;
                    
                    JsonObject result = new JsonObject();
                    result.putNumber("code", 200);
                    result.putString("fileId", fileId);
                    result.putString("fileName", fileName);
                    result.putString("downloadUrl", downloadUrl);
                    message.reply(result);
                    
                } else {
                    message.reply(responseData);
                }
            } catch (Exception e) {
                container.logger().error("Error", e);
                message.reply(new JsonObject().putNumber("code", 500));
            }
        }
    });
}
```

---

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | File metadata retrieved successfully |
| 204 | No Content | File deleted successfully |
| 400 | Bad Request | Cannot delete persisted file |
| 404 | Not Found | File does not exist |
| 500 | Server Error | Internal error |

---

## Response Formats

### Get File ID Response

```json
{
  "code": 200,
  "body": {
    "data": {
      "fileId": "file-12345-abcde"
    }
  }
}
```

### Get Multiple File IDs Response

```json
{
  "code": 200,
  "body": {
    "data": {
      "fileIds": [
        "file-12345-abcde",
        "file-67890-fghij",
        "file-11111-klmno"
      ]
    }
  }
}
```

### Get File Metadata Response

```json
{
  "code": 200,
  "body": {
    "data": {
      "fileId": "file-12345-abcde",
      "fileName": "document.pdf",
      "fileSize": 1048576,
      "contentType": "application/pdf",
      "persisted": true,
      "uploadDate": "2026-02-25T10:30:00Z"
    }
  }
}
```

---

## Checklist

Before writing File-API code, verify:

- [ ] Used `getFileIdAPI()` to pre-allocate file ID
- [ ] Used `CallBackGet` for GET operations
- [ ] Used generic `CallBack` for DELETE operations
- [ ] Called `putFileAPIPersist()` to make file permanent
- [ ] Handled HTTP 200, 204, 404 status codes
- [ ] Wrapped callback logic in try-catch
- [ ] Logged file operations (ID, persist, delete)
- [ ] Validated file before persisting (size, type)
- [ ] Understood that DELETE only works for temp files
- [ ] Extracted file ID from response correctly

---

## Common Mistakes

### ❌ Mistake 1: Not Pre-allocating File ID

```java
// WRONG: Uploading without file ID
// Client uploads file directly without getting ID first
```

### ✅ Fix: Get File ID First

```java
// CORRECT: Get file ID before upload
da.getFileIdAPI("", callback);
// Then client uploads using this file ID
```

### ❌ Mistake 2: Forgetting to Persist

```java
// WRONG: File uploaded but never persisted
// File will be deleted automatically after some time
```

### ✅ Fix: Always Persist

```java
// CORRECT: Persist after upload
da.putFileAPIPersist(fileId, callback);
```

### ❌ Mistake 3: Trying to Delete Persisted File

```java
// WRONG: Trying to delete permanent file
da.deleteFileAPI(persistedFileId, callback);
// Returns 400 error
```

### ✅ Fix: Only Delete Temp Files

```java
// CORRECT: Only delete temporary (non-persisted) files
da.deleteFileAPI(tempFileId, callback);
```

---

## File-API Summary

| Operation | Method | Parameter | Purpose |
|-----------|--------|-----------|---------|
| Get single ID | `getFileIdAPI("")` | Empty string | Generate 1 file ID |
| Get multiple IDs | `getFileIdAPI("5")` | Count as string | Generate N file IDs |
| Get metadata | `getFileAPI(fileId)` | File ID | Get file info |
| Persist file | `putFileAPIPersist(fileId)` | File ID | Make permanent |
| Delete temp file | `deleteFileAPI(fileId)` | File ID | Delete temp file |

---

**Related**: 
- Quick start: `00-quick-start.md`
- Data-API: `../data-api/01-get-templates.md`
- Async-API: `../async-api/01-async-api-template.md`
