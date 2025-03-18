from flask import Flask, request, render_template, jsonify
import loguru
import requests

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from yellowcab.modelling import run_inference
from yellowcab.utils import load_model, load_preprocessor
from yellowcab.models import InputData, PredictionOut

# MODELS
MODEL_VERSION = "0.0.1"
PATH_TO_PREPROCESSOR = f"models/dv.pkl"
PATH_TO_MODEL = f"models/linear_regression.pkl"
CATEGORICAL_VARS = ["PULocationID", "DOLocationID", "passenger_count"]


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('prediction.html')
    #return "Hello World!"
@app.route("/prediction/", methods=["POST"])
def predict():
    # 获取前端输入数据
    data = request.get_json()
    PULocationID = float(data.get("PULocationID", 0))
    DOLocationID = float(data.get("DOLocationID", 0))
    passenger_count = float(data.get("passenger_count", 1))

    # 简单的预测逻辑
    trip_duration_prediction = PULocationID * 0.5 + DOLocationID * 0.3 + passenger_count * 1.2

    return jsonify({"trip_duration_prediction": round(trip_duration_prediction, 2)})

if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=5050,
        debug=True)
