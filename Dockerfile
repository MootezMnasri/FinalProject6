# ── Stage 1: Test ──────────────────────────────────────────
FROM python:3.11-slim AS test

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest

COPY . .
RUN python -m pytest tests/ -v --tb=short

# ── Stage 2: Production ───────────────────────────────────
FROM python:3.11-slim AS production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Run with gunicorn for production-ready serving
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
