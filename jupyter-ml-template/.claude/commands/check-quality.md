---
description: Run code quality checks with ruff and mypy
argument-hint: [path]
---

Perform comprehensive code quality checks including linting, style violations, and type checking.

## Arguments

- `$1`: Optional path to check (defaults to `src/` and `tests/`)

## Instructions

1. Run ruff linting checks:
   ```bash
   uv run ruff check $1
   ```
   - Checks for code smells, potential bugs
   - Validates import ordering
   - Identifies unused imports and variables
   - Finds complexity issues

2. Run mypy type checking:
   ```bash
   uv run mypy $1
   ```
   - Validates type annotations
   - Catches type-related errors
   - Ensures type consistency

3. Display comprehensive report:
   - Total number of issues found
   - Breakdown by category (errors, warnings, info)
   - File-specific issues with line numbers
   - Suggestions for fixes

4. Exit with appropriate code:
   - 0 if no issues found
   - Non-zero if issues exist

## Quality Checks Performed

**Ruff checks:**
- E/W: pycodestyle errors and warnings
- F: pyflakes (undefined names, unused imports)
- I: isort (import ordering)
- B: flake8-bugbear (likely bugs and design problems)
- C4: flake8-comprehensions
- UP: pyupgrade (upgrade syntax for newer Python)

**Mypy checks:**
- Type annotation correctness
- Type compatibility
- Optional value handling
- Return type consistency

## Example Usage

```
/check-quality
/check-quality src/models/
/check-quality src/data/preprocessors.py
```

## Common Issues and Fixes

**Unused import:**
```python
# Remove or use the import
import pandas as pd  # F401: imported but unused
```

**Line too long:**
```python
# Break into multiple lines (handled by black)
result = some_function(arg1, arg2, arg3, arg4)
```

**Missing type hints:**
```python
# Add type annotations
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    return df
```

## Configuration

Quality checks configured in `pyproject.toml`:
- Line length: 88 characters
- Target Python version: 3.13
- Type checking: gradual typing mode

## Notes

- Fix issues before committing code
- Many issues can be auto-fixed with `ruff check --fix`
- Type errors may require code refactoring
- Use `# type: ignore` sparingly and with comments
- CI/CD should enforce quality checks
