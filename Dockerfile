FROM kaedroho/django-base

# PIP requirements
ADD docker/requirements.txt docker-requirements.txt
RUN pip install -r docker-requirements.txt

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Project source code
ADD {{ project_name }}/ /usr/local/app/

# Docker configuration
ADD docker/uwsgi.ini /usr/local/app/uwsgi.ini
ADD docker/local.py /usr/local/app/{{ project_name }}/settings/local.py
ADD docker/wsgi_docker.py /usr/local/app/my_lovely_website/wsgi_docker.py

ENV PYTHONPATH /usr/local/app
ENV DJANGO_SETTINGS_MODULE my_lovely_website.settings.production

# Static files
# Note: we need to create a temporary database in order for "dj compress" to work
RUN DATABASE_URL=sqlite:///tmp/db.sqlite SECRET_KEY=build django-admin migrate --noinput > /dev/null
RUN DATABASE_URL=sqlite:///tmp/db.sqlite SECRET_KEY=build django-admin collectstatic --noinput
RUN DATABASE_URL=sqlite:///tmp/db.sqlite SECRET_KEY=build django-admin compress
RUN python -m whitenoise.gzip /usr/local/static/

VOLUME /usr/local/media/
WORKDIR /usr/local/app
CMD uwsgi --ini uwsgi.ini
EXPOSE 80
