# Single-Port Production Dockerfile for Render.com Free Tier & Cloud Run
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required by Reflex frontend bundler (curl, unzip)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rxconfig.py .
COPY build_prod.py .
COPY start_prod.py .
COPY gradwyn ./gradwyn

# Pre-build the static production frontend during Docker image build (high-RAM build environment)
ENV API_URL=https://gradwyn-mvp.onrender.com
RUN python build_prod.py

EXPOSE 8080

# Start lightweight single-port ASGI server serving both .web/_static and FastAPI/WebSockets
CMD ["python", "start_prod.py"]
