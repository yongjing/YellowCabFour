# YellowCab Trip Duration Prediction

This project provides tools for predicting NYC Yellow Taxi trip durations using machine learning. It consists of three main components:

- **yellowcab_api**: FastAPI service for serving predictions (includes ML model functionality)
- **yellowcab_flask**: Web interface for making predictions
- **yellowcab_streamlit**: Alternative interactive web interface

## Components

1. **Prediction Service (FastAPI)**
   - RESTful API service for model predictions
   - Handles direct API calls for trip duration predictions
   - Runs on port 8080

2. **Web Interface (Flask)**
   - User-friendly web interface
   - Connects to the prediction service
   - Provides form-based interaction
   - Runs on port 5000

3. **Streamlit Interface**
   - Alternative user-friendly web interface
   - Interactive data visualization capabilities
   - Connects to the prediction service
   - Runs on port 8501

## Setup and Installation

### Environment Setup
1. Create Python virtual environment:
```bash
pyenv virtualenv 3.10.12 yellowcab
pyenv local yellowcab
```

Note: In a production environment, each component would typically have its own virtual environment to avoid dependency conflicts. For this training context, we're using a single environment for simplicity since the risk of conflicts is minimal.

2. Install each component:
```bash
# Install API service
cd yellowcab_api
pip install -e .

# Install Flask interface
cd ../yellowcab_flask
pip install -e .

# Install Streamlit interface
cd ../yellowcab_streamlit
pip install -e .
```

3. Start the services:
   1. Start the prediction service:
      ```bash
      cd yellowcab_api
      uvicorn --host localhost --port 8080 --reload yellowcab_api.app:api
      ```
   2. Start the web interface (in a new terminal):
      ```bash
      cd yellowcab_flask
      flask --app yellowcab_flask.app run --debug
      ```
   3. Start the Streamlit interface (optional, in a new terminal):
      ```bash
      cd yellowcab_streamlit
      streamlit run src/yallowcab_streamlit/app.py
      ```

## Web Interfaces

### Flask Interface (http://localhost:5000)
- Simple form interface for entering trip details
- Visual display of prediction results
- Internally calls the FastAPI prediction service

### Streamlit Interface (http://localhost:8501)
- Interactive and dynamic user interface
- Real-time updates and visualizations
- Data exploration capabilities

## Model Details

### Feature Transformation Process
The API transforms raw input features in two steps:

1. **Input Processing**:
   - Required features:
     - `PULocationID`: Pickup location ID (integer)
     - `DOLocationID`: Dropoff location ID (integer)
     - `passenger_count`: Number of passengers (float)

2. **Feature Engineering**:
   - Uses `DictVectorizer` for categorical variable transformation
   - Converts inputs to strings to match training format
   - Creates a sparse matrix with 528 features through one-hot encoding

### Model Files
Required files in `yellowcab_api/models/`:
- `forest_model.pkl`: Trained Random Forest model
- `dict_vectorizer.pkl`: Fitted DictVectorizer

Generate these files by running `YellowCab.ipynb` (requires MLflow server).

## API Reference

### Prediction Endpoint: `/predict`

**Request Format:**
```json
{
    "PULocationID": 123,
    "DOLocationID": 456,
    "passenger_count": 1.0
}
```

**Response Format:**
```json
{
    "prediction": 15.5  // Duration in minutes
}
```

**Example cURL Request:**
```bash
curl -X POST "http://localhost:8080/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "PULocationID": 142,
           "DOLocationID": 43,
           "passenger_count": 1
         }'
```

## Project Structure
```
yellowcab_api/
├── models/
│   ├── forest_model.pkl
│   └── dict_vectorizer.pkl
├── src/
│   └── yellowcab_api/
│       ├── app.py
│       └── model.py
yellowcab_flask/
├── src/
│   └── yellowcab_flask/
│       ├── app.py
│       ├── services/
│       ├── templates/
│       └── static/
yellowcab_streamlit/
├── src/
│   └── yellowcab_streamlit/
│       └── app.py
```

## Deployment

Each component (yellowcab_api, yellowcab_flask, yellowcab_streamlit) needs to be configured and deployed separately.

### Environment Configuration
For each project directory, create a `.env` file:

1. API Service (.env in yellowcab_api/):
```bash
PORT=8080
PROJECT_ID=your-project-id        # Your GCP project ID
LOCATION=us-central1             # GCP region
REPOSITORY=artifacts-repository  # Name of your Artifact Registry repository
IMAGE=yellowcab-api
TAG=0.0.1-dev
```

2. Flask Interface (.env in yellowcab_flask/):
```bash
PORT=5000
API_URL=http://localhost:8080
PROJECT_ID=your-project-id
LOCATION=us-central1
REPOSITORY=artifacts-repository
IMAGE=yellowcab-flask
TAG=0.0.1-dev
```

3. Streamlit Interface (.env in yellowcab_streamlit/):
```bash
PORT=8501
API_URL=http://localhost:8080
PROJECT_ID=your-project-id
LOCATION=us-central1
REPOSITORY=artifacts-repository
IMAGE=yellowcab-streamlit
TAG=0.0.1-dev
```

Note: 
- Add `.env` files to `.gitignore` in each project to protect sensitive information
- Each service must have its own unique IMAGE name
- REPOSITORY should match your GCP Artifact Registry repository name

### Docker Setup

1. Configure Docker permissions (if needed):
```bash
sudo usermod -aG docker $USER
newgrp docker
```

2. Local development with Docker:
```bash
# For API service
cd yellowcab_api
make docker_build  # Build the Docker image locally
make docker_run    # Run the container locally for testing

# For Flask interface
cd ../yellowcab_flask
make docker_build
make docker_run

# For Streamlit interface
cd ../yellowcab_streamlit
make docker_build
make docker_run
```

3. Deploy to GCP:
```bash
# For API service
cd yellowcab_api
make deploy  # Builds, pushes to GCR, and deploys to Cloud Run

# For Flask interface
cd ../yellowcab_flask
make deploy

# For Streamlit interface
cd ../yellowcab_streamlit
make deploy
```

Note: Deploy the API service first, then update the API_URL in Flask and Streamlit configurations before deploying them.

## Coming Soon: Docker Compose Deployment

The above deployment instructions describe how to build, run, and deploy each service individually. In the next iteration, we'll introduce a simpler deployment process using Docker Compose, which will allow:

- Building and running all services with a single command
- Simplified environment configuration
- Automatic service discovery and networking
- Coordinated deployment of all components

Stay tuned for Docker Compose implementation details.