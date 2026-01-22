#!/usr/bin/env bash
pip install -r requirements.txt
python -m django startproject config .
python manage.py migrate
python manage.py collectstatic --noinput
