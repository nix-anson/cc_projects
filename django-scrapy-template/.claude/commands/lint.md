---
description: Run black, isort, and flake8 code quality checks
---

Check code formatting and style.

```bash
uv run black --check . && uv run isort --check-only . && uv run flake8 .
```

Auto-fix formatting issues:

```bash
uv run black . && uv run isort .
```

Run individual tools:

```bash
# Check formatting only
uv run black --check .

# Check import sorting
uv run isort --check-only .

# Check style and type issues
uv run flake8 .
```
