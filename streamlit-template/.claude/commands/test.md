---
description: Run pytest with coverage
argument-hint: '[test_path]'
---

Run pytest tests with coverage reporting.

If $1 is provided, run specific test file or directory. Otherwise, run all tests.

```bash
pytest ${1:-.} --cov=app --cov-report=term-missing --cov-report=html -v
```

Coverage report will be generated in `htmlcov/` directory.
