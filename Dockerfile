# Multi-stage build for optimized Django application with Channels support
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=ems.settings

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    postgresql-client \
    libpq-dev \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy all application code
COPY --chown=appuser:appuser . .

# Remove virtual environment directories if they were copied
RUN rm -rf /app/venv /app/env /app/ENV /app/.venv /app/ems/Lib /app/ems/Scripts /app/ems/Include /app/ems/pyvenv.cfg

# Create startup script with database wait logic
RUN echo '#!/bin/sh\n\
echo "Waiting for PostgreSQL..."\n\
\n\
# Wait for database to be ready\n\
max_attempts=30\n\
attempt=0\n\
\n\
while [ $attempt -lt $max_attempts ]; do\n\
  if [ -z "$POSTGRES_HOST" ]; then\n\
    echo "ERROR: POSTGRES_HOST environment variable is not set!"\n\
    echo "Please set all required database environment variables in Railway:"\n\
    echo "  - POSTGRES_HOST"\n\
    echo "  - POSTGRES_PORT"\n\
    echo "  - POSTGRES_DB"\n\
    echo "  - POSTGRES_USER"\n\
    echo "  - POSTGRES_PASSWORD"\n\
    exit 1\n\
  fi\n\
  \n\
  echo "Attempt $((attempt+1))/$max_attempts: Checking database connection to $POSTGRES_HOST:${POSTGRES_PORT:-5432}..."\n\
  \n\
  if nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}" 2>/dev/null; then\n\
    echo "Database is ready!"\n\
    break\n\
  fi\n\
  \n\
  attempt=$((attempt+1))\n\
  if [ $attempt -lt $max_attempts ]; then\n\
    echo "Database not ready yet, waiting 2 seconds..."\n\
    sleep 2\n\
  else\n\
    echo "ERROR: Could not connect to database after $max_attempts attempts"\n\
    echo "Database: $POSTGRES_HOST:${POSTGRES_PORT:-5432}"\n\
    exit 1\n\
  fi\n\
done\n\
\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
\n\
echo "Starting Daphne server on port ${PORT:-8000}..."\n\
exec daphne -b 0.0.0.0 -p ${PORT:-8000} ems.asgi:application\n\
' > /app/start.sh && chmod +x /app/start.sh

# Create necessary directories and set permissions
RUN mkdir -p /app/media /app/staticfiles && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

# Switch to non-root user
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput --clear || echo "Static files collection skipped"

# Expose port (Railway will set PORT env variable)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Run startup script
CMD ["/app/start.sh"]
