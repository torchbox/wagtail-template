"""
Sample tasks file.
Will fallback to a simple task decorator that returns the original function.
"""

# The following will check to see if we can import task from celery -
# if not then we definitely haven't installed it.
# Taken from wagtail core
try:
    from celery.decorators import task
    NO_CELERY = False
except:
    NO_CELERY = True

# However, we could have installed celery for other projects. So we will also
# check if we have defined the BROKER_URL setting. If not then definitely we
# haven't configured it.
if NO_CELERY or not hasattr(settings, 'BROKER_URL'):
    # So if we enter here we will define a different "task" decorator that
    # just returns the original function and sets its delay attribute to
    # point to the original function: This way, the actual callee
    # function (task_function()) will be called instead of task_function.delay()
    def task(f):
        f.delay = f
        return f
