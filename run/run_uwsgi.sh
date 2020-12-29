#!/bin/bash

python manage.py migrate

uwsgi --ini /code/run/uwsgi.ini