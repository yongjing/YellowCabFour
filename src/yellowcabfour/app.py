import pickle
from fastapi import FastAPI, HTTPException
import pandas as pd
from yellowcabfour.schemas import TripFeatures, PredictionResponse
from yellowcabfour.data import YellowCabData

# Initialize FastAPI app
app = FastAPI(title="Yellow Cab Trip Duration Predictor")

# Initialize data handler
data_handler = YellowCabData()

# Load the trained model
try:
    with open("models/forest_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("Model file not found. Please ensure the model is trained and saved.")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Yellow Cab Trip Duration Prediction API"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(features: TripFeatures):
    """Predict trip duration
    
    Args:
        features: Input features for the prediction
        
    Returns:
        Prediction response with estimated trip duration
    """
    try:
        # Convert input features to DataFrame
        df = pd.DataFrame([features.dict()])
        
        # Prepare features using data handler
        X, _ = data_handler.prepare_data(df, fit_dv=False)
        
        # Make prediction
        prediction = model.predict(X)[0]
        
        return PredictionResponse(
            duration_prediction=float(prediction),
            pickup_location=features.PULocationID,
            dropoff_location=features.DOLocationID,
            passenger_count=features.passenger_count,
            trip_distance=features.trip_distance,
            fare_amount=features.fare_amount,
            total_amount=features.total_amount
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 