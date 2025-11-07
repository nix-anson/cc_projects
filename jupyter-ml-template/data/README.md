# Data Directory

This directory contains all data files used in the project. Data files are excluded from version control via `.gitignore`.

## Directory Structure

```
data/
├── raw/            # Original, immutable data
├── processed/      # Cleaned, transformed data ready for modeling
├── interim/        # Intermediate data transformations
└── external/       # External data sources
```

## Usage Guidelines

### `raw/`
- Store original, unmodified data files
- **Never modify files in this directory**
- Document data sources and collection dates
- Use descriptive filenames with dates (e.g., `customers_20250106.csv`)

### `processed/`
- Store cleaned and transformed data
- Data should be ready for model training
- Include preprocessing pipeline artifacts
- Use consistent naming conventions

### `interim/`
- Store intermediate transformation results
- Useful for multi-step processing pipelines
- Can be safely deleted and regenerated

### `external/`
- Store data from external sources
- Document source URLs and download dates
- Consider automating downloads when possible

## Best Practices

1. **Documentation**: Create a data dictionary documenting all datasets
2. **Versioning**: Use dates or version numbers in filenames
3. **Formats**: Prefer efficient formats (parquet, feather) for large datasets
4. **Security**: Never commit sensitive or personal data
5. **Size**: Keep individual files under 100MB when possible

## Data Management

### Loading Data
```python
from src.data.loaders import load_csv

df = load_csv('data/raw/dataset.csv')
```

### Saving Processed Data
```python
from src.data.loaders import save_data

save_data(df_processed, 'data/processed/clean_data.csv')
save_data(df_processed, 'data/processed/clean_data.parquet', format='parquet')
```

## Data Privacy

- Anonymize personal information
- Follow GDPR/CCPA guidelines
- Document data retention policies
- Implement access controls for sensitive data

## Adding New Data

1. Place raw data in `data/raw/`
2. Create preprocessing notebook in `notebooks/02_preprocessing/`
3. Save processed data to `data/processed/`
4. Document in data dictionary
5. Update experiment tracking

---

**Note**: This directory is git ignored. Data files will not be committed to version control.
