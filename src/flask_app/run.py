from flask import Flask
from flask import request, jsonify, render_template
from flask_app.services.model_service import ModelService
from flask_app.services.api_service import APIService

model_service = ModelService()
api_service = APIService()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/local-predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        prediction = model_service.predict(
            data['PULocationID'],
            data['DOLocationID'],
            data['passenger_count']
        )
        return jsonify({'prediction': float(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()
        result = api_service.predict(
            data['PULocationID'],
            data['DOLocationID'],
            data['passenger_count']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400 
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 