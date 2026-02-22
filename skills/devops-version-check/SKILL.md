---
name: devops-version-check
description: Language version and dependency safety check. Verifies code uses correct syntax for the project's language version, APIs are not deprecated, and dependencies are stable/secure versions.
allowed-tools: Read, Glob, Bash, Grep
---

# Version & Compatibility Check (Step 6 of Pipeline)

プロジェクトの言語バージョンと依存関係の安全性を確認する。

---

## Step 1 — Detect Project Runtime

Read the following files to determine versions:

| File | What to read |
|------|-------------|
| `package.json` | `engines.node`, `dependencies`, `devDependencies` |
| `.nvmrc` / `.node-version` | Node.js version |
| `pyproject.toml` / `setup.py` | Python version |
| `Gemfile` | Ruby version |
| `go.mod` | Go version |
| `pom.xml` / `build.gradle` | Java version |
| `.tool-versions` | asdf version manager |
| `Dockerfile` | Base image version |
| `docker-compose.yml` | Service image versions |

---

## Step 2 — Syntax Compatibility

Check that newly written code uses syntax compatible with the detected version:

### JavaScript / TypeScript
- Node < 18: No `fetch` native (need `node-fetch`)
- Node < 16: No top-level `await`
- Node < 14.17: No `??=`, `||=` operators
- Check `tsconfig.json` `target` and `lib` — don't use features above the target

### Python
- Python < 3.10: No `match` statement
- Python < 3.9: No `list[str]` type hints (use `List[str]` from typing)
- Python < 3.8: No walrus operator `:=`

### Other Languages
Apply equivalent version-gate rules for the detected runtime.

---

## Step 3 — Deprecated API Check

Flag usage of known deprecated APIs:
- `moment.js` → Suggest `date-fns` or native `Intl`
- `request` npm package (deprecated) → Suggest `axios` or `fetch`
- `React.createClass` → Suggest functional components
- `componentWillMount` → Suggest `useEffect`

---

## Step 4 — Security Stability

For each **newly added** dependency, verify:
- [ ] Package is actively maintained (not archived on GitHub)
- [ ] Version is not flagged as insecure
- [ ] Use `^` or `~` pinning appropriately (not `*`)
- [ ] Prefer LTS versions for major packages

---

## Output Format

```
## 📦 Version Check

**Detected:** Node 20.x / TypeScript 5.3 / React 18

### ✅ Passed
- Syntax compatible with Node 20
- No deprecated APIs used

### ⚠️ Issues

| Type | Issue | Fix |
|------|-------|-----|
| Deprecated | `moment(date).format()` | Replace with `date-fns format()` |
| Version | `fetch` used but engines requires Node 16 | Add polyfill or upgrade engines |
```
