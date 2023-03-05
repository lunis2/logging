import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_news_sending': {
        'task': 'posts.tasks.weekly_notification',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

# app.conf.beat_schedule = {
#     'weekly_news_sending': {
#         'task': 'posts.tasks.weekly_notification',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#     },
# }
