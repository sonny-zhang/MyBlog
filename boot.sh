#!/bin/sh
source "`pipenv --venv`/bin/activate"
python manage.py deploy
exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app
