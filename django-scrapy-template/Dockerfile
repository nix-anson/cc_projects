FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Install dependencies (no dev extras in container)
COPY pyproject.toml .
RUN uv sync --no-dev

# Copy project
COPY . .

# Ensure app root is on PYTHONPATH so `apps.*` and `scrapy_spiders.*` resolve
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=config.settings.development

# Default: run the web server (override in docker-compose for Celery)
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
