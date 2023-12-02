import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduprene.settings')

app = Celery('eduprene')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_results=False)
def debug_task(self):
    print(f'Request: {self.request!r}')
