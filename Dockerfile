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

# Startup script
CMD sh -c "python manage.py migrate --noinput && daphne -b 0.0.0.0 -p ${PORT:-8000} ems.asgi:application"
