#!/bin/sh
source "`pipenv --venv`/bin/activate"
while true; do
    python manage.py deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy 命令失败, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app
