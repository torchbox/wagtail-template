#!/bin/bash

PROJECT_NAME=$1

PROJECT_DIR=/vagrant
DJANGO_DIR=$PROJECT_DIR/$PROJECT_NAME
VIRTUALENV_DIR=/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


# Create database
su - vagrant -c "createdb $PROJECT_NAME"


# Virtualenv setup for project
su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR"
su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"
su - vagrant -c "$PIP install -r $PROJECT_DIR/requirements.txt"


# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $DJANGO_DIR/manage.py


# Run syncdb/migrate/update_index
su - vagrant -c "$PYTHON $DJANGO_DIR/manage.py migrate --noinput && \
                 $PYTHON $DJANGO_DIR/manage.py update_index"


# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
alias dj="$PYTHON $DJANGO_DIR/manage.py"
alias djrun="dj runserver 0.0.0.0:8000"

source $VIRTUALENV_DIR/bin/activate
cd $PROJECT_DIR
EOF
