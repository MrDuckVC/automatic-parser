FROM python:3.8.10-alpine3.12

RUN mkdir /var/run/python/

# Root bin to PATH:
ENV PATH=$PATH:/root/.local/bin

# Python site-packages to PYTHONPATH:
ENV PYTHONPATH=/root/.local/lib/python3.8/site-packages:/usr/local/lib/python3.8/site-packages

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Tell uWSGI -> where to find your wsgi file <- and -> number of uWSGI workers and threads per worker <-:
ENV UWSGI_WSGI_FILE=main/wsgi.py UWSGI_WORKERS=1 UWSGI_THREADS=1

RUN apk update && apk add --no-cache --virtual build-deps gcc python3-dev musl-dev libffi-dev \
    && apk add --no-cache uwsgi-python3 mariadb-dev jpeg-dev freetype-dev libpng logrotate \
    && pip3 install --upgrade pip

RUN pip3 install --user --no-cache-dir --no-warn-script-location \
    'Django==3.2.6,<4.0' \
    'django-mysql>=3.8.1' \
    'mysqlclient>=2.0.1' \
    'requests>=2.24.0' \
    'celery==4.4.7' \
    'redis>=3.5.3' \
    'selenium<=4.0.0' \
    'openpyxl==3.0.9' \
    'dload==0.6'
WORKDIR /var/www/backend

COPY ./docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]