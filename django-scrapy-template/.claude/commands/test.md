---
description: Run the pytest test suite with coverage reporting
argument-hint: "[path] [--cov-report html]"
---

Run the full test suite with coverage.

```bash
uv run pytest --cov=apps --cov-report=term-missing $ARGUMENTS
```

Run specific tests:

```bash
# Run only model tests
uv run pytest apps/tracker/tests/test_models.py -v

# Run only API tests
uv run pytest apps/tracker/tests/test_api.py -v

# Run with HTML coverage report
uv run pytest --cov=apps --cov-report=html
# Then open: htmlcov/index.html

# Run with verbose output and no capture
uv run pytest -v -s
```
