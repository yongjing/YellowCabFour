"""Prediction functions."""

from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def predict(model: RandomForestRegressor, X: csr_matrix) -> np.ndarray:
    """Make predictions using trained model."""
    return model.predict(X) 