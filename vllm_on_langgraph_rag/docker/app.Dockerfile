FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env.example ./.env.example
COPY app/run.py ./app/run.py

ENV PYTHONUNBUFFERED=1

# Default entrypoint just runs the example pipeline once.
# For a long-running API you'd swap this to uvicorn/flask/etc.
CMD ["python", "-m", "app.run"]
