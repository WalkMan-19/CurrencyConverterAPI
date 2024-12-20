import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('CurrencyConverterAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-data-every-midnight': {
        'task': 'converter.tasks.fetch_exchange_rates',
        'schedule': crontab(minute="0"),  # crontab(minute="*") - каждую минуту
    },
}