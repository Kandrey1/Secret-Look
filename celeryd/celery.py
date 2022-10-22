from celery import Celery
from celery.schedules import crontab


clr = Celery('clr', include=['celeryd.tasks'])

clr.config_from_object('celeryd.celeryconfig')
clr.conf.beat_schedule = {
    'check_which_running-every-2m': {
        'task': 'celeryd.tasks.check_vote_which_running',
        'schedule': crontab(minute='*/2')
    },
    'check_which_finished-every-5m': {
        'task': 'celeryd.tasks.check_vote_which_finished',
        'schedule': crontab(minute='*/5')
    }
}
