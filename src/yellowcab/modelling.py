from typing import List

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.base import BaseEstimator
from sklearn.feature_extraction import DictVectorizer

from yellowcab.models import InputData
from yellowcab.preprocessing import CATEGORICAL_COLS, encode_categorical_cols


def run_inference(payload: List[InputData], dv: DictVectorizer, model: BaseEstimator) -> np.ndarray:
    """Run inference on a list of input data.

    Args:
        payload (dict): the data point to run inference on.
        dv (DictVectorizer): the fitted DictVectorizer object.
        model (BaseEstimator): the fitted model object.

    Returns:
        np.ndarray: the predicted trip durations in minutes.

    Example payload:
        {'PULocationID': 264, 'DOLocationID': 264, 'passenger_count': 1}
    """
    logger.info(f"Running inference on:\n{payload}")
    df = pd.DataFrame([x.model_dump() for x in payload])
    df = encode_categorical_cols(df)
    dicts = df[CATEGORICAL_COLS].to_dict(orient="records")
    X = dv.transform(dicts)
    logger.info(f"Transformed input data:\n{X}")
    y = model.predict(X)
    logger.info(f"Predicted trip durations:\n{y}")
    return y
