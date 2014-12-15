from .production import *

SECRET_KEY = 'foobar'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db',
    }
}
