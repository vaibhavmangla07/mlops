FROM python:3.9-slim

WORKDIR /app

# Install dependencies first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY run.py config.yaml data.csv ./
COPY src/ ./src/

# Run pipeline, capture exit code, print metrics to stdout, then exit with original code
CMD python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log; \
    EXIT_CODE=$?; \
    cat metrics.json; \
    exit $EXIT_CODE
