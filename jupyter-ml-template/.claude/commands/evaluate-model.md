---
description: Evaluate a trained model with comprehensive metrics
argument-hint: <model_path> <test_data_path>
---

Evaluate a trained machine learning model on test data with comprehensive metrics and visualizations.

## Arguments

- `$1`: Path to the trained model file (e.g., `models/saved_models/xgboost_model.pkl`)
- `$2`: Path to test data (e.g., `data/processed/test_data.csv`)

## Instructions

1. Load the trained model from the specified path
2. Load test data from the specified path
3. Generate predictions on test data
4. Calculate comprehensive metrics based on task type:
   - **Classification**: accuracy, precision, recall, F1-score, ROC-AUC, confusion matrix
   - **Regression**: MAE, MSE, RMSE, R², MAPE
5. Generate visualizations:
   - Classification: confusion matrix heatmap, ROC curve, precision-recall curve
   - Regression: actual vs predicted plot, residual plot, error distribution
6. Save metrics to `reports/metrics.json`
7. Save visualizations to `reports/figures/`
8. Display summary of results
9. Optionally log results to MLflow if experiment is active

## Output Format

```json
{
  "model_path": "models/saved_models/xgboost_model.pkl",
  "test_data_path": "data/processed/test_data.csv",
  "metrics": {
    "accuracy": 0.95,
    "precision": 0.94,
    "recall": 0.96,
    "f1_score": 0.95,
    "roc_auc": 0.98
  },
  "confusion_matrix": [[100, 5], [3, 92]],
  "timestamp": "2025-01-15T10:30:00"
}
```

## Example Usage

```
/evaluate-model models/saved_models/xgboost_model.pkl data/processed/test_data.csv
```

## Notes

- Automatically detects classification vs regression task
- Visualizations are saved as PNG files
- Metrics can be compared across model versions
- Consider using with `/track-experiment` for experiment tracking
