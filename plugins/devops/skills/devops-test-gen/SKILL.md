---
name: devops-test-gen
description: Automatically generate unit tests for newly written code. Run after code review is clean. Generates tests appropriate for the detected framework (Jest, Pytest, Go test, etc.).
tags: [devops, test, generate, unit-test, coverage]
allowed-tools: Read, Write, Glob, Bash
---

# Test Generation (Step 8 of Pipeline)

新しく作成したコードのユニットテストを自動生成する。

---

## Step 1 — Detect Test Framework

| Project Type | Check File | Framework |
|-------------|------------|-----------|
| Node/TypeScript | `package.json` → jest, vitest, mocha | Jest / Vitest |
| Python | `pyproject.toml`, `pytest.ini` | Pytest |
| Go | `*_test.go` exists | Go test |
| Ruby | `Gemfile` → rspec | RSpec |

If no test framework detected → Ask user: "テストフレームワークはどれを使いますか？"

---

## Step 2 — Identify What Needs Tests

Read the newly written files. Identify:
- Public functions and methods
- API endpoint handlers
- Business logic / utility functions
- Data transformation functions

**Skip:** Simple getters/setters, one-liner wrappers, generated code.

---

## Step 3 — Generate Tests

### Coverage Priority
1. **Happy path** — normal expected inputs → expected outputs
2. **Edge cases** — null, empty, 0, very large numbers, special chars
3. **Error cases** — invalid input, missing required fields, external service failures

### File Placement Convention
Follow the project's existing convention:
- `__tests__/` folder next to the source file
- `*.test.ts` / `*.spec.ts` alongside the file
- `tests/` directory at project root

If no convention found → create `__tests__/` next to the source file.

---

## Test Template — TypeScript/Jest

```typescript
// テスト対象: {functionName}
// ファイル: {sourceFile}

import { {functionName} } from '../{sourceFile}';

describe('{functionName}', () => {
  // 正常系
  it('正しい入力で期待する結果を返すこと', () => {
    // arrange
    const input = {...};
    const expected = {...};

    // act
    const result = {functionName}(input);

    // assert
    expect(result).toEqual(expected);
  });

  // 異常系
  it('nullが渡された場合にエラーをスローすること', () => {
    expect(() => {functionName}(null)).toThrow();
  });

  // エッジケース
  it('空の配列が渡された場合に空の結果を返すこと', () => {
    expect({functionName}([])).toEqual([]);
  });
});
```

---

## Test Template — Python/Pytest

```python
# テスト対象: {function_name}
import pytest
from {module} import {function_name}

class Test{FunctionName}:
    # 正常系
    def test_正しい入力で期待する結果を返す(self):
        result = {function_name}(valid_input)
        assert result == expected_output

    # 異常系
    def test_Noneが渡された場合にValueErrorをスローする(self):
        with pytest.raises(ValueError):
            {function_name}(None)
```

---

## Output

```
## 🧪 Test Generation

- 生成ファイル: tests/__tests__/userService.test.ts
- テスト数: 8件 (正常系: 3, 異常系: 3, エッジケース: 2)
```
