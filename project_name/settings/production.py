from .base import *


DEBUG = False
TEMPLATE_DEBUG = False

COMPRESS_OFFLINE = True


try:
    from .local import *
except ImportError:
    pass
