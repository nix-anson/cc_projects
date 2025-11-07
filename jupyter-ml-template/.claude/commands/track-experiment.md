---
description: Initialize MLflow or W&B experiment tracking
argument-hint: <experiment_name> [--backend mlflow|wandb]
---

Initialize experiment tracking for machine learning workflows using MLflow or Weights & Biases.

## Arguments

- `$1`: Name of the experiment (e.g., `customer_churn_v1`)
- `$2`: Optional backend selection: `mlflow` (default) or `wandb`

## Instructions

1. Check if MLflow server is running (for mlflow backend)
2. Create or set the experiment with the specified name
3. Initialize tracking context
4. Display experiment information:
   - Experiment ID
   - Tracking URI
   - Artifact location
5. Provide code snippet for logging in notebooks/scripts:

```python
import mlflow

# Set experiment
mlflow.set_experiment("$1")

# Start a run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)

    # Log model
    mlflow.sklearn.log_model(model, "model")
```

## For Weights & Biases

```python
import wandb

# Initialize
wandb.init(project="$1")

# Log metrics
wandb.log({"accuracy": 0.95, "loss": 0.05})

# Log artifacts
wandb.save("model.pkl")
```

## MLflow UI

To view experiments in MLflow:
```bash
mlflow ui --port 5000
```
Then open http://localhost:5000 in browser

## Weights & Biases UI

View experiments at: https://wandb.ai/your-username/$1

## Example Usage

```
/track-experiment customer_churn_xgboost
/track-experiment image_classification --backend wandb
```

## Notes

- MLflow stores experiments locally by default
- W&B requires account and API key in .env
- Experiments track parameters, metrics, and artifacts
- Use same experiment name for related runs
- Compare runs easily in the web UI
