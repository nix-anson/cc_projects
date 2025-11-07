"""
Model training utilities.
"""

from sklearn.model_selection import cross_val_score, GridSearchCV
from typing import Any, Dict, Optional
import pandas as pd


def train_with_cross_validation(
    model: Any,
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5,
    scoring: str = 'accuracy'
) -> Dict[str, float]:
    """
    Train model with cross-validation.

    Args:
        model: Scikit-learn compatible model
        X: Feature matrix
        y: Target vector
        cv: Number of cross-validation folds
        scoring: Scoring metric

    Returns:
        Dictionary with mean and std of CV scores

    Example:
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> model = RandomForestClassifier()
        >>> results = train_with_cross_validation(model, X_train, y_train)
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)

    return {
        'mean_score': scores.mean(),
        'std_score': scores.std(),
        'scores': scores.tolist()
    }


def hyperparameter_tuning(
    model: Any,
    X: pd.DataFrame,
    y: pd.Series,
    param_grid: Dict,
    cv: int = 5,
    scoring: str = 'accuracy',
    n_jobs: int = -1
) -> tuple:
    """
    Perform hyperparameter tuning with GridSearchCV.

    Args:
        model: Scikit-learn compatible model
        X: Feature matrix
        y: Target vector
        param_grid: Dictionary of parameters to search
        cv: Number of cross-validation folds
        scoring: Scoring metric
        n_jobs: Number of parallel jobs

    Returns:
        Tuple of (best_model, best_params, best_score)

    Example:
        >>> param_grid = {'n_estimators': [100, 200], 'max_depth': [10, 20]}
        >>> best_model, best_params, best_score = hyperparameter_tuning(
        >>>     RandomForestClassifier(), X_train, y_train, param_grid
        >>> )
    """
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv,
        scoring=scoring,
        n_jobs=n_jobs,
        verbose=1
    )

    grid_search.fit(X, y)

    return (
        grid_search.best_estimator_,
        grid_search.best_params_,
        grid_search.best_score_
    )
