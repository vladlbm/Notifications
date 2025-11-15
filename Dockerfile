FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


CMD ["sh", "-c", "until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do echo 'Waiting for PostgreSQL...'; sleep 2; done; uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]