import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am':{
        'task':'news.tasks.get_new_articles_for_subscribers',
        'schedule': crontab(),
        'args':()
    }

}

