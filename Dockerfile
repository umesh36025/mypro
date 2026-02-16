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

# Expose port
EXPOSE 8000

# Start command
CMD python manage.py migrate --noinput && \
    daphne -b 0.0.0.0 -p 8000 ems.asgi:application
