---
description: Run all quality checks
---

Run all code quality checks: linting, type checking, and tests.

```bash
echo "Running Ruff linter..."
ruff check .

echo "Running type checker..."
mypy .

echo "Running tests with coverage..."
pytest --cov=app --cov-report=term-missing

echo "All checks complete!"
```

This command runs:
1. Ruff linting
2. mypy type checking
3. pytest with coverage

If all checks pass, your code is ready for commit.
