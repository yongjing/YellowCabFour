import streamlit as st
import requests
import json
from loguru import logger

def main():
    st.title("NYC Taxi Trip Duration Predictor")
    
    # Add inputs in the sidebar
    st.sidebar.header("Trip Information")
    
    # Input fields
    pickup_id = st.sidebar.number_input(
        "Pickup Location ID",
        min_value=1,
        max_value=1000000000,
        value=100
    )
    
    dropoff_id = st.sidebar.number_input(
        "Dropoff Location ID",
        min_value=1,
        max_value=1000000000,
        value=100
    )
    
    passengers = st.sidebar.number_input(
        "Number of Passengers",
        min_value=1,
        max_value=8,
        value=1
    )
    
    # Predict button
    if st.sidebar.button("Predict Duration"):
        # Prepare the data
        data = {
            "PULocationID": pickup_id,
            "DOLocationID": dropoff_id,
            "passenger_count": float(passengers)
        }
        
        try:
            # Make prediction request to FastAPI endpoint
            response = requests.post(
                "http://localhost:8080/predict",
                json=data
            )
            
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                
                # Display results
                st.success("Prediction successful!")
                st.header("Predicted Trip Duration")
                st.write(f"The predicted trip duration is {prediction:.2f} minutes")
                
                # Add some visual context
                if prediction < 10:
                    st.info("This is a short trip! 🚕")
                elif prediction < 20:
                    st.info("This is a medium-length trip! 🚖")
                else:
                    st.info("This is a long trip! 🚗")
            else:
                st.error("Error getting prediction from the API")
                
        except requests.exceptions.ConnectionError as e:
            logger.error("Could not connect to the API. Make sure the FastAPI server is running.", e)
            st.error("Could not connect to the API. Make sure the FastAPI server is running.")

if __name__ == "__main__":
    main() 