from fabric.api import *


env.roledefs = {
    'production': [],
    'staging': [],
    'testing': [],
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
        run(python + ' {{ project_name }}/manage.py migrate --settings={{ project_name }}.settings.production --noinput')
        run(python + ' {{ project_name }}/manage.py collectstatic --settings={{ project_name }}.settings.production --noinput')
        run(python + ' {{ project_name }}/manage.py compress --settings={{ project_name }}.settings.production')
        run(python + ' {{ project_name }}/manage.py update_index --settings={{ project_name }}.settings.production')

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
        run(python + ' {{ project_name }}/manage.py migrate --settings={{ project_name }}.settings.production --noinput')
        run(python + ' {{ project_name }}/manage.py collectstatic --settings={{ project_name }}.settings.production --noinput')
        run(python + ' {{ project_name }}/manage.py compress --settings={{ project_name }}.settings.production')
        run(python + ' {{ project_name }}/manage.py update_index --settings={{ project_name }}.settings.production')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')


def dokku(command, **kwargs):
    kwargs.setdefault('shell', False)
    return run(command, **kwargs)


class TestingEnvironment(object):
    prefix = '{{ project_name }}'
    settings_module = '{{ project_name }}.settings.production_paas'

    def __init__(self, branch):
        self.branch = branch

    @property
    def name(self):
        return self.prefix + '-' + self.branch.replace('/', '-')

    def set_config(self, config):
        config_string = ' '.join([
            name + '=' + value
            for name, value in config.items()
        ])
        dokku('config:set %s %s' % (self.name, config_string), warn_only=True)

    def run(self, command, interactive=False):
        dokku('run %s %s' % (self.name, command))

    def django_admin(self, command, interactive=False):
        self.run('django-admin %s' % command, interactive=interactive)

    def push(self):
        local('git push %s:%s %s:master' % (env['host_string'], self.name, self.branch))

    def exists(self):
        return dokku('config %s' % self.name, quiet=True).succeeded

    def create(self):
        # Create app
        dokku('create %s' % self.name)

        # Create database
        dokku('postgresql:create %s' % self.name)
        dokku('postgresql:link %s %s' % (self.name, self.name))

        # Create volume for media
        dokku('volume:create %s /app/media/' % self.name)
        dokku('volume:link %s %s' % (self.name, self.name))

        # Extra configuration
        self.set_config({
            'DJANGO_SETTINGS_MODULE': self.settings_module,
            'PYTHONPATH': '/app/{{ project_name }}/',
            'SECRET_KEY': 'test',
        })

    def update(self):
        self.push()
        self.django_admin('migrate')


@roles('testing')
def test():
    branch = local('git branch | grep "^*" | cut -d" " -f2', capture=True)

    env = TestingEnvironment(branch)

    # Create the environment
    if not env.exists():
        print("Creating testing environment for %s..." % branch)
        env.create()

    # Update it
    print("Updating testing environment...")
    env.update()
