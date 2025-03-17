"""Training pipeline."""

import mlflow
from mlflow.models.signature import infer_signature
from sklearn.feature_extraction import DictVectorizer
import logging
from typing import Tuple, Dict, Any

from yellowcab.data import load_data, prepare_data
from yellowcab.model import train_model, evaluate_model
from yellowcab.predict import predict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_flow(
    train_path: str,
    test_path: str,
    model_params: Dict[str, Any] = None
) -> Tuple[float, float]:
    """Full training pipeline with MLflow tracking."""
    
    if model_params is None:
        model_params = {"n_estimators": 50, "random_state": 42}

    logger.info("Loading data...")
    train_df = load_data(train_path)
    test_df = load_data(test_path)

    logger.info("Preparing training data...")
    X_train, y_train, dv = prepare_data(train_df, fit=True)
    
    logger.info("Preparing test data...")
    X_test, y_test, _ = prepare_data(test_df, dv=dv)

    with mlflow.start_run() as run:
        logger.info("Training model...")
        model = train_model(X_train, y_train, **model_params)
        
        # Get predictions
        train_pred = predict(model, X_train)
        test_pred = predict(model, X_test)
        
        # Calculate metrics
        train_rmse = evaluate_model(y_train, train_pred)
        test_rmse = evaluate_model(y_test, test_pred)
        
        logger.info(f"Train RMSE: {train_rmse:.2f}")
        logger.info(f"Test RMSE: {test_rmse:.2f}")

        # Log parameters and metrics
        mlflow.log_params(model_params)
        mlflow.log_metric("train_rmse", train_rmse)
        mlflow.log_metric("test_rmse", test_rmse)
        
        # Log model with signature
        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(model, "model", signature=signature)
        
        return train_rmse, test_rmse 