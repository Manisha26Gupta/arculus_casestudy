# ---------- Builder stage ----------
FROM python:3.11-slim AS builder

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Create work directory
WORKDIR /app

# Copy requirements and install into a temporary folder
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt


# ---------- Final runtime stage ----------
FROM python:3.11-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy app source
COPY app.py pytest.ini .flake8 ./
COPY templates ./templates
COPY tests ./tests

RUN mkdir -p /app/instance && chown -R appuser /app/instance

# Expose port
EXPOSE 5000

# Switch to non-root user
USER appuser

# Run Gunicorn with 3 workers
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["python", "app.py"]
