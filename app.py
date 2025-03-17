from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import os
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
from typing import List

api = FastAPI()

class TripInput(BaseModel):
    PULocationID: int
    DOLocationID: int
    passenger_count: float

    class Config:
        # This will allow extra fields to be sent without validation errors
        extra = "allow"

def extract_x_y(
    df: pd.DataFrame,
    categorical_cols: List[str] = None,
    dv: DictVectorizer = None,
    with_target: bool = True,
) -> dict:
    if categorical_cols is None:
        categorical_cols = ["PULocationID", "DOLocationID", "passenger_count"]
    dicts = df[categorical_cols].to_dict(orient="records")

    y = None
    if with_target:
        if dv is None:
            dv = DictVectorizer()
            dv.fit(dicts)
        y = df["duration"].values

    x = dv.transform(dicts)
    return x, y, dv

@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.post("/predict")
async def predict(trip_input: TripInput):
    # Convert input to DataFrame
    input_df = pd.DataFrame([{
        "PULocationID": str(trip_input.PULocationID),
        "DOLocationID": str(trip_input.DOLocationID),
        "passenger_count": str(trip_input.passenger_count)
    }])
    
    # Load the DictVectorizer
    dv_path = os.path.join(os.path.dirname(__file__), "src", "models", "dict_vectorizer.pkl")
    with open(dv_path, 'rb') as dv_file:
        dv = pickle.load(dv_file)
    
    # Load the model
    model_path = os.path.join(os.path.dirname(__file__), "src", "models", "forest_model.pkl")
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    
    # Transform features using extract_x_y with the loaded DictVectorizer
    transformed_features, _, _ = extract_x_y(input_df, dv=dv, with_target=False)
    
    prediction = model.predict(transformed_features)
    
    return {"prediction": float(prediction[0])}



