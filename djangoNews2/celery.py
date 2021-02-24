from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoNews2.settings')

app = Celery('djangoNews2')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'news.tasks.my_job',
        'schedule': crontab(2),
        'args': (),
    },
}