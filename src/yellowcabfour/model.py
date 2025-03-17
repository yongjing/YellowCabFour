"""Model training and evaluation functions."""

from sklearn.ensemble import RandomForestRegressor
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.metrics import mean_squared_error

def train_model(X: csr_matrix, 
                y: np.ndarray,
                n_estimators: int = 50,
                random_state: int = 42,
                **kwargs) -> RandomForestRegressor:
    """Train Random Forest model."""
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        **kwargs
    )
    model.fit(X, y)
    return model

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate RMSE."""
    return np.sqrt(mean_squared_error(y_true, y_pred)) 