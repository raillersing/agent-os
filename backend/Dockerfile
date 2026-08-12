# Agent OS Backend Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Install only the API runtime dependencies. Optional provider, vector-store,
# test and lint tooling stays outside the production container.
COPY requirements.runtime.txt .
RUN pip install --no-cache-dir -r requirements.runtime.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
