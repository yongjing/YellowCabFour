from .app_config import (
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    MODEL_VERSION,
    PATH_TO_MODEL,
    PATH_TO_PREPROCESSOR,
)
from fastapi import FastAPI

from yellowcab.modelling import run_inference
from yellowcab.utils import load_model, load_preprocessor
from yellowcab.models import InputData, PredictionOut

app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION)


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": MODEL_VERSION}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(payload: InputData):
    print(payload)
    dv = load_preprocessor(PATH_TO_PREPROCESSOR)
    model = load_model(PATH_TO_MODEL)
    y = run_inference([payload], dv, model)
    return {"trip_duration_prediction": y[0]}
