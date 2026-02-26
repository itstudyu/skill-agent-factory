# Schema-API Template

## Template: Get Table Schema

**Use this to retrieve table structure information.**

```java
public void getTableSchema(String tableName, final Message<JsonObject> message) {
    final String methodName = new Throwable().getStackTrace()[0].getMethodName();
    container.logger().info(BUS_NAME + LogConstants.START);
    
    try {
        final DataAccess da = new DataAccess(container, vertx);
        
        // Validate table name
        if (StringUtil.isNullOrEmpty(tableName)) {
            message.reply(new JsonObject()
                .putNumber("code", 400)
                .putString("message", "Table name is required"));
            return;
        }
        
        container.logger().debug("Getting schema for table: " + tableName);
        
        da.getSchemaAPI(tableName, new CallBack() {
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
                    switch (code) {
                        case 200:
                            container.logger().info(methodName + " - Schema found");
                            
                            JsonObject schema = responseData.getObject("body")
                                .getObject("data");
                            
                            // Extract schema information
                            String tableNameFromSchema = schema.getString("tableName");
                            JsonArray columns = schema.getArray("columns");
                            
                            container.logger().info("Table: " + tableNameFromSchema 
                                + ", Columns: " + columns.size());
                            
                            message.reply(schema);
                            break;
                            
                        case 204:
                            container.logger().warn(methodName + " - Schema not found: " + tableName);
                            message.reply(new JsonObject()
                                .putNumber("code", 404)
                                .putString("message", "Schema not found for table: " + tableName));
                            break;
                            
                        default:
                            container.logger().error(methodName + " - Unexpected code: " + code);
                            message.reply(responseData);
                            break;
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

## Common Patterns

### Pattern 1: Extract Column Information

```java
da.getSchemaAPI(tableName, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (th != null || code != 200) {
                message.reply(responseData);
                return;
            }
            
            JsonObject schema = responseData.getObject("body").getObject("data");
            JsonArray columns = schema.getArray("columns");
            
            // Extract column details
            JsonArray columnInfo = new JsonArray();
            for (int i = 0; i < columns.size(); i++) {
                JsonObject column = columns.get(i);
                
                JsonObject info = new JsonObject();
                info.putString("name", column.getString("name"));
                info.putString("type", column.getString("type"));
                info.putNumber("length", column.getInteger("length"));
                info.putBoolean("nullable", column.getBoolean("nullable"));
                info.putBoolean("primaryKey", column.getBoolean("primaryKey", false));
                
                columnInfo.add(info);
            }
            
            message.reply(new JsonObject()
                .putNumber("code", 200)
                .putString("tableName", schema.getString("tableName"))
                .putArray("columns", columnInfo));
                
        } catch (Exception e) {
            container.logger().error("Error", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

### Pattern 2: Generate Form Fields from Schema

```java
// Use schema to generate form field definitions
da.getSchemaAPI(tableName, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (code == 200) {
                JsonObject schema = responseData.getObject("body").getObject("data");
                JsonArray columns = schema.getArray("columns");
                
                // Generate form fields
                JsonArray formFields = new JsonArray();
                for (int i = 0; i < columns.size(); i++) {
                    JsonObject column = columns.get(i);
                    
                    JsonObject field = new JsonObject();
                    field.putString("name", column.getString("name"));
                    field.putBoolean("required", !column.getBoolean("nullable"));
                    
                    // Determine input type based on data type
                    String dataType = column.getString("type");
                    if ("VARCHAR".equals(dataType)) {
                        field.putString("type", "text");
                        field.putNumber("maxLength", column.getInteger("length"));
                    } else if ("INTEGER".equals(dataType)) {
                        field.putString("type", "number");
                    } else if ("DATE".equals(dataType)) {
                        field.putString("type", "date");
                    }
                    
                    formFields.add(field);
                }
                
                message.reply(new JsonObject()
                    .putNumber("code", 200)
                    .putArray("formFields", formFields));
            }
        } catch (Exception e) {
            container.logger().error("Error", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

### Pattern 3: Validate Data Against Schema

```java
// Validate input data against table schema
da.getSchemaAPI(tableName, new CallBack() {
    @Override
    public void callBack(int code, JsonObject responseData, Throwable th) {
        try {
            if (code == 200) {
                JsonObject schema = responseData.getObject("body").getObject("data");
                JsonArray columns = schema.getArray("columns");
                
                // Validate input data
                JsonArray errors = new JsonArray();
                
                for (int i = 0; i < columns.size(); i++) {
                    JsonObject column = columns.get(i);
                    String columnName = column.getString("name");
                    boolean nullable = column.getBoolean("nullable");
                    
                    // Check required fields
                    if (!nullable && !inputData.containsField(columnName)) {
                        errors.add(new JsonObject()
                            .putString("field", columnName)
                            .putString("error", "Required field missing"));
                    }
                    
                    // Check data type
                    if (inputData.containsField(columnName)) {
                        String type = column.getString("type");
                        Object value = inputData.getValue(columnName);
                        
                        if ("INTEGER".equals(type) && !(value instanceof Number)) {
                            errors.add(new JsonObject()
                                .putString("field", columnName)
                                .putString("error", "Must be a number"));
                        }
                        
                        // Check length for VARCHAR
                        if ("VARCHAR".equals(type) && value instanceof String) {
                            int maxLength = column.getInteger("length");
                            if (((String) value).length() > maxLength) {
                                errors.add(new JsonObject()
                                    .putString("field", columnName)
                                    .putString("error", "Exceeds max length: " + maxLength));
                            }
                        }
                    }
                }
                
                if (errors.size() > 0) {
                    message.reply(new JsonObject()
                        .putNumber("code", 400)
                        .putString("message", "Validation failed")
                        .putArray("errors", errors));
                } else {
                    message.reply(new JsonObject()
                        .putNumber("code", 200)
                        .putString("message", "Validation passed"));
                }
            }
        } catch (Exception e) {
            container.logger().error("Error", e);
            message.reply(new JsonObject().putNumber("code", 500));
        }
    }
});
```

---

## Common Use Cases

### Use Case 1: Dynamic Form Generation

Schema-API → Extract columns → Generate form fields

### Use Case 2: Data Validation

Schema-API → Get constraints → Validate input data

### Use Case 3: Query Builder

Schema-API → Get column types → Build type-safe queries

### Use Case 4: Documentation

Schema-API → Extract schema → Generate API documentation

---

## Checklist

Before writing Schema-API code, verify:

- [ ] Used `getSchemaAPI()` method
- [ ] Used generic `CallBack` (not specialized)
- [ ] Checked `if (th != null)` FIRST
- [ ] Handled HTTP 200 (schema found)
- [ ] Handled HTTP 204 (schema not found)
- [ ] Wrapped callback logic in try-catch
- [ ] Logged table name being queried
- [ ] Used schema for metadata only

---

**Related**: 
- Quick start: `00-quick-start.md`
- Complete template: `01-schema-api-template.md`
