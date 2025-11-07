# Models Directory

This directory contains trained machine learning models and related artifacts. Model files are excluded from version control via `.gitignore`.

## Directory Structure

```
models/
├── saved_models/       # Serialized trained models
├── checkpoints/        # Training checkpoints
└── model_registry/     # Model versioning information
```

## Usage Guidelines

### `saved_models/`
- Store final trained models
- Use descriptive names with versions
- Include model metadata
- Format: `{model_type}_{date}_v{version}.pkl`

Example:
```
xgboost_20250106_v1.0.pkl
random_forest_customer_churn_v2.3.pkl
```

### `checkpoints/`
- Store intermediate training checkpoints
- Useful for resuming long training runs
- Can include optimizer states

### `model_registry/`
- Store model versioning metadata
- Track model lineage and experiments
- Document model performance

## Saving Models

### Basic Model Saving
```python
import joblib
from datetime import datetime

# Save model
model_path = f'models/saved_models/xgboost_{datetime.now().strftime("%Y%m%d")}_v1.0.pkl'
joblib.dump(model, model_path)
```

### Save with Metadata
```python
from src.utils.helpers import save_model_metadata

metadata = {
    'model_type': 'XGBoost',
    'version': '1.0',
    'features': feature_names,
    'hyperparameters': {'n_estimators': 100, 'max_depth': 6},
    'performance': {
        'train_accuracy': 0.95,
        'val_accuracy': 0.92,
        'test_accuracy': 0.91
    },
    'training_data': 'data/processed/train_20250106.csv',
    'training_date': datetime.now().isoformat()
}

save_model_metadata(model, metadata, model_path)
```

## Loading Models

```python
from src.utils.helpers import load_model_with_metadata

# Load model and metadata
model, metadata = load_model_with_metadata('models/saved_models/xgboost_v1.0.pkl')

# Access metadata
print(f"Model type: {metadata['model_type']}")
print(f"Test accuracy: {metadata['performance']['test_accuracy']}")
```

## Model Versioning

### Version Naming Convention
- **Major version** (X.0): Significant architecture changes
- **Minor version** (1.X): Hyperparameter tuning, feature changes
- **Patch version** (1.0.X): Bug fixes, small improvements

Examples:
- `v1.0` - Initial model
- `v1.1` - Added new features
- `v2.0` - Changed from Random Forest to XGBoost

### MLflow Integration

Models tracked with MLflow are automatically versioned:

```python
import mlflow

mlflow.set_experiment("customer_churn")

with mlflow.start_run():
    # Train model
    model.fit(X_train, y_train)

    # Log model
    mlflow.sklearn.log_model(model, "model")

    # Register model
    mlflow.register_model(f"runs:/{run.info.run_id}/model", "churn_prediction_model")
```

## Model Formats

### Recommended Formats

1. **Joblib** (`.pkl`): sklearn models, fast and efficient
2. **ONNX** (`.onnx`): Cross-platform, production deployment
3. **SavedModel** (TensorFlow): Deep learning models
4. **PyTorch** (`.pt`, `.pth`): PyTorch models

### Format Comparison

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| Joblib | sklearn models | Fast, efficient | Python-specific |
| ONNX | Production deployment | Cross-platform | Conversion overhead |
| Pickle | General Python objects | Simple | Security concerns |
| SavedModel | TensorFlow models | Full graph | Large file size |

## Best Practices

1. **Never commit large models**: Use `.gitignore` to exclude
2. **Document thoroughly**: Include metadata with every model
3. **Version systematically**: Follow semantic versioning
4. **Track experiments**: Use MLflow or similar tool
5. **Test before deployment**: Validate on holdout test set
6. **Monitor performance**: Track model metrics over time

## Model Deployment

### Preparing for Deployment

1. Save model with preprocessor:
```python
from sklearn.pipeline import Pipeline

# Full pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model)
])

joblib.dump(pipeline, 'models/saved_models/pipeline_v1.0.pkl')
```

2. Create deployment package:
```
deployment/
├── model.pkl
├── requirements.txt
├── api.py
└── Dockerfile
```

3. Test deployment:
```python
# Load and test
loaded_pipeline = joblib.load('models/saved_models/pipeline_v1.0.pkl')
predictions = loaded_pipeline.predict(X_new)
```

## Model Registry

### Track Model Information

Create a model registry file: `models/model_registry/registry.json`

```json
{
  "customer_churn_v1.0": {
    "model_path": "saved_models/xgboost_20250106_v1.0.pkl",
    "status": "production",
    "created_at": "2025-01-06T10:30:00",
    "performance": {
      "accuracy": 0.91,
      "f1_score": 0.89,
      "roc_auc": 0.94
    },
    "features": ["age", "income", "tenure", ...],
    "notes": "Initial production model"
  },
  "customer_churn_v1.1": {
    "model_path": "saved_models/xgboost_20250115_v1.1.pkl",
    "status": "staging",
    "created_at": "2025-01-15T14:20:00",
    "performance": {
      "accuracy": 0.93,
      "f1_score": 0.91,
      "roc_auc": 0.95
    },
    "features": ["age", "income", "tenure", "engagement_score", ...],
    "notes": "Added engagement features, improved performance"
  }
}
```

## Cleanup

Periodically clean up old checkpoints and outdated models:

```bash
# Remove old checkpoints (older than 30 days)
find models/checkpoints/ -type f -mtime +30 -delete

# Archive old models before deletion
tar -czf models/archive/models_2024.tar.gz models/saved_models/*_2024*
```

---

**Note**: This directory is git ignored. Model files will not be committed to version control. Use MLflow or model registry for versioning and collaboration.
