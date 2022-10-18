from celery import Celery
from celery.schedules import crontab


clr = Celery('clr', include=['celeryd.tasks'])

clr.config_from_object('celeryd.celeryconfig')
clr.conf.beat_schedule = {
    'run-me-every-5-minute-task': {
        'task': 'celeryd.tasks.check_vote_which_be_running',
        'schedule': crontab(minute='*/5')
    },
    'run-me-every-10-minute-task': {
        'task': 'celeryd.tasks.check_vote_which_be_finished',
        'schedule': crontab(minute='*/10')
    }
}
