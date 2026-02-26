# Insert-API Template

**⚠️ WARNING**: No actual usage examples found in the codebase. This template is based on common API patterns and naming conventions.

---

## Template 1: Bulk Insert (Hypothetical)

**Use this pattern for bulk data insertion.**

```java
public void bulkInsert(List<DataRecord> records, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate input
        if (records == null || records.isEmpty()) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Records list is empty"));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build records array
        JsonArray recordsArray = new JsonArray();
        for (DataRecord record : records) {
            JsonObject recordObj = new JsonObject();
            recordObj.putString("field1", record.field1);
            recordObj.putString("field2", record.field2);
            recordObj.putString("field3", record.field3);
            // Add more fields as needed
            recordsArray.add(recordObj);
        }
        
        // Build request body
        JsonObject requestBody = new JsonObject();
        requestBody.putArray("records", recordsArray);
        requestBody.putString("tableName", "TARGET_TABLE");
        
        container.logger().info("Bulk inserting " + records.size() + " records");
        
        // Call Insert-API (method name may vary - check DataAccess.java)
        da.postInsertAPI("bulk", requestBody, new CallBack() {
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
                    
                    // STEP 2: Handle status codes
                    if (code == 201 || code == 200) {
                        container.logger().info(methodName + " - Bulk insert successful");
                        
                        // Extract inserted count if available
                        int insertedCount = records.size();
                        if (responseData.containsField("body")) {
                            JsonObject body = responseData.getObject("body");
                            if (body.containsField("insertedCount")) {
                                insertedCount = body.getInteger("insertedCount");
                            }
                        }
                        
                        message.reply(new JsonObject()
                            .putNumber("code", 200)
                            .putNumber("insertedCount", insertedCount));
                    } else {
                        container.logger().error(methodName + " - Insert failed: " + code);
                        message.reply(new JsonObject()
                            .putNumber("code", code)
                            .putString("message", "Bulk insert failed"));
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

## Template 2: Batch Insert with Validation (Hypothetical)

**Use this to validate data before bulk insertion.**

```java
public void batchInsertWithValidation(List<DataRecord> records, 
        final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        // Validate input
        if (records == null || records.isEmpty()) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Records list is empty"));
            return;
        }
        
        // Validate each record
        JsonArray errors = new JsonArray();
        for (int i = 0; i < records.size(); i++) {
            DataRecord record = records.get(i);
            
            // Validate required fields
            if (StringUtil.isNullOrEmpty(record.field1)) {
                errors.add(new JsonObject()
                    .putNumber("index", i)
                    .putString("field", "field1")
                    .putString("error", "Required field missing"));
            }
            
            // Add more validation as needed
        }
        
        // Return validation errors if any
        if (errors.size() > 0) {
            container.logger().warn("Validation failed: " + errors.size() + " errors");
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Validation failed")
                .putArray("errors", errors));
            return;
        }
        
        final DataAccess da = new DataAccess(container, vertx);
        
        // Build records array
        JsonArray recordsArray = new JsonArray();
        for (DataRecord record : records) {
            JsonObject recordObj = new JsonObject();
            recordObj.putString("field1", record.field1);
            recordObj.putString("field2", record.field2);
            recordsArray.add(recordObj);
        }
        
        JsonObject requestBody = new JsonObject();
        requestBody.putArray("records", recordsArray);
        
        container.logger().info("Inserting " + records.size() + " validated records");
        
        // Call Insert-API
        da.postInsertAPI("batch", requestBody, new CallBack() {
            @Override
            public void callBack(int code, JsonObject responseData, Throwable th) {
                try {
                    if (th != null) {
                        container.logger().error(methodName + " - Error", th);
                        message.reply(JsonUtil.createReplyObjectFail(th));
                        return;
                    }
                    
                    if (code == 201 || code == 200) {
                        container.logger().info(methodName + " - Batch insert successful");
                        message.reply(new JsonObject()
                            .putNumber("code", 200)
                            .putNumber("insertedCount", records.size()));
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

## Template 3: Chunked Insert (Hypothetical)

**Use this to insert large datasets in chunks.**

```java
public void chunkedInsert(List<DataRecord> allRecords, 
        final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        if (allRecords == null || allRecords.isEmpty()) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Records list is empty"));
            return;
        }
        
        final int CHUNK_SIZE = 100;  // Insert 100 records at a time
        final int totalRecords = allRecords.size();
        final int totalChunks = (int) Math.ceil((double) totalRecords / CHUNK_SIZE);
        
        final AtomicInteger completedChunks = new AtomicInteger(0);
        final AtomicInteger totalInserted = new AtomicInteger(0);
        final AtomicBoolean hasError = new AtomicBoolean(false);
        
        container.logger().info("Inserting " + totalRecords + " records in " 
            + totalChunks + " chunks");
        
        // Process each chunk
        for (int chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
            final int startIndex = chunkIndex * CHUNK_SIZE;
            final int endIndex = Math.min(startIndex + CHUNK_SIZE, totalRecords);
            final List<DataRecord> chunk = allRecords.subList(startIndex, endIndex);
            final int currentChunk = chunkIndex + 1;
            
            // Build chunk data
            JsonArray recordsArray = new JsonArray();
            for (DataRecord record : chunk) {
                JsonObject recordObj = new JsonObject();
                recordObj.putString("field1", record.field1);
                recordObj.putString("field2", record.field2);
                recordsArray.add(recordObj);
            }
            
            JsonObject requestBody = new JsonObject();
            requestBody.putArray("records", recordsArray);
            
            final DataAccess da = new DataAccess(container, vertx);
            
            // Insert chunk
            da.postInsertAPI("chunk", requestBody, new CallBack() {
                @Override
                public void callBack(int code, JsonObject responseData, Throwable th) {
                    try {
                        if (th != null || (code != 200 && code != 201)) {
                            if (!hasError.get()) {
                                hasError.set(true);
                                container.logger().error("Chunk " + currentChunk 
                                    + " failed: " + (th != null ? th.getMessage() : "code=" + code));
                                message.reply(new JsonObject()
                                    .putNumber("code", 500)
                                    .putString("message", "Chunk insert failed at chunk " + currentChunk));
                            }
                            return;
                        }
                        
                        // Update counters
                        totalInserted.addAndGet(chunk.size());
                        int completed = completedChunks.incrementAndGet();
                        
                        container.logger().info("Chunk " + currentChunk + "/" + totalChunks 
                            + " completed (" + totalInserted.get() + "/" + totalRecords + " records)");
                        
                        // All chunks completed
                        if (completed == totalChunks && !hasError.get()) {
                            container.logger().info("All chunks completed successfully");
                            message.reply(new JsonObject()
                                .putNumber("code", 200)
                                .putNumber("insertedCount", totalInserted.get())
                                .putNumber("totalChunks", totalChunks));
                        }
                        
                    } catch (Exception e) {
                        container.logger().error(methodName + LogConstants.ERROR, e);
                        if (!hasError.get()) {
                            hasError.set(true);
                            message.reply(new JsonObject().putNumber("code", 500));
                        }
                    }
                }
            });
        }
        
    } catch (Throwable th) {
        container.logger().error(methodName + LogConstants.ERROR, th);
        message.reply(JsonUtil.createReplyObjectFail(th));
    }
}
```

---

## Common Patterns (Hypothetical)

### Pattern 1: Simple Bulk Insert

```java
// Insert multiple records at once
JsonArray records = new JsonArray();
for (DataItem item : dataList) {
    records.add(new JsonObject()
        .putString("field1", item.field1)
        .putString("field2", item.field2));
}

JsonObject body = new JsonObject().putArray("records", records);
da.postInsertAPI("bulk", body, callback);
```

### Pattern 2: Insert with Transaction

```java
// Insert with transaction control
JsonObject body = new JsonObject();
body.putArray("records", recordsArray);
body.putBoolean("transaction", true);  // Use transaction
body.putBoolean("rollbackOnError", true);  // Rollback if any error

da.postInsertAPI("transactional", body, callback);
```

### Pattern 3: Insert with Duplicate Handling

```java
// Handle duplicates
JsonObject body = new JsonObject();
body.putArray("records", recordsArray);
body.putString("onDuplicate", "skip");  // or "update", "error"

da.postInsertAPI("bulk", body, callback);
```

---

## HTTP Status Codes (Expected)

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Records inserted successfully |
| 201 | Created | Records created successfully |
| 400 | Bad Request | Invalid data or validation error |
| 409 | Conflict | Duplicate key or constraint violation |
| 500 | Server Error | Internal error |

---

## Request Body Structure (Hypothetical)

```json
{
  "tableName": "TARGET_TABLE",
  "records": [
    {
      "field1": "value1",
      "field2": "value2",
      "field3": "value3"
    },
    {
      "field1": "value4",
      "field2": "value5",
      "field3": "value6"
    }
  ],
  "options": {
    "transaction": true,
    "onDuplicate": "skip"
  }
}
```

---

## Response Format (Expected)

```json
{
  "code": 201,
  "body": {
    "insertedCount": 100,
    "failedCount": 0,
    "duplicateCount": 5
  }
}
```

---

## Checklist

Before writing Insert-API code, verify:

- [ ] **Confirmed actual method name in DataAccess.java**
- [ ] **Checked endpoint format and parameters**
- [ ] **Validated all data before insertion**
- [ ] Used generic `CallBack`
- [ ] Checked `if (th != null)` FIRST
- [ ] Handled success codes (200/201)
- [ ] Handled error codes (400/409/500)
- [ ] Wrapped callback logic in try-catch
- [ ] Logged insertion details
- [ ] Considered chunking for large datasets
- [ ] Tested with small dataset first

---

## Common Mistakes

### ❌ Mistake 1: Inserting Without Validation

```java
// WRONG: No validation
da.postInsertAPI("bulk", body, callback);
```

### ✅ Fix: Validate First

```java
// CORRECT: Validate before insert
if (records.isEmpty()) {
    message.reply(new JsonObject()
        .putNumber("code", 400)
        .putString("message", "No records to insert"));
    return;
}

// Validate each record
for (DataRecord record : records) {
    if (StringUtil.isNullOrEmpty(record.requiredField)) {
        message.reply(new JsonObject()
            .putNumber("code", 400)
            .putString("message", "Required field missing"));
        return;
    }
}

da.postInsertAPI("bulk", body, callback);
```

### ❌ Mistake 2: Not Chunking Large Datasets

```java
// WRONG: Inserting 10,000 records at once
da.postInsertAPI("bulk", allRecords, callback);
```

### ✅ Fix: Use Chunking

```java
// CORRECT: Insert in chunks of 100
final int CHUNK_SIZE = 100;
for (int i = 0; i < totalRecords; i += CHUNK_SIZE) {
    List<DataRecord> chunk = records.subList(i, Math.min(i + CHUNK_SIZE, totalRecords));
    // Insert chunk
}
```

---

## Important Notes

⚠️ **CRITICAL**: This documentation is hypothetical. Before using Insert-API:

1. **Check DataAccess.java** for actual method signatures:
   ```java
   // Look for methods like:
   public void postInsertAPI(String param, JsonObject body, CallBack callback)
   public void getInsertAPI(String param, CallBack callback)
   ```

2. **Verify API endpoint format** in your API documentation

3. **Test with small dataset** (1-10 records) first

4. **Check response structure** to understand actual response format

5. **Consult API documentation** for specific requirements

---

**Related**: 
- Quick start: `00-quick-start.md`
- Data-API PUT: For single record creation
- Async-API: For long-running bulk operations

---

**⚠️ REMINDER**: No actual usage examples found in the codebase. This is a hypothetical guide based on common patterns. Always verify actual implementation before use.
