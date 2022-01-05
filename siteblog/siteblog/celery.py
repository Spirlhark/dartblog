import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteblog.settings')

app = Celery('siteblog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-spam-every-5-minutes': {
        'task': 'blog.tasks.send_beat_email',
        'schedule': crontab(minute='*/5'),
    },
}