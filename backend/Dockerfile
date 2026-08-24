# Agent OS Backend Dockerfile

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user and give it ownership of the application directory.
RUN groupadd -r appuser \
    && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && chown -R appuser:appuser /app

# Install only the API runtime dependencies. Optional provider, vector-store,
# test and lint tooling stays outside the production container.
COPY requirements.runtime.txt .
RUN pip install --no-cache-dir -r requirements.runtime.txt

# Copy application code and migrations, then make the entrypoint executable.
COPY --chown=appuser:appuser . .
RUN chmod +x docker-entrypoint.sh

USER appuser

# Expose port
EXPOSE 8080

# Run migrations and start the API.
CMD ["./docker-entrypoint.sh"]
