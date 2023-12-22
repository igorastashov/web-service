FROM python:3.11-slim

RUN mkdir /web-service

WORKDIR /web-service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .. .

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
