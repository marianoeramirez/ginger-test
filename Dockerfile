FROM python:3.9-alpine3.12
ARG REQUIREMENTS

COPY requirements /tmp

RUN apk add --no-cache --virtual .build-deps \
       postgresql-dev \
       musl-dev \
   && apk add --no-cache \
        postgresql-client \
        libffi-dev \
        bash \
        zlib-dev \
        gcc \
        jpeg-dev \
        gettext \
        linux-headers \
        dbus git \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r /tmp/$REQUIREMENTS


ADD . /code
WORKDIR /code

