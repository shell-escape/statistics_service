FROM python:3.10 AS build

WORKDIR /usr/statistic_service

RUN pip install -U pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY .env .

COPY alembic alembic
COPY alembic.ini .

ENV PYTHONPATH /usr/statistic_service

CMD alembic upgrade head && uvicorn statistic_service.app:app --host 0.0.0.0 --port 8001