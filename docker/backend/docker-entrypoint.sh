#!/bin/sh

if [ "$*" = "" ]; then
  exec uwsgi --master \
    --processes=4 \
    --attach-daemon='celery worker --app=main --concurrency=3 --loglevel=info --logfile=/dev/stderr' \
    --attach-daemon='celery beat --app=main --loglevel=info --logfile=/dev/stderr --schedule=/var/www/celery/schedule.db' \
    --socket /var/run/python/uwsgi.sock \
    --plugins python3 \
    --protocol uwsgi \
    --chmod-socket=666 \
    --die-on-term
else
  exec "$@"
fi
