"""
Visualization utilities for ML projects.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc
from typing import Optional


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: Optional[list] = None,
    title: str = 'Confusion Matrix',
    figsize: tuple = (8, 6)
) -> None:
    """
    Plot confusion matrix.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        labels: Class labels
        title: Plot title
        figsize: Figure size

    Example:
        >>> plot_confusion_matrix(y_test, y_pred, labels=['Class 0', 'Class 1'])
    """
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.show()


def plot_roc_curve(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    title: str = 'ROC Curve',
    figsize: tuple = (8, 6)
) -> None:
    """
    Plot ROC curve.

    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        title: Plot title
        figsize: Figure size

    Example:
        >>> y_pred_proba = model.predict_proba(X_test)[:, 1]
        >>> plot_roc_curve(y_test, y_pred_proba)
    """
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=figsize)
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_feature_importance(
    feature_names: list,
    importances: np.ndarray,
    top_n: int = 20,
    title: str = 'Feature Importance',
    figsize: tuple = (10, 8)
) -> None:
    """
    Plot feature importance.

    Args:
        feature_names: List of feature names
        importances: Feature importance values
        top_n: Number of top features to display
        title: Plot title
        figsize: Figure size

    Example:
        >>> plot_feature_importance(
        >>>     feature_names=X_train.columns,
        >>>     importances=model.feature_importances_
        >>> )
    """
    # Create dataframe and sort
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False).head(top_n)

    # Plot
    plt.figure(figsize=figsize)
    sns.barplot(data=importance_df, x='importance', y='feature', palette='viridis')
    plt.title(title)
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()


def plot_learning_curve(
    train_scores: np.ndarray,
    val_scores: np.ndarray,
    train_sizes: np.ndarray,
    title: str = 'Learning Curve',
    figsize: tuple = (10, 6)
) -> None:
    """
    Plot learning curve.

    Args:
        train_scores: Training scores
        val_scores: Validation scores
        train_sizes: Training set sizes
        title: Plot title
        figsize: Figure size

    Example:
        >>> from sklearn.model_selection import learning_curve
        >>> train_sizes, train_scores, val_scores = learning_curve(
        >>>     model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)
        >>> )
        >>> plot_learning_curve(train_scores, val_scores, train_sizes)
    """
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    plt.figure(figsize=figsize)
    plt.plot(train_sizes, train_mean, label='Training score', marker='o')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15)
    plt.plot(train_sizes, val_mean, label='Validation score', marker='s')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.15)

    plt.xlabel('Training Set Size')
    plt.ylabel('Score')
    plt.title(title)
    plt.legend(loc='best')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
