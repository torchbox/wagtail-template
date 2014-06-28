from fabric.api import *


env.roledefs = {
    'app': [],
}


@roles('app')
def deploy():
    base_dir = '/usr/local/django/{{ project_name }}'
    virtualenv_dir = '/usr/local/django/virtualenvs/{{ project_name }}'
    python = virtualenv_dir + '/bin/python'
    pip = virtualenv_dir + '/bin/pip'

    user = '{{ project_name }}'
    supervisor_task = '{{ project_name }}'

    with cd(base_dir):
        with settings(sudo_user=user):
            sudo('git pull origin master')
            sudo(pip + ' install -r requirements/production.txt')
            sudo(python + ' manage.py syncdb --settings={{ project_name }}.settings.production --noinput')
            sudo(python + ' manage.py migrate --settings={{ project_name }}.settings.production --noinput')
            sudo(python + ' manage.py collectstatic --settings={{ project_name }}.settings.production --noinput')
            sudo(python + ' manage.py compress --settings={{ project_name }}.settings.production')
            sudo(python + ' manage.py update_index --settings={{ project_name }}.settings.production')

    sudo('supervisorctl restart ' + supervisor_task)
