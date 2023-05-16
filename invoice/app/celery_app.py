# django_celery/celery.py

import os
try:
    import celery
    from celery import Celery
except ImportError:
    raise ImportError("celery is required to use Invoice Celery")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()