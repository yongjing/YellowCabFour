from datetime import datetime
from pydantic import BaseModel, Field

class TripFeatures(BaseModel):
    """Input features for trip duration prediction"""
    PULocationID: int = Field(..., description="Pickup location ID")
    DOLocationID: int = Field(..., description="Dropoff location ID")
    passenger_count: int = Field(..., ge=0, description="Number of passengers")
    tpep_pickup_datetime: datetime = Field(..., description="Pickup datetime")
    tpep_dropoff_datetime: datetime = Field(..., description="Dropoff datetime")
    trip_distance: float = Field(..., ge=0.0, description="Trip distance in miles")
    fare_amount: float = Field(..., ge=0.0, description="Base fare amount")
    total_amount: float = Field(..., ge=0.0, description="Total fare amount including taxes and fees")

    class Config:
        json_schema_extra = {
            "example": {
                "PULocationID": 142,
                "DOLocationID": 43,
                "passenger_count": 1,
                "tpep_pickup_datetime": "2021-01-01T00:30:10",
                "tpep_dropoff_datetime": "2021-01-01T00:36:12",
                "trip_distance": 2.10,
                "fare_amount": 8.0,
                "total_amount": 11.80
            }
        }

class PredictionResponse(BaseModel):
    """Response model for trip duration prediction"""
    duration_prediction: float = Field(..., description="Predicted trip duration in minutes")
    pickup_location: int = Field(..., description="Pickup location ID used")
    dropoff_location: int = Field(..., description="Dropoff location ID used")
    passenger_count: int = Field(..., description="Number of passengers used")
    trip_distance: float = Field(..., description="Trip distance in miles")
    fare_amount: float = Field(..., description="Base fare amount")
    total_amount: float = Field(..., description="Total fare amount") 