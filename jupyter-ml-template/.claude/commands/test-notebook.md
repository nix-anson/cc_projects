---
description: Run tests for Jupyter notebooks and Python code
argument-hint: [notebook_path] [--all]
---

Execute tests for Jupyter notebooks using nbval and Python code using pytest.

## Arguments

- `$1`: Optional notebook path or test type:
  - Specific notebook: `notebooks/01_eda/analysis.ipynb`
  - `--all`: Test all notebooks in the project
  - Empty: Run pytest on Python modules only

## Instructions

### For Notebook Testing (with nbval)

1. If specific notebook provided:
   ```bash
   uv run pytest --nbval $1
   ```

2. If `--all` flag provided:
   ```bash
   uv run pytest --nbval notebooks/
   ```

3. Notebook testing validates:
   - All cells execute without errors
   - Output matches stored output (if using strict mode)
   - No exceptions raised during execution

### For Python Module Testing

1. Run pytest on src/ and tests/ directories:
   ```bash
   uv run pytest tests/ -v --cov=src --cov-report=html
   ```

2. Display:
   - Test results summary
   - Code coverage percentage
   - Failed tests with details
   - Coverage report location

## Test Configuration

Tests are configured in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--strict-markers", "--cov=src", "--cov-report=html"]
```

## Example Usage

```
/test-notebook notebooks/01_eda/analysis.ipynb
/test-notebook --all
/test-notebook
```

## Coverage Report

After running tests, view HTML coverage report:
```bash
open htmlcov/index.html  # Unix/MacOS
start htmlcov/index.html  # Windows
```

## Notes

- Notebooks should clear outputs before committing
- Use `pytest.mark.skip` to skip specific tests
- Coverage helps identify untested code
- Failed notebook tests show the problematic cell
- Consider using CI/CD to run tests automatically
