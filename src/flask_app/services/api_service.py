import requests
from typing import Dict
from flask import current_app

class APIService:
    def __init__(self):
        self.api_base_url = "http://localhost:8080"

    def predict(self, 
                pu_location_id: int, 
                do_location_id: int, 
                passenger_count: float) -> Dict[str, float]:
        """
        Make prediction request to FastAPI endpoint
        """
        payload = {
            "PULocationID": pu_location_id,
            "DOLocationID": do_location_id,
            "passenger_count": passenger_count
        }
        
        response = requests.post(
            f"{self.api_base_url}/predict",
            json=payload
        )
        response.raise_for_status()
        return response.json() 