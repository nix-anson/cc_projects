"""
Data preprocessing utilities.
"""

import pandas as pd
import numpy as np
from typing import List, Optional


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = 'drop',
    fill_value: Optional[dict] = None
) -> pd.DataFrame:
    """
    Handle missing values in DataFrame.

    Args:
        df: Input DataFrame
        strategy: Strategy to handle missing values ('drop', 'fill_mean', 'fill_median', 'fill_mode', 'fill_value')
        fill_value: Dictionary of column: value for 'fill_value' strategy

    Returns:
        DataFrame with missing values handled

    Example:
        >>> df_clean = handle_missing_values(df, strategy='fill_median')
        >>> df_clean = handle_missing_values(df, strategy='fill_value', fill_value={'age': 0, 'income': 50000})
    """
    df = df.copy()

    if strategy == 'drop':
        return df.dropna()

    elif strategy == 'fill_mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        return df

    elif strategy == 'fill_median':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        return df

    elif strategy == 'fill_mode':
        for col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else np.nan)
        return df

    elif strategy == 'fill_value' and fill_value:
        return df.fillna(fill_value)

    else:
        raise ValueError(f"Unsupported strategy: {strategy}")


def remove_outliers(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: str = 'iqr',
    factor: float = 1.5
) -> pd.DataFrame:
    """
    Remove outliers from DataFrame.

    Args:
        df: Input DataFrame
        columns: List of columns to check for outliers (None for all numeric)
        method: Outlier detection method ('iqr' or 'zscore')
        factor: Factor for IQR method or threshold for z-score method

    Returns:
        DataFrame with outliers removed

    Example:
        >>> df_clean = remove_outliers(df, columns=['age', 'income'], method='iqr')
        >>> df_clean = remove_outliers(df, method='zscore', factor=3)
    """
    df = df.copy()

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if method == 'iqr':
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - factor * IQR
            upper_bound = Q3 + factor * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    elif method == 'zscore':
        from scipy import stats
        for col in columns:
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            df = df[z_scores < factor]

    else:
        raise ValueError(f"Unsupported method: {method}")

    return df


def encode_categorical(
    df: pd.DataFrame,
    columns: List[str],
    method: str = 'onehot',
    drop_first: bool = True
) -> pd.DataFrame:
    """
    Encode categorical variables.

    Args:
        df: Input DataFrame
        columns: List of categorical columns to encode
        method: Encoding method ('onehot', 'label', 'frequency')
        drop_first: Whether to drop first category in one-hot encoding

    Returns:
        DataFrame with encoded categorical variables

    Example:
        >>> df_encoded = encode_categorical(df, columns=['city', 'occupation'], method='onehot')
        >>> df_encoded = encode_categorical(df, columns=['education'], method='label')
    """
    df = df.copy()

    if method == 'onehot':
        df = pd.get_dummies(df, columns=columns, drop_first=drop_first)

    elif method == 'label':
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        for col in columns:
            df[col] = le.fit_transform(df[col])

    elif method == 'frequency':
        for col in columns:
            freq_encoding = df[col].value_counts(normalize=True).to_dict()
            df[f'{col}_freq'] = df[col].map(freq_encoding)
            df = df.drop(columns=[col])

    else:
        raise ValueError(f"Unsupported method: {method}")

    return df
