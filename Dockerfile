FROM python:3.9.5-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps


COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .

RUN python manage.py collectstatic --noinput

RUN adduser -D serega
USER serega

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
