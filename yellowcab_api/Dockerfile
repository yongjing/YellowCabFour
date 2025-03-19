# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

COPY pyproject.toml .

# Install dependencies
RUN poetry install --no-root

# Copy application code
COPY src/ src/
COPY models/ models/
COPY README.md .

# Install the package
RUN pip install .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the API
CMD ["sh", "-c", "uvicorn yellowcab_api.app:api --host 0.0.0.0 --port ${PORT:-8080}"]