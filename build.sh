#!/usr/bin/env bash

# Our render.com build script.

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py makemigrations
python manage.py runserver