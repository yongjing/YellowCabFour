"""Data loading and preparation functions."""

import pandas as pd
from typing import List, Tuple
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import csr_matrix
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    """Load data from parquet file."""
    return pd.read_parquet(path)

def compute_target(df: pd.DataFrame,
                  pickup_column: str = "tpep_pickup_datetime",
                  dropoff_column: str = "tpep_dropoff_datetime") -> pd.DataFrame:
    """Compute trip duration in minutes."""
    df["duration"] = df[dropoff_column] - df[pickup_column]
    df["duration"] = df["duration"].dt.total_seconds() / 60
    return df

def filter_outliers(df: pd.DataFrame, 
                   min_duration: float = 1,
                   max_duration: float = 60) -> pd.DataFrame:
    """Filter duration outliers."""
    return df[(df.duration >= min_duration) & (df.duration <= max_duration)]

def encode_categorical_cols(df: pd.DataFrame, 
                          categorical_cols: List[str] = None) -> pd.DataFrame:
    """Encode categorical columns."""
    if categorical_cols is None:
        categorical_cols = ["PULocationID", "DOLocationID", "passenger_count"]
    df[categorical_cols] = df[categorical_cols].fillna(-1).astype("int")
    df[categorical_cols] = df[categorical_cols].astype("str")
    return df

def extract_features(df: pd.DataFrame,
                    categorical_cols: List[str] = None,
                    dv: DictVectorizer = None,
                    fit: bool = False) -> Tuple[csr_matrix, np.ndarray, DictVectorizer]:
    """Extract features and target from dataframe."""
    if categorical_cols is None:
        categorical_cols = ["PULocationID", "DOLocationID", "passenger_count"]
        
    dicts = df[categorical_cols].to_dict(orient="records")
    
    if fit:
        if dv is None:
            dv = DictVectorizer()
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
        
    y = df["duration"].values if "duration" in df.columns else None
    
    return X, y, dv

def prepare_data(df: pd.DataFrame, 
                dv: DictVectorizer = None,
                fit: bool = False) -> Tuple[csr_matrix, np.ndarray, DictVectorizer]:
    """Prepare data for training/prediction."""
    df = compute_target(df)
    df = filter_outliers(df)
    df = encode_categorical_cols(df)
    return extract_features(df, dv=dv, fit=fit) 