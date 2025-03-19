import os
from flask import Flask
from flask import request, jsonify, render_template
from yellowcab_flask.services.api_service import APIService
import loguru

api_service = APIService()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    port = int(os.environ.get("PORT", 5000))
    loguru.logger.info(f"Starting Flask app on port {port}")
    debug = os.environ.get("DEBUG", False)
    app.run(host='0.0.0.0', port=port, debug=debug) 