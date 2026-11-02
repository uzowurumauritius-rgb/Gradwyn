# Single-Port Production Dockerfile for Render.com Free Tier & Cloud Run
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies + Caddy for single-port reverse proxying (Frontend :3000 + Backend :8000 -> $PORT)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    ca-certificates \
    caddy \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rxconfig.py .
COPY Caddyfile .
COPY gradwyn ./gradwyn

# Pre-initialize the Reflex frontend workspace
RUN reflex init

EXPOSE 8080

# Start Caddy on $PORT (default 8080) and run Reflex in production mode
CMD ["sh", "-c", "caddy start --config /app/Caddyfile && reflex run --env prod --frontend-port 3000 --backend-port 8000"]
