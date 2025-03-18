import pickle
import os

class ModelService:
    # Define constants for model and vectorizer paths
    # Paths are relative to the location of this file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODEL_PATH = os.path.join(BASE_DIR, "src", "models", "dict_vectorizer.pkl")
    VECTORIZER_PATH = os.path.join(BASE_DIR, "src", "models", "forest_model.pkl")

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self._load_model()

    def _load_model(self):
        with open(self.MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)
        with open(self.VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)

    def predict(self, pu_location_id, do_location_id, passenger_count):
        features = {
            'PULocationID': str(pu_location_id),
            'DOLocationID': str(do_location_id),
            'passenger_count': str(passenger_count)
        }
        
        X = self.vectorizer.transform([features])
        prediction = self.model.predict(X)[0]
        
        return prediction 