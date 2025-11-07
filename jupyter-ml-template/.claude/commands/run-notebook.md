---
description: Execute a Jupyter notebook with optional parameters
argument-hint: <notebook_path> [param1=value1 param2=value2 ...]
---

Execute a Jupyter notebook programmatically, optionally passing parameters for parameterized notebooks.

## Arguments

- `$1`: Path to the notebook to execute (e.g., `notebooks/01_eda/analysis.ipynb`)
- `$2+`: Optional parameters in format `key=value` for parameterized notebooks

## Instructions

1. Verify the notebook exists at the specified path
2. If parameters are provided, use papermill to execute with parameters:
   ```bash
   uv run papermill $1 $1 -p param1 value1 -p param2 value2
   ```
3. If no parameters, execute using nbconvert:
   ```bash
   uv run jupyter nbconvert --to notebook --execute $1 --inplace
   ```
4. Display execution status and any errors
5. Show execution time and cell-level statistics

## Example Usage

```
/run-notebook notebooks/01_eda/analysis.ipynb
/run-notebook notebooks/04_modeling/train.ipynb model_type=xgboost n_estimators=100
```

## Notes

- Parameterized notebooks must use the papermill parameter cell convention
- Execution errors will be captured and displayed
- Output is saved back to the same notebook file
- Consider using `--inplace` flag carefully in production
