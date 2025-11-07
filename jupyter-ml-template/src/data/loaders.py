"""
Data loading utilities for various data sources.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union


def load_csv(
    file_path: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """
    Load data from CSV file.

    Args:
        file_path: Path to CSV file
        **kwargs: Additional arguments to pass to pd.read_csv()

    Returns:
        DataFrame with loaded data

    Example:
        >>> df = load_csv('data/raw/dataset.csv')
        >>> df = load_csv('data/raw/large_file.csv', chunksize=10000)
    """
    return pd.read_csv(file_path, **kwargs)


def load_excel(
    file_path: Union[str, Path],
    sheet_name: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Load data from Excel file.

    Args:
        file_path: Path to Excel file
        sheet_name: Name of sheet to load (None for first sheet)
        **kwargs: Additional arguments to pass to pd.read_excel()

    Returns:
        DataFrame with loaded data
    """
    return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)


def save_data(
    df: pd.DataFrame,
    file_path: Union[str, Path],
    format: str = 'csv',
    **kwargs
) -> None:
    """
    Save DataFrame to file.

    Args:
        df: DataFrame to save
        file_path: Output file path
        format: Output format ('csv', 'parquet', 'excel')
        **kwargs: Additional arguments for save function

    Example:
        >>> save_data(df, 'data/processed/clean_data.csv')
        >>> save_data(df, 'data/processed/data.parquet', format='parquet')
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format == 'csv':
        df.to_csv(file_path, index=False, **kwargs)
    elif format == 'parquet':
        df.to_parquet(file_path, index=False, **kwargs)
    elif format == 'excel':
        df.to_excel(file_path, index=False, **kwargs)
    else:
        raise ValueError(f"Unsupported format: {format}")
