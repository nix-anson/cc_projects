"""
General utility functions.
"""

import random
import numpy as np
import pandas as pd
from typing import Any, Dict


def set_seed(seed: int = 42) -> None:
    """
    Set random seed for reproducibility.

    Args:
        seed: Random seed value

    Example:
        >>> set_seed(42)
    """
    random.seed(seed)
    np.random.seed(seed)

    # Set seeds for ML libraries if available
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass

    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass


def print_dataframe_info(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """
    Print comprehensive information about a DataFrame.

    Args:
        df: DataFrame to analyze
        name: Name to display

    Example:
        >>> print_dataframe_info(df, "Training Data")
    """
    print(f"\n{'='*60}")
    print(f"{name} Information")
    print(f"{'='*60}")

    print(f"\nShape: {df.shape}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    print(f"\nColumn Types:")
    print(df.dtypes)

    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        missing_pct = 100 * missing / len(df)
        missing_df = pd.DataFrame({
            'Missing_Values': missing,
            'Percentage': missing_pct
        }).sort_values('Percentage', ascending=False)
        print(missing_df[missing_df['Percentage'] > 0])
    else:
        print("No missing values")

    print(f"\nDuplicate Rows: {df.duplicated().sum()}")

    print(f"\nNumeric Summary:")
    print(df.describe())


def save_model_metadata(
    model: Any,
    metadata: Dict[str, Any],
    file_path: str
) -> None:
    """
    Save model with metadata.

    Args:
        model: Trained model object
        metadata: Dictionary of metadata
        file_path: Path to save model and metadata

    Example:
        >>> metadata = {
        >>>     'model_type': 'RandomForest',
        >>>     'features': feature_names,
        >>>     'accuracy': 0.95
        >>> }
        >>> save_model_metadata(model, metadata, 'models/model.pkl')
    """
    import joblib
    from datetime import datetime

    model_data = {
        'model': model,
        'metadata': metadata,
        'saved_at': datetime.now().isoformat()
    }

    joblib.dump(model_data, file_path)
    print(f"Model saved to: {file_path}")


def load_model_with_metadata(file_path: str) -> tuple:
    """
    Load model and metadata.

    Args:
        file_path: Path to saved model

    Returns:
        Tuple of (model, metadata)

    Example:
        >>> model, metadata = load_model_with_metadata('models/model.pkl')
        >>> print(metadata['accuracy'])
    """
    import joblib

    model_data = joblib.load(file_path)
    return model_data['model'], model_data.get('metadata', {})
