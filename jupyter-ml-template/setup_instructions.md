# Jupyter ML Template - Setup Instructions

Complete step-by-step guide to set up your Jupyter ML development environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Environment Setup](#environment-setup)
4. [Verification](#verification)
5. [JupyterLab Configuration](#jupyterlab-configuration)
6. [MLflow Setup](#mlflow-setup)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.13+**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads)
- **Text Editor/IDE**: VS Code (recommended) or your preferred editor

### Recommended Tools

- **uv**: Fast Python package manager ([installation guide](https://docs.astral.sh/uv/))
- **Claude Code**: For enhanced AI assistance

### System Requirements

- **Disk Space**: At least 5GB free
- **RAM**: 8GB minimum, 16GB recommended
- **OS**: Windows 10/11, macOS 10.15+, or Linux

## Installation Steps

### Step 1: Clone or Download Template

```bash
# If using git
git clone <repository-url> my-ml-project
cd my-ml-project

# Or download and extract ZIP file, then navigate to directory
cd my-ml-project
```

### Step 2: Install uv Package Manager

uv is a fast, modern Python package manager that's 10-100x faster than pip.

#### Windows

```powershell
# Using PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux

```bash
# Using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your terminal or source your shell config
source ~/.bashrc  # or ~/.zshrc for zsh
```

#### Verify Installation

```bash
uv --version
```

### Step 3: Install Python 3.13

uv can manage Python versions for you:

```bash
# Install Python 3.13
uv python install 3.13

# Pin project to Python 3.13
uv python pin 3.13
```

### Step 4: Create Virtual Environment

```bash
# Create virtual environment
uv venv

# uv creates .venv directory automatically
```

### Step 5: Activate Virtual Environment

#### Windows (Command Prompt)
```cmd
.venv\Scripts\activate.bat
```

#### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

#### macOS/Linux
```bash
source .venv/bin/activate
```

**You should see `(.venv)` in your terminal prompt.**

### Step 6: Install Dependencies

```bash
# Install all dependencies (production + development)
uv sync --all-extras

# Or install production dependencies only
uv sync
```

This will install:
- Core ML libraries (pandas, numpy, scikit-learn)
- Deep learning frameworks (PyTorch, TensorFlow)
- Advanced ML (XGBoost, LightGBM, CatBoost)
- Visualization (matplotlib, seaborn, plotly)
- MLOps (MLflow)
- Dev tools (black, ruff, mypy, pytest)

**Note**: First installation may take 5-15 minutes depending on your internet connection.

## Environment Setup

### Step 1: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Windows: notepad .env
# macOS/Linux: nano .env or vim .env
```

Example `.env` configuration:

```env
# Python Environment
PYTHONPATH=./src

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=default

# Jupyter Configuration
JUPYTER_PORT=8888

# Random Seeds (for reproducibility)
RANDOM_SEED=42
```

### Step 2: Configure Jupyter Kernel

Register the project's virtual environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name=jupyter-ml --display-name="Python 3.13 (ML)"
```

### Step 3: Create Data Directories

Ensure data directories exist:

```bash
# Already created, but verify
ls data/raw data/processed data/interim data/external
```

## Verification

### Verify Installation

Run these commands to verify everything is installed correctly:

```bash
# Check Python version
python --version
# Should show: Python 3.13.x

# Check installed packages
uv pip list

# Verify key packages
python -c "import pandas; print(f'pandas: {pandas.__version__}')"
python -c "import sklearn; print(f'scikit-learn: {sklearn.__version__}')"
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
```

### Test JupyterLab

```bash
# Start JupyterLab
jupyter lab --port=8888

# Or if using Claude Code
/start-jupyter
```

JupyterLab should open in your browser at `http://localhost:8888`

### Test MLflow

```bash
# Start MLflow UI
mlflow ui --port 5000
```

MLflow UI should be accessible at `http://localhost:5000`

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
# Windows: start htmlcov/index.html
# macOS: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

## JupyterLab Configuration

### Recommended Extensions

Install useful JupyterLab extensions:

```bash
# Install extensions
pip install jupyterlab-git  # Git integration
pip install jupyterlab-lsp python-lsp-server  # Code completion
pip install jupyter-resource-usage  # CPU/RAM monitoring
```

### JupyterLab Settings

Configure JupyterLab (Settings → Advanced Settings Editor):

**Code formatting** (install jupyterlab-code-formatter):
```json
{
    "formatOnSave": true,
    "preferences": {
        "default_formatter": {
            "python": "black"
        }
    }
}
```

**Autosave**:
```json
{
    "autosaveInterval": 120  # Save every 2 minutes
}
```

## MLflow Setup

### Initialize MLflow

```bash
# Create MLflow tracking directory
mkdir -p experiments/mlruns

# Set tracking URI (already in .env)
export MLFLOW_TRACKING_URI=http://localhost:5000
```

### Start MLflow Server

```bash
# Start in background (Unix/macOS)
nohup mlflow ui --port 5000 &

# Start in separate terminal (Windows)
# Open new terminal and run:
mlflow ui --port 5000
```

### Create First Experiment

```python
import mlflow

# Set experiment
mlflow.set_experiment("test_experiment")

# Start a run
with mlflow.start_run():
    mlflow.log_param("test_param", "value")
    mlflow.log_metric("test_metric", 0.95)

print("Test experiment created successfully!")
```

## Troubleshooting

### Issue: uv command not found

**Solution**:
```bash
# Restart terminal or source shell config
source ~/.bashrc  # or ~/.zshrc

# Or install with pip
pip install uv
```

### Issue: Python 3.13 not available

**Solution**:
```bash
# Use Python 3.11 or 3.12 instead
uv python install 3.11
uv python pin 3.11

# Update pyproject.toml:
# Change: requires-python = ">=3.13"
# To: requires-python = ">=3.11"
```

### Issue: Virtual environment activation fails

**Windows PowerShell Solution**:
```powershell
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\Activate.ps1
```

### Issue: PyTorch/TensorFlow installation errors

**Solution**:
```bash
# Install CPU versions (faster, smaller)
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install tensorflow-cpu

# Or for GPU support, check official docs:
# PyTorch: https://pytorch.org/get-started/locally/
# TensorFlow: https://www.tensorflow.org/install
```

### Issue: Jupyter kernel not found

**Solution**:
```bash
# Re-register kernel
python -m ipykernel install --user --name=jupyter-ml --display-name="Python 3.13 (ML)"

# List available kernels
jupyter kernelspec list

# Select kernel in notebook: Kernel → Change Kernel → Python 3.13 (ML)
```

### Issue: Import errors in notebooks

**Solution**:
```bash
# Ensure PYTHONPATH includes src/
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or add to notebook first cell:
import sys
sys.path.append('./src')
```

### Issue: MLflow UI not accessible

**Solution**:
```bash
# Check if port is in use
# Windows: netstat -ano | findstr :5000
# Unix/macOS: lsof -i :5000

# Use different port
mlflow ui --port 5001

# Update .env:
MLFLOW_TRACKING_URI=http://localhost:5001
```

### Issue: Out of memory errors

**Solution**:
```python
# Process data in chunks
chunk_size = 10000
chunks = pd.read_csv('large_file.csv', chunksize=chunk_size)
df = pd.concat([chunk for chunk in chunks])

# Use appropriate data types
df['category'] = df['category'].astype('category')
df['id'] = df['id'].astype('int32')

# Clear memory
import gc
del large_object
gc.collect()
```

### Issue: Package conflicts

**Solution**:
```bash
# Remove virtual environment
rm -rf .venv  # Unix/macOS
rmdir /s .venv  # Windows

# Recreate and reinstall
uv venv
uv sync --all-extras
```

## Next Steps

After successful setup:

1. **Explore Templates**:
   ```bash
   /create-notebook eda getting_started
   ```

2. **Try Example Workflow**:
   - Create EDA notebook
   - Load sample data
   - Run basic analysis
   - Train simple model

3. **Read Documentation**:
   - `README.md` - Project overview
   - `CLAUDE.md` - ML best practices
   - `.claude/commands/` - Available slash commands

4. **Start Your Project**:
   - Add your data to `data/raw/`
   - Create preprocessing notebook
   - Build features
   - Train models
   - Track experiments

## Getting Help

- **Claude Code**: Ask Claude for help with ML workflows
- **Documentation**: Check `README.md` and `CLAUDE.md`
- **Issues**: Report problems on GitHub Issues
- **Community**: Join ML communities for best practices

## Useful Commands Reference

```bash
# Virtual Environment
uv venv                          # Create environment
source .venv/bin/activate        # Activate (Unix/macOS)
.venv\Scripts\activate          # Activate (Windows)
deactivate                       # Deactivate

# Dependencies
uv sync                          # Install dependencies
uv add package-name              # Add new package
uv pip list                      # List installed packages

# Jupyter
jupyter lab                      # Start JupyterLab
jupyter notebook list            # List running servers
jupyter kernelspec list          # List available kernels

# MLflow
mlflow ui --port 5000           # Start UI
mlflow run .                    # Run MLflow project

# Code Quality
black src/ tests/               # Format code
ruff check src/ tests/          # Lint code
mypy src/                       # Type check
pytest                          # Run tests

# Claude Code Slash Commands
/start-jupyter                  # Start JupyterLab
/install-deps                   # Install dependencies
/format-code                    # Format code
/check-quality                  # Run quality checks
/track-experiment <name>        # Initialize experiment tracking
```

---

**Congratulations!** Your Jupyter ML environment is now ready for data science and machine learning projects. Happy coding! 🚀
