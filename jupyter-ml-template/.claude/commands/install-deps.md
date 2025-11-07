---
description: Install project dependencies using uv package manager
argument-hint: [--dev] [--upgrade]
---

Install all project dependencies using the modern uv package manager for fast and reliable dependency management.

## Arguments

- `$1`: Optional flags:
  - `--dev`: Include development dependencies (pytest, black, ruff, mypy)
  - `--upgrade`: Upgrade all packages to latest compatible versions
  - `--all`: Install both production and development dependencies

## Instructions

1. Check if uv is installed, if not provide installation instructions
2. Verify Python 3.13 is available
3. Create virtual environment if it doesn't exist:
   ```bash
   uv venv
   ```
4. Install dependencies based on arguments:
   - No args: `uv sync`
   - `--dev`: `uv sync --all-extras`
   - `--upgrade`: `uv sync --upgrade`
5. Display installation summary:
   - Number of packages installed
   - Python version used
   - Virtual environment location
6. Remind user to activate virtual environment if not already active

## UV Commands Reference

```bash
# Basic installation
uv sync

# Install with dev dependencies
uv sync --all-extras

# Add a new package
uv add package-name

# Add dev dependency
uv add --dev package-name

# Remove package
uv remove package-name

# Upgrade packages
uv sync --upgrade

# Export to requirements.txt
uv export > requirements.txt
```

## Example Usage

```
/install-deps
/install-deps --dev
/install-deps --upgrade
```

## Virtual Environment Activation

**Windows:**
```bash
.venv\Scripts\activate
```

**Unix/MacOS:**
```bash
source .venv/bin/activate
```

## Notes

- uv is 10-100x faster than pip
- Automatically manages Python versions
- Creates lock file for reproducibility
- Supports parallel downloads
- Compatible with pip workflows
