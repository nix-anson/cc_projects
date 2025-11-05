---
description: Run mypy type checking
argument-hint: '[path]'
---

Run mypy to check type annotations.

```bash
mypy ${1:-.}
```

Checks all Python files for type consistency according to pyproject.toml configuration.
