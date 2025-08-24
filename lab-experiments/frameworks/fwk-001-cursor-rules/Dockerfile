FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY examples/ ./examples/
COPY tests/ ./tests/

# Set Python path
ENV PYTHONPATH=/app/src

# Default command
CMD ["python", "-m", "examples.basic_usage"]
