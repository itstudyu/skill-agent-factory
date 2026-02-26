# Data-API Documentation

This directory contains comprehensive documentation for using the Data-API in the P3 system.

## 📚 Documentation Structure

### Start Here
- **[00-quick-start.md](00-quick-start.md)** - Quick reference and decision tree

### Core Templates
- **[01-get-templates.md](01-get-templates.md)** - GET request templates
- **[02-put-templates.md](02-put-templates.md)** - PUT request templates
- **[03-delete-templates.md](03-delete-templates.md)** - DELETE request templates
- **[04-slkey-template.md](04-slkey-template.md)** - SLkey (master data) template
- **[05-chaining-template.md](05-chaining-template.md)** - Chaining multiple API calls

### Reference Guides
- **[06-error-handling.md](06-error-handling.md)** - Error handling patterns
- **[07-status-codes.md](07-status-codes.md)** - HTTP status codes reference

### Complete Guide
- **[data-api-usage-guide.md](../data-api-usage-guide.md)** - Full comprehensive guide (1600+ lines)

---

## 🚀 Quick Navigation

### For AI Code Generation

1. Read `00-quick-start.md` first
2. Follow the decision tree to find the right template
3. Use the template exactly as shown
4. Verify with the checklist

### For Developers

1. Start with `00-quick-start.md` for overview
2. Jump to specific template based on your need:
   - GET data → `01-get-templates.md`
   - Create/Update → `02-put-templates.md`
   - Delete → `03-delete-templates.md`
   - Master data → `04-slkey-template.md`
   - Multiple calls → `05-chaining-template.md`
3. Reference `06-error-handling.md` and `07-status-codes.md` as needed

---

## 📖 Document Sizes

| File | Lines | Purpose |
|------|-------|---------|
| `00-quick-start.md` | ~150 | Quick reference |
| `01-get-templates.md` | ~300 | GET patterns |
| `02-put-templates.md` | ~250 | PUT patterns |
| `03-delete-templates.md` | ~250 | DELETE patterns |
| `04-slkey-template.md` | ~250 | SLkey patterns |
| `05-chaining-template.md` | ~300 | Chaining patterns |
| `06-error-handling.md` | ~300 | Error handling |
| `07-status-codes.md` | ~250 | Status codes |

**Total**: ~2000 lines split into 8 focused documents

---

## 🎯 Use Cases

### "I need to fetch user data"
→ Read `01-get-templates.md` → Use Template 1 or 2

### "I need to create/update a record"
→ Read `02-put-templates.md` → Use Template 1 or 2

### "I need to delete a record"
→ Read `03-delete-templates.md` → Use Template 1 or 2

### "I need to get dropdown options"
→ Read `04-slkey-template.md` → Use SLkey template

### "I need to fetch related data"
→ Read `05-chaining-template.md` → Use chaining template

### "I'm getting errors"
→ Read `06-error-handling.md` and `07-status-codes.md`

---

## 🔑 5 Critical Rules

1. ⚠️ **ALWAYS check `th != null` BEFORE checking status code**
2. ⚠️ **ALWAYS wrap callback logic in try-catch**
3. ⚠️ **ALWAYS handle status codes: 200, 204, 404, 500, 900**
4. ⚠️ **NEVER perform blocking operations in callbacks**
5. ⚠️ **ALWAYS log method name, parameters, and response codes**

---

## 📁 Source Code Locations

All Data-API related code is in:
```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/
├── DataAccess.java              # Main wrapper class
├── APIClientPool.java           # HTTP client pool
├── CallBack.java                # Generic callback
├── CallBackGet.java             # GET callback
├── CallBackPut.java             # PUT callback
├── CallBackDelete.java          # DELETE callback
└── CallBackSLkey.java           # SLkey callback
```

Real-world examples:
```
src/main/java/jp/co/payroll/p3/submodules/CommonScreen/
├── formal/CustomFormal_H101_base.java        # GET example
└── filter/Common_CustomFilter_SLkey.java     # SLkey example
```

---

## 🤖 For AI Agents

When generating Data-API code:

1. **Always start with** `00-quick-start.md`
2. **Use templates exactly** - do not deviate
3. **Follow the decision tree** to select the right template
4. **Verify with checklist** before completing
5. **Reference source code** for implementation details

### Template Selection

```
GET request? → 01-get-templates.md
PUT request? → 02-put-templates.md
DELETE request? → 03-delete-templates.md
Master data? → 04-slkey-template.md
Multiple calls? → 05-chaining-template.md
```

---

## 📝 Document Maintenance

**Last Updated**: 2026-02-25  
**Version**: 2.0 (Split from monolithic guide)  
**Maintainer**: Development Team

### Version History

- **v2.0** (2026-02-25): Split into focused documents
- **v1.1** (2026-02-25): Added source code locations
- **v1.0** (2026-02-25): Initial comprehensive guide

---

## 🔗 Related Documentation

- **Original Guide**: `../data-api-usage-guide.md` (comprehensive 1600+ line document)
- **Constants**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/constants/`
- **Utilities**: `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/util/`

---

## 💡 Tips

- **New to Data-API?** Start with `00-quick-start.md`
- **Need a specific pattern?** Jump directly to the relevant template
- **Debugging errors?** Check `06-error-handling.md` and `07-status-codes.md`
- **Want complete reference?** Read `../data-api-usage-guide.md`

---

**Questions?** Contact the development team or refer to source code in `src/main/java/jp/co/payroll/p3/submodules/CommonScreen/api/`
