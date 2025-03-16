# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project configuration and install dependencies
COPY pyproject.toml .
# Copy source code and model files
COPY src/ src/
COPY app.py .
COPY README.md .
RUN pip install .


# Expose the port the app runs on
EXPOSE 8080

# Command to run the API
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8080"] 