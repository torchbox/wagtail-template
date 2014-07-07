from .base import *


# Disable debug mode

DEBUG = False
TEMPLATE_DEBUG = False


# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE

COMPRESS_OFFLINE = True


# Celery settings
# http://celery.readthedocs.org/en/latest/configuration.html

import djcelery

djcelery.setup_loader()

CELERY_SEND_TASK_ERROR_EMAILS = True
BROKER_URL = 'redis://'


# Use Redis as the cache backend for extra performance

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'KEY_PREFIX': '{{ project_name }}',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}


# Use Elasticsearch as the search backend for extra performance and better search results

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': '{{ project_name }}',
    },
}


try:
    from .local import *
except ImportError:
    pass
