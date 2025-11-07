# Jupyter ML Template

A production-ready Jupyter template for machine learning projects with comprehensive Claude Code integration, modern Python tooling, and ML best practices.

## Features

✨ **Complete ML Stack**: pandas, numpy, scikit-learn, PyTorch, TensorFlow, XGBoost, LightGBM, CatBoost
📊 **Advanced Visualization**: matplotlib, seaborn, plotly for interactive and publication-quality plots
🔬 **Experiment Tracking**: MLflow for tracking parameters, metrics, and model versions
🎯 **Claude Code Integration**: 12 slash commands, 6 specialized agents, 4 skills for ML workflows
⚡ **Modern Tooling**: uv package manager, black, ruff, mypy, pytest for fast and clean development
📓 **Structured Notebooks**: Templates for EDA, modeling, evaluation, and reporting
🏗️ **Production-Ready**: Proper project structure separating notebooks from reusable source code
🔒 **Security First**: .gitignore configured to prevent committing data, models, or secrets

## Quick Start

### Prerequisites

- Python 3.13+
- [uv package manager](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone or download this template**:
   ```bash
   git clone <repository-url> my-ml-project
   cd my-ml-project
   ```

2. **Install uv** (if not already installed):
   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Unix/MacOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**:
   ```bash
   /install-deps
   ```
   Or manually:
   ```bash
   uv venv
   uv sync --all-extras
   ```

4. **Activate virtual environment**:
   ```bash
   # Windows
   .venv\Scripts\activate

   # Unix/MacOS
   source .venv/bin/activate
   ```

5. **Start JupyterLab**:
   ```bash
   /start-jupyter
   ```
   Or manually:
   ```bash
   uv run jupyter lab
   ```

6. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Project Structure

```
jupyter-ml-template/
├── notebooks/                  # Jupyter notebooks organized by workflow
│   ├── 01_eda/                # Exploratory Data Analysis
│   ├── 02_preprocessing/      # Data preprocessing experiments
│   ├── 03_feature_engineering/ # Feature creation and selection
│   ├── 04_modeling/           # Model training and tuning
│   ├── 05_evaluation/         # Model evaluation and comparison
│   └── templates/             # Notebook templates for quick start
├── data/                      # Data directory (git ignored)
│   ├── raw/                   # Original, immutable data
│   ├── processed/             # Cleaned, transformed data
│   ├── interim/               # Intermediate transformations
│   └── external/              # External data sources
├── models/                    # Trained model artifacts (git ignored)
│   ├── saved_models/          # Serialized models
│   ├── checkpoints/           # Training checkpoints
│   └── model_registry/        # Model versioning info
├── src/                       # Production-ready source code
│   ├── data/                  # Data processing modules
│   ├── features/              # Feature engineering modules
│   ├── models/                # Model training and prediction
│   ├── utils/                 # Utility functions
│   └── visualization/         # Visualization utilities
├── tests/                     # Unit and integration tests
├── configs/                   # Configuration files
├── experiments/               # MLflow experiment tracking
├── reports/                   # Generated analysis reports
│   └── figures/              # Generated visualizations
├── .claude/                   # Claude Code configuration
│   ├── settings.json         # Claude Code settings
│   ├── commands/             # 12 slash commands
│   ├── agents/               # 6 specialized agents
│   └── skills/               # 4 agent skills
├── pyproject.toml            # Project dependencies and config
├── .gitignore                # Git ignore patterns
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Claude Code Features

### 12 Slash Commands

Streamline common ML operations:

- `/start-jupyter` - Start JupyterLab server
- `/run-notebook <path>` - Execute notebook with parameters
- `/create-notebook <type> <name>` - Create from template (eda, modeling, evaluation, etc.)
- `/train-model <config>` - Train model with configuration
- `/evaluate-model <model> <data>` - Comprehensive model evaluation
- `/preprocess-data <input>` - Run preprocessing pipeline
- `/track-experiment <name>` - Initialize MLflow/W&B tracking
- `/install-deps` - Install dependencies with uv
- `/test-notebook [path]` - Run notebook tests
- `/format-code [path]` - Format with black and ruff
- `/check-quality [path]` - Run linting and type checks
- `/profile-notebook <path>` - Profile performance and memory

### 6 Specialized Agents

Expert agents that assist proactively:

1. **eda-specialist** - Data profiling, statistical analysis, visualization recommendations
2. **feature-engineer** - Feature creation, transformation, selection strategies
3. **model-optimizer** - Hyperparameter tuning, algorithm selection, training strategies
4. **ml-debugger** - Diagnose overfitting, data leakage, convergence issues
5. **experiment-tracker** - MLflow/W&B experiment management
6. **notebook-reviewer** - Review notebooks for best practices and reproducibility

### 4 Skills

Reusable patterns for common tasks:

1. **ml-pipeline** - Build sklearn pipelines with feature engineering
2. **notebook-templates** - Generate structured notebooks
3. **data-validation** - Great Expectations/Pandera validation
4. **model-deployment** - Package models for production

## Typical Workflow

### 1. Exploratory Data Analysis
```bash
/create-notebook eda customer_analysis
```
Open the created notebook and explore your data with built-in templates.

### 2. Data Preprocessing
```bash
/preprocess-data data/raw/customers.csv
```
Or create a preprocessing notebook:
```bash
/create-notebook preprocessing data_cleaning
```

### 3. Feature Engineering
Use the feature-engineer agent or create a notebook:
```bash
/create-notebook feature_engineering customer_features
```

### 4. Model Training
```bash
/track-experiment customer_churn_v1
/train-model configs/xgboost_config.yaml
```

### 5. Model Evaluation
```bash
/evaluate-model models/saved_models/xgboost_model.pkl data/processed/test_data.csv
```

### 6. Code Quality
```bash
/format-code
/check-quality
/test-notebook
```

## Development

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Notebook tests
pytest --nbval notebooks/
```

### Code Formatting
```bash
# Format code
black src/ tests/
ruff check --fix src/ tests/

# Type checking
mypy src/
```

### Experiment Tracking

#### MLflow
```bash
# Start MLflow UI
mlflow ui --port 5000
```
Visit http://localhost:5000 to view experiments.

#### In Code
```python
import mlflow

mlflow.set_experiment("my_experiment")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

## Best Practices

### Data Management
- Keep raw data immutable in `data/raw/`
- Store processed data in `data/processed/`
- Never commit data files to git
- Document data sources and versions

### Notebooks
- Clear outputs before committing
- One logical operation per cell
- Use markdown for documentation
- Set random seeds for reproducibility
- Keep notebooks focused and modular

### Code Organization
- Move reusable code to `src/` modules
- Write tests for data processing logic
- Use type hints for clarity
- Document functions with docstrings

### Model Training
- Track all experiments with MLflow
- Save model artifacts and metadata
- Version control configuration files
- Document hyperparameters and results

### Reproducibility
- Set random seeds everywhere
- Pin dependency versions
- Document environment setup
- Use pipelines for preprocessing

## Dependencies

### Core ML Libraries
- pandas, numpy, scikit-learn
- PyTorch, TensorFlow
- XGBoost, LightGBM, CatBoost

### Visualization
- matplotlib, seaborn, plotly

### MLOps
- MLflow for experiment tracking

### Data Validation
- Great Expectations, Pandera

### Development Tools
- black (formatting)
- ruff (linting)
- mypy (type checking)
- pytest (testing)

See `pyproject.toml` for complete list and versions.

## Troubleshooting

### uv Installation Issues
If uv fails to install, use pip as fallback:
```bash
python -m venv .venv
.venv\Scripts\activate  # or source .venv/bin/activate
pip install -r requirements.txt
```

### Jupyter Kernel Not Found
```bash
python -m ipykernel install --user --name=jupyter-ml
```

### Import Errors
Ensure PYTHONPATH includes src/:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### MLflow Connection Issues
Start MLflow server:
```bash
mlflow server --host 127.0.0.1 --port 5000
```

## Contributing

When contributing to this template:
1. Follow the existing project structure
2. Add tests for new functionality
3. Update documentation
4. Format code with black/ruff
5. Ensure notebooks run top-to-bottom

## License

MIT License - feel free to use this template for any project.

## Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [scikit-learn Documentation](https://scikit-learn.org)
- [MLflow Documentation](https://mlflow.org)
- [Jupyter Documentation](https://jupyter.org)
- [uv Documentation](https://docs.astral.sh/uv)

---

**Note**: This template is designed to be a starting point. Customize it for your specific use case, team conventions, and infrastructure requirements.
