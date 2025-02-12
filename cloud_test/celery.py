import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_test.settings')

app = Celery('cloud_test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
