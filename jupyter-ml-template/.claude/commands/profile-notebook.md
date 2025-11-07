---
description: Profile notebook performance and memory usage
argument-hint: <notebook_path>
---

Profile a Jupyter notebook to identify performance bottlenecks, memory usage, and execution time for each cell.

## Arguments

- `$1`: Path to the notebook to profile (e.g., `notebooks/04_modeling/train.ipynb`)

## Instructions

1. Verify the notebook exists
2. Execute the notebook with profiling enabled:
   ```bash
   uv run python -m memory_profiler jupyter nbconvert --to notebook --execute $1 --inplace
   ```

3. Analyze and report:
   - **Execution time per cell**
   - **Total execution time**
   - **Memory usage per cell**
   - **Peak memory usage**
   - **Cells taking longest to execute**
   - **Cells using most memory**

4. Generate profiling report in `reports/profiling/`

5. Provide optimization recommendations based on findings

## Profiling Output Format

```
Profiling Report: notebooks/04_modeling/train.ipynb
================================================

Total Execution Time: 2m 35s
Peak Memory Usage: 2.4 GB

Cell-by-Cell Analysis:
----------------------
Cell 1 (Load Data):
  - Execution: 5.2s
  - Memory: 450 MB
  - Status: ✓

Cell 2 (Feature Engineering):
  - Execution: 45.3s  ⚠️  SLOW
  - Memory: 1.2 GB   ⚠️  HIGH MEMORY
  - Status: ⚠️  Needs optimization

Cell 3 (Model Training):
  - Execution: 1m 32s
  - Memory: 800 MB
  - Status: ✓

Recommendations:
----------------
1. Cell 2: Consider vectorized operations instead of loops
2. Cell 2: Use chunking for large dataframes
3. Cell 3: Consider using sparse matrices
```

## Detailed Profiling

For line-by-line profiling of specific functions:

```python
# Add to notebook cell
%load_ext line_profiler
%lprun -f your_function your_function(args)
```

For memory profiling:
```python
%load_ext memory_profiler
%memit your_function(args)
```

## Example Usage

```
/profile-notebook notebooks/04_modeling/train.ipynb
/profile-notebook notebooks/02_preprocessing/data_cleaning.ipynb
```

## Optimization Tips

**Execution Time:**
- Use vectorized operations (pandas/numpy)
- Avoid Python loops on large datasets
- Use efficient data structures
- Consider parallel processing
- Cache expensive computations

**Memory Usage:**
- Process data in chunks
- Delete large objects when done
- Use appropriate data types (int8 vs int64)
- Use sparse matrices when applicable
- Clear outputs before committing notebooks

## Notes

- Profiling adds overhead to execution time
- Results vary based on system resources
- Profile on representative data sizes
- Use profiling to guide optimization efforts
- Consider using `%time` and `%timeit` for quick checks
