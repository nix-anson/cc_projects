---
description: Run data preprocessing pipeline with specified configuration
argument-hint: <input_data_path> [--config CONFIG_FILE]
---

Execute a data preprocessing pipeline to clean, transform, and prepare data for modeling.

## Arguments

- `$1`: Path to raw input data (e.g., `data/raw/dataset.csv`)
- `$2`: Optional preprocessing configuration file (defaults to `configs/preprocessing_config.yaml`)

## Instructions

1. Load raw data from the specified path
2. Load preprocessing configuration (if provided) or use defaults
3. Execute preprocessing steps in order:
   - Data type conversion
   - Missing value handling (imputation/removal)
   - Outlier detection and treatment
   - Feature scaling/normalization
   - Encoding categorical variables
   - Feature engineering (if specified)
4. Perform data quality checks
5. Save processed data to `data/processed/` with timestamp
6. Generate preprocessing report with statistics
7. Save preprocessing pipeline for later reuse
8. Display summary of transformations applied

## Configuration File Format

```yaml
missing_values:
  strategy: impute  # or drop
  numeric_fill: median
  categorical_fill: mode

outliers:
  method: iqr  # or zscore, isolation_forest
  action: clip  # or remove, keep

scaling:
  method: standard  # or minmax, robust, none
  columns: all  # or list of column names

encoding:
  categorical_columns:
    - column1
    - column2
  method: onehot  # or label, target

feature_engineering:
  create_interactions: false
  polynomial_features: false
  degree: 2

output:
  path: data/processed/
  filename: processed_data.csv
  save_pipeline: true
```

## Example Usage

```
/preprocess-data data/raw/customer_data.csv
/preprocess-data data/raw/sales.csv --config configs/custom_preprocessing.yaml
```

## Notes

- Preprocessing pipeline is saved for use on new data
- Data quality report is generated automatically
- Original raw data is never modified
- Use consistent preprocessing for train/test/prod data
