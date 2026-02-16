# Dockerfile for Django application with Channels (WebSocket support)
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=ems.settings

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Remove virtual environment if copied
RUN rm -rf ems/Lib ems/Scripts ems/Include ems/pyvenv.cfg venv env

# Create directories
RUN mkdir -p media staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput --clear || true

# Create startup script
RUN echo '#!/bin/sh\n\
set -e\n\
\n\
echo "=== Starting Application ==="\n\
\n\
# Check required environment variables\n\
if [ -z "$POSTGRES_HOST" ]; then\n\
  echo "ERROR: POSTGRES_HOST is not set!"\n\
  echo "Please set these environment variables in Render:"\n\
  echo "  - POSTGRES_HOST"\n\
  echo "  - POSTGRES_PORT"\n\
  echo "  - POSTGRES_DB"\n\
  echo "  - POSTGRES_USER"\n\
  echo "  - POSTGRES_PASSWORD"\n\
  exit 1\n\
fi\n\
\n\
echo "Database configuration:"\n\
echo "  Host: $POSTGRES_HOST"\n\
echo "  Port: ${POSTGRES_PORT:-5432}"\n\
echo "  Database: $POSTGRES_DB"\n\
echo "  User: $POSTGRES_USER"\n\
\n\
# Wait for database\n\
echo "Waiting for database to be ready..."\n\
max_attempts=30\n\
attempt=0\n\
\n\
while [ $attempt -lt $max_attempts ]; do\n\
  attempt=$((attempt + 1))\n\
  echo "Attempt $attempt/$max_attempts: Testing connection to $POSTGRES_HOST:${POSTGRES_PORT:-5432}"\n\
  \n\
  if nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}" 2>/dev/null; then\n\
    echo "✓ Database is reachable!"\n\
    break\n\
  fi\n\
  \n\
  if [ $attempt -eq $max_attempts ]; then\n\
    echo "ERROR: Cannot connect to database after $max_attempts attempts"\n\
    echo "Please verify:"\n\
    echo "  1. Database is running"\n\
    echo "  2. POSTGRES_HOST and POSTGRES_PORT are correct"\n\
    echo "  3. Network connectivity between services"\n\
    exit 1\n\
  fi\n\
  \n\
  echo "Database not ready, waiting 2 seconds..."\n\
  sleep 2\n\
done\n\
\n\
# Run migrations\n\
echo "Running database migrations..."\n\
python manage.py migrate --noinput\n\
\n\
if [ $? -ne 0 ]; then\n\
  echo "ERROR: Migration failed!"\n\
  exit 1\n\
fi\n\
\n\
echo "✓ Migrations completed successfully"\n\
\n\
# Start server\n\
echo "Starting Daphne server on port 8000..."\n\
exec daphne -b 0.0.0.0 -p 8000 ems.asgi:application\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Start command
CMD ["/app/start.sh"]
