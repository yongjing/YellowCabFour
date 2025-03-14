from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import os

api = FastAPI()

class TripInput(BaseModel):
    passenger_count: float
    trip_distance: float
    fare_amount: float
    total_amount: float
    # Add any other required fields for your model

@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.post("/predict")
async def predict(trip_input: TripInput):
    # Load the model
    model_path = os.path.join(os.path.dirname(__file__), "src", "models", "forest_model.pkl")
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    print(model.predict.__doc__)

    # Convert input to numpy array
    features = np.array([[
        trip_input.passenger_count,
        trip_input.trip_distance,
        trip_input.fare_amount,
        trip_input.total_amount
        # Add other features in the same order as your model expects
    ]])
    
    # Make prediction
    prediction = model.predict(features)
    
    return {"prediction": int(prediction[0])}



