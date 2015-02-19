FROM kaedroho/django-base

# PIP requirements
ADD docker/requirements.txt docker-requirements.txt
RUN pip3 install -r docker-requirements.txt

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Project source code
ADD {{ project_name }}/ /app/

# Docker configuration
ADD docker/uwsgi.ini /app/uwsgi.ini
ADD docker/local.py /app/{{ project_name }}/settings/local.py
ADD docker/wsgi_docker.py /app/my_lovely_website/wsgi_docker.py

ENV PYTHONPATH /app/
ENV DJANGO_SETTINGS_MODULE my_lovely_website.settings.production

# Static files
# Note: we need to create a temporary database in order for "dj compress" to work
RUN DATABASE_URL=sqlite:///tmp/db.sqlite SECRET_KEY=build django-admin migrate --noinput > /dev/null
RUN DATABASE_URL=sqlite:///tmp/db.sqlite SECRET_KEY=build django-admin collectstatic --noinput
RUN DATABASE_URL=sqlite:///tmp/db.sqlite SECRET_KEY=build django-admin compress
RUN python3 -m whitenoise.gzip /static/

VOLUME /media/
WORKDIR /app/
CMD uwsgi --ini uwsgi.ini
EXPOSE 80
