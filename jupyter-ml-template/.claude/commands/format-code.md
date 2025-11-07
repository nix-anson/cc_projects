---
description: Format Python code and notebooks using black and ruff
argument-hint: [path] [--check]
---

Format Python code and Jupyter notebooks to maintain consistent code style across the project.

## Arguments

- `$1`: Optional path to format (file or directory), defaults to entire project
- `$2`: Optional `--check` flag to only check without modifying files

## Instructions

1. Determine the target path (default to `src/` and notebooks if not specified)

2. Format Python files with black:
   ```bash
   uv run black $1
   ```

3. Auto-fix linting issues with ruff:
   ```bash
   uv run ruff check --fix $1
   ```

4. If `--check` flag is provided, run in check-only mode:
   ```bash
   uv run black --check $1
   uv run ruff check $1
   ```

5. Display summary:
   - Number of files formatted/checked
   - Any remaining linting issues
   - Files that would be reformatted (in check mode)

## Formatting Standards

- **Line length**: 88 characters (Black default)
- **String quotes**: Double quotes preferred
- **Import sorting**: Automatic with ruff
- **Type hints**: Encouraged but not enforced

## Example Usage

```
/format-code
/format-code src/models/train.py
/format-code notebooks/
/format-code --check
```

## Pre-commit Hook

To automatically format on commit, add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
uv run black src/ tests/
uv run ruff check --fix src/ tests/
```

Make executable: `chmod +x .git/hooks/pre-commit`

## Notes

- Formatting is non-destructive and reversible
- Black is opinionated and minimizes configuration
- Ruff is extremely fast (~10-100x faster than flake8)
- Notebooks can be formatted but may need manual cleanup
- Use `# fmt: off` and `# fmt: on` to disable formatting for specific sections
- Settings configured in pyproject.toml
