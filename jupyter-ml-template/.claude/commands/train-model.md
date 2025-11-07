---
description: Train a machine learning model with specified configuration
argument-hint: <config_file> [--experiment-name NAME]
---

Train a machine learning model using configuration from YAML file with automatic experiment tracking.

## Arguments

- `$1`: Path to model configuration file (e.g., `configs/xgboost_config.yaml`)
- `$2`: Optional experiment name for MLflow tracking (defaults to config filename)

## Instructions

1. Load the configuration file specified in $1
2. Validate required fields: model_type, data_path, target_column, features
3. Set up MLflow experiment tracking with provided or default experiment name
4. Load data from specified path
5. Perform train/test split or cross-validation as specified in config
6. Initialize the model with hyperparameters from config
7. Train the model with progress tracking
8. Log metrics, parameters, and model artifact to MLflow
9. Save trained model to `models/saved_models/`
10. Display training summary with metrics and artifact locations

## Configuration File Format

```yaml
model_type: xgboost  # or sklearn_random_forest, lightgbm, catboost, etc.
data_path: data/processed/train_data.csv
target_column: target
features:
  - feature1
  - feature2
hyperparameters:
  n_estimators: 100
  learning_rate: 0.1
  max_depth: 6
validation:
  method: cv  # or train_test_split
  n_folds: 5
  test_size: 0.2
tracking:
  log_model: true
  log_params: true
  log_metrics: true
```

## Example Usage

```
/train-model configs/xgboost_config.yaml
/train-model configs/random_forest.yaml --experiment-name customer_churn
```

## Notes

- Ensure data files exist before training
- MLflow UI can be started with `mlflow ui` to view experiments
- Models are versioned automatically
- Training progress is displayed in real-time
