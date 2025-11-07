---
description: Create a new Jupyter notebook from template
argument-hint: <template_type> <notebook_name>
---

Create a new Jupyter notebook from a predefined template with best practices and common imports.

## Arguments

- `$1`: Template type - one of: `eda`, `modeling`, `evaluation`, `preprocessing`, `feature_engineering`, `report`
- `$2`: Name for the new notebook (e.g., `customer_churn_analysis`)

## Instructions

1. Validate the template type exists
2. Determine the appropriate directory based on template type:
   - `eda` → `notebooks/01_eda/`
   - `preprocessing` → `notebooks/02_preprocessing/`
   - `feature_engineering` → `notebooks/03_feature_engineering/`
   - `modeling` → `notebooks/04_modeling/`
   - `evaluation` → `notebooks/05_evaluation/`
   - `report` → `notebooks/`
3. Copy the template from `notebooks/templates/{template_type}_template.ipynb`
4. Rename to `{notebook_name}.ipynb` in the target directory
5. Update the notebook title cell with the provided name
6. Inform the user where the notebook was created

## Template Types

- **eda**: Exploratory Data Analysis with data profiling, visualization setup
- **modeling**: Model training pipeline with cross-validation, hyperparameter tuning
- **evaluation**: Model evaluation with metrics, confusion matrix, ROC curves
- **preprocessing**: Data cleaning, transformation, missing value handling
- **feature_engineering**: Feature creation, selection, transformation
- **report**: Results reporting with markdown structure, executive summary

## Example Usage

```
/create-notebook eda customer_churn_analysis
/create-notebook modeling xgboost_classifier
/create-notebook evaluation model_comparison
```

## Notes

- Notebooks are created with a standardized structure
- All templates include common imports and utility functions
- Consider running `/format-code` after creating and editing
