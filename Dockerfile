FROM ubuntu:14.04

# APT requirements
RUN apt-get update -y
RUN apt-get install -y build-essential python python-dev python-setuptools libpq-dev libjpeg-dev libtiff-dev zlib1g-dev libfreetype6-dev liblcms2-dev
RUN easy_install -U pip

# PIP requirements
ADD docker/requirements.txt docker-requirements.txt
RUN pip install -r docker-requirements.txt

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Project source code
ADD {{ project_name }}/ /usr/local/app/

# Docker configuration
ADD docker/uwsgi.ini /usr/local/app/uwsgi.ini
ADD docker/settings/ /usr/local/app/{{ project_name }}/settings/
ADD docker/bin/ /usr/local/bin/

# Static files
# Note: we need to create a temporary database in order for "dj compress" to work
ENV DJANGO_SETTINGS_MODULE {{ project_name }}.settings.dockerbuild
RUN dj migrate --noinput > /dev/null
RUN dj collectstatic --noinput
RUN dj compress
RUN find /usr/local/static -type f -not -name '*.gz' -exec sh -c 'gzip -9c "{}" > "{}.gz"' \;

ENV DJANGO_SETTINGS_MODULE {{ project_name }}.settings.production

VOLUME /usr/local/media/
WORKDIR /usr/local/app
CMD uwsgi --ini uwsgi.ini
EXPOSE 80
