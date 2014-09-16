from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = '{{ secret_key }}'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
