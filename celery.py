from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'myapp',  
    broker='redis://localhost:6379/0', 
    backend='redis://localhost:6379/0'  
)

celery.conf.timezone = 'UTC'


celery.conf.beat_schedule = {
    'check-every-minute': {
        'task': 'tasks.check_and_update_transactions',
        'schedule': crontab(minute='*'),
    },
}
