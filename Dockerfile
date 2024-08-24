# Dockerfile
FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . /usr/src/app
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean
RUN pip install python-multipart

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client



CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
