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
COPY README.md .

# Install the package
RUN pip install .

# Create entrypoint script
RUN echo '#!/bin/bash\n\
flask --app yellowcab_flask.app run --host 0.0.0.0 --port ${PORT}' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE ${PORT}

# Command to run the API
ENTRYPOINT ["/entrypoint.sh"]