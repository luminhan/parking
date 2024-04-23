import os

from celery import Celery


# Celery configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery("project")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
