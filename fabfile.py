from fabric.api import *


env.roledefs = {
    'staging': [],
    'production': [],
}


@roles('staging')
def deploy_staging():
    # Remove this line when you're happy that this Fabfile is correct
    raise RuntimeError("Please check the fabfile before using it")

    base_dir = '/usr/local/django/{{ project_name }}wagtail/'
    virtualenv_dir = '/usr/local/django/virtualenvs/{{ project_name }}wagtail/'
    python = virtualenv_dir + '/bin/python'
    pip = virtualenv_dir + '/bin/pip'

    with cd(base_dir):
        run('git pull origin master')
        run(pip + ' install -r requirements.txt')
        run(python + ' manage.py migrate --settings={{ project_name }}.settings.production --noinput')
        run(python + ' manage.py collectstatic --settings={{ project_name }}.settings.production --noinput')
        run(python + ' manage.py compress --settings={{ project_name }}.settings.production')
        run(python + ' manage.py update_index --settings={{ project_name }}.settings.production')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')


@roles('production')
def deploy_production():
    # Remove this line when you're happy that this Fabfile is correct
    raise RuntimeError("Please check the fabfile before using it")

    base_dir = '/usr/local/django/{{ project_name }}wagtail/'
    virtualenv_dir = '/usr/local/django/virtualenvs/{{ project_name }}wagtail/'
    python = virtualenv_dir + '/bin/python'
    pip = virtualenv_dir + '/bin/pip'

    with cd(base_dir):
        run('git pull origin master')
        run(pip + ' install -r requirements.txt')
        run(python + ' manage.py migrate --settings={{ project_name }}.settings.production --noinput')
        run(python + ' manage.py collectstatic --settings={{ project_name }}.settings.production --noinput')
        run(python + ' manage.py compress --settings={{ project_name }}.settings.production')
        run(python + ' manage.py update_index --settings={{ project_name }}.settings.production')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')
