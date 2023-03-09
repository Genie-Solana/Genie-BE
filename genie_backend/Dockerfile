FROM python:3.8-slim-buster as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install libpq-dev gcc nginx supervisor libpython3-dev build-essential\
  && pip install psycopg2

WORKDIR /app
ADD ./requirement.txt /app
ADD ./.env /app
RUN pip install -r requirement.txt
ADD . /app/

USER root

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY ./config/nginx/nginx.conf /etc/nginx/sites-available/default
COPY ./config/supervisor/supervisor.conf /etc/supervisor/conf.d/

EXPOSE 80
EXPOSE 433

RUN python manage.py collectstatic --no-input

VOLUME ["/app/static"]