FROM python:3.8.3-slim
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
COPY requirements.txt /

WORKDIR /

RUN pip install -r ./requirements.txt --no-cache-dir

COPY app/ /app/

WORKDIR /app

ENV FLASK_APP=app.py
CMD flask db upgrade && flask run -h 0.0.0.0 -p 5000
