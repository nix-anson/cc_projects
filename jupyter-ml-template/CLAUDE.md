# Jupyter ML Project Context

This document provides essential context for Claude Code when working with this Jupyter machine learning project.

## Project Overview

**Type**: Machine Learning / Data Science Project
**Framework**: Jupyter notebooks + Python 3.13
**Purpose**: End-to-end ML workflows from EDA to model deployment
**Architecture**: Notebook-based experimentation with production-ready source code in `src/`

## Technology Stack

### Core ML Libraries
- **pandas** (>=2.2.0): Data manipulation and analysis
- **numpy** (>=1.26.0): Numerical computing
- **scikit-learn** (>=1.4.0): Traditional ML algorithms and pipelines

### Deep Learning
- **PyTorch** (>=2.2.0): Neural networks and deep learning
- **TensorFlow** (>=2.15.0): Alternative deep learning framework

### Advanced ML
- **XGBoost** (>=2.0.0): Gradient boosting
- **LightGBM** (>=4.3.0): Fast gradient boosting
- **CatBoost** (>=1.2.0): Gradient boosting with categorical support

### Visualization
- **matplotlib** (>=3.8.0): Basic plotting
- **seaborn** (>=0.13.0): Statistical visualizations
- **plotly** (>=5.18.0): Interactive visualizations

### MLOps
- **MLflow** (>=2.10.0): Experiment tracking and model registry

### Data Validation
- **Great Expectations** (>=0.18.0): Data quality and validation
- **Pandera** (>=0.18.0): DataFrame validation

### Development Tools
- **black**: Code formatting
- **ruff**: Fast linting
- **mypy**: Type checking
- **pytest**: Testing framework

## Project Structure Philosophy

### Separation of Concerns
- **`notebooks/`**: Experimental, exploratory analysis
- **`src/`**: Production-ready, tested, reusable code
- **`data/`**: Data files (gitignored)
- **`models/`**: Model artifacts (gitignored)
- **`tests/`**: Unit and integration tests

### Notebook Organization
Notebooks are organized by ML workflow stage:
1. **01_eda/**: Exploratory Data Analysis
2. **02_preprocessing/**: Data cleaning and transformation
3. **03_feature_engineering/**: Feature creation and selection
4. **04_modeling/**: Model training and tuning
5. **05_evaluation/**: Model evaluation and comparison

## Common Operations

### Starting Work
1. Activate virtual environment
2. Start JupyterLab: `/start-jupyter`
3. Create notebook from template: `/create-notebook <type> <name>`

### Data Processing
1. Load raw data from `data/raw/`
2. Preprocess: `/preprocess-data <input>`
3. Save to `data/processed/`
4. Never modify raw data

### Model Training
1. Initialize experiment: `/track-experiment <name>`
2. Train model: `/train-model <config>` or in notebook
3. Log to MLflow automatically
4. Save artifacts to `models/saved_models/`

### Evaluation
1. Load test data from `data/processed/`
2. Evaluate: `/evaluate-model <model_path> <test_data>`
3. Generate metrics and visualizations
4. Save reports to `reports/`

## Code Style and Conventions

### Python Code
- **Line length**: 88 characters (Black default)
- **Imports**: Grouped (stdlib, third-party, local) and sorted
- **Naming**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
- **Type hints**: Encouraged, especially for function signatures
- **Docstrings**: Google or numpy style

### Notebooks
- **Structure**: Title → Setup → Content → Conclusions
- **Cells**: One logical operation per cell
- **Documentation**: Markdown cells for every major section
- **Outputs**: Clear before committing (selective exceptions)
- **Reproducibility**: Set random seeds, use relative paths

### Example Code Structure
```python
# =============================================================================
# IMPORTS
# =============================================================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# =============================================================================
# CONFIGURATION
# =============================================================================
RANDOM_SEED = 42
DATA_PATH = './data/processed/dataset.csv'

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the input dataframe.

    Args:
        df: Raw dataframe

    Returns:
        Preprocessed dataframe
    """
    # Implementation
    return df

# =============================================================================
# MAIN WORKFLOW
# =============================================================================
# Load data
df = pd.read_csv(DATA_PATH)

# Preprocess
df_clean = preprocess_data(df)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    df_clean.drop('target', axis=1),
    df_clean['target'],
    test_size=0.2,
    random_state=RANDOM_SEED
)
```

## ML Best Practices

### Data Handling
- **Raw data is immutable**: Never modify `data/raw/`
- **Preprocessor fit**: Fit only on training data
- **Data leakage**: Never use test data in feature engineering
- **Missing values**: Handle explicitly, don't ignore
- **Outliers**: Understand before removing

### Feature Engineering
- **Domain knowledge**: Use it to create meaningful features
- **Interactions**: Test feature combinations
- **Scaling**: Apply to numeric features before modeling
- **Encoding**: One-hot for nominal, target/label for high cardinality
- **Selection**: Remove low-variance and highly correlated features

### Model Training
- **Baseline first**: Start with simple models
- **Cross-validation**: Always use for model selection
- **Hyperparameter tuning**: Systematic (Grid/Random/Bayesian search)
- **Regularization**: Prevent overfitting
- **Early stopping**: Use with validation set

### Evaluation
- **Hold-out test set**: Use only for final evaluation
- **Multiple metrics**: Don't rely on accuracy alone
- **Confusion matrix**: For classification problems
- **Residual plots**: For regression problems
- **Feature importance**: Understand model decisions

### Reproducibility
- **Random seeds**: Set for all stochastic operations
- **Versions**: Pin dependency versions
- **Pipelines**: Use sklearn Pipeline for preprocessing
- **Documentation**: Document all decisions
- **Logging**: Track experiments with MLflow

## Common Patterns

### Pattern 1: EDA Workflow
```python
# 1. Load and overview
df = pd.read_csv(DATA_PATH)
print(df.shape, df.dtypes)

# 2. Missing values
df.isnull().sum()

# 3. Distributions
df.describe()
df.hist(bins=50, figsize=(20,15))

# 4. Correlations
sns.heatmap(df.corr(), annot=True)

# 5. Target analysis
df.groupby('target').mean()
```

### Pattern 2: Preprocessing Pipeline
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Fit on train only
X_train_processed = pipeline.fit_transform(X_train)
X_test_processed = pipeline.transform(X_test)
```

### Pattern 3: Model Training with Tracking
```python
import mlflow
from sklearn.ensemble import RandomForestClassifier

mlflow.set_experiment("customer_churn")

with mlflow.start_run():
    # Log parameters
    params = {'n_estimators': 100, 'max_depth': 10}
    mlflow.log_params(params)

    # Train model
    model = RandomForestClassifier(**params, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate and log metrics
    train_score = model.score(X_train, y_train)
    val_score = model.score(X_val, y_val)
    mlflow.log_metric("train_accuracy", train_score)
    mlflow.log_metric("val_accuracy", val_score)

    # Log model
    mlflow.sklearn.log_model(model, "model")
```

### Pattern 4: Model Evaluation
```python
from sklearn.metrics import classification_report, confusion_matrix

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# Metrics
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.show()

# ROC curve
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_test, y_pred_proba[:, 1])
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

## Security Considerations

### Data Protection
- **Never commit**: Raw data, processed data, model artifacts
- **gitignore**: Configured to exclude `data/` and `models/`
- **Sensitive info**: Use `.env` for API keys, never hardcode
- **Notebook outputs**: Clear before committing to avoid data leakage

### Dependency Security
- **Pin versions**: Specified in `pyproject.toml`
- **Regular updates**: Keep dependencies current
- **Vulnerability scanning**: Use tools like `safety` or `pip-audit`

### Model Security
- **Input validation**: Always validate inference inputs
- **Model artifacts**: Don't commit large models to git
- **Access control**: Restrict access to production models

## Performance Optimization

### Data Operations
- **Vectorization**: Use pandas/numpy operations, avoid loops
- **Chunking**: Process large files in chunks
- **Data types**: Use appropriate dtypes (int8 vs int64, category)
- **Indexing**: Set index for faster lookups

### Model Training
- **Parallel processing**: Use `n_jobs=-1` where available
- **GPU**: Use for deep learning (PyTorch/TensorFlow)
- **Early stopping**: Don't train longer than needed
- **Sampling**: Use stratified sampling for large datasets

### Memory Management
- **Delete unused**: Free memory with `del` and `gc.collect()`
- **In-place operations**: Use when appropriate
- **Sparse matrices**: For high-dimensional data
- **Data types**: Optimize memory with smaller dtypes

## Common Issues and Solutions

### Issue: Model Overfitting
**Symptoms**: High train accuracy, low validation accuracy
**Solutions**:
- More training data
- Reduce model complexity
- Apply regularization (L1, L2)
- Use cross-validation
- Feature selection

### Issue: Poor Model Performance
**Symptoms**: Low accuracy on both train and validation
**Solutions**:
- Better feature engineering
- More complex model
- Check for data quality issues
- Ensure proper preprocessing
- Address class imbalance

### Issue: Data Leakage
**Symptoms**: Unrealistically high performance
**Solutions**:
- Split data before preprocessing
- Fit transformers only on training data
- Remove target-derived features
- Check for temporal leakage

### Issue: Convergence Problems
**Symptoms**: Training loss not decreasing
**Solutions**:
- Scale features (StandardScaler, MinMaxScaler)
- Reduce learning rate
- Check for NaN/Inf values
- Try different optimizer
- Use gradient clipping

## Testing Guidelines

### Unit Tests
```python
# tests/test_preprocessing.py
import pytest
from src.data.preprocessors import clean_data

def test_clean_data_removes_nulls():
    df = pd.DataFrame({'a': [1, None, 3]})
    result = clean_data(df)
    assert result.isnull().sum().sum() == 0
```

### Notebook Tests
```bash
# Test notebooks execute without errors
pytest --nbval notebooks/01_eda/analysis.ipynb
```

### Integration Tests
```python
# Test full pipeline
def test_full_pipeline():
    # Load data
    df = pd.read_csv('data/raw/test_data.csv')

    # Preprocess
    X, y = preprocess(df)

    # Train
    model = train_model(X, y)

    # Evaluate
    score = evaluate_model(model, X, y)

    assert score > 0.7  # Minimum acceptable performance
```

## Links and Resources

- **MLflow UI**: http://localhost:5000 (after running `mlflow ui`)
- **JupyterLab**: http://localhost:8888 (after running `/start-jupyter`)
- **Documentation**: See README.md for detailed setup
- **Templates**: `notebooks/templates/` for quick starts

## Tips for Claude Code

- Use specialized agents proactively (eda-specialist, feature-engineer, etc.)
- Leverage slash commands for common operations
- Follow the established project structure
- Always track experiments with MLflow
- Validate data before training
- Test notebooks before committing
- Document assumptions and decisions
- Keep notebooks focused and modular

---

**Remember**: Good ML projects are reproducible, well-documented, and maintainable. Follow these conventions to ensure quality and collaboration success.
