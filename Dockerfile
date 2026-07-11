FROM python:3.14-slim

WORKDIR /app


ENV PYTHONDONTWRITEBYCODE=1

ENV PYTHONNUNBUFFERED=1

#system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#COPY requirements
COPY requirements.txt .

#dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000