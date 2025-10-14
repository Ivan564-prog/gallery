from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings


scheduler = BackgroundScheduler(
    jobstores={
        'default': DjangoJobStore()
    },
    executors={
        'default': ThreadPoolExecutor(10),
        'processpool': ProcessPoolExecutor(2)
    },
    job_defaults={
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': 7200
    },
    timezone=settings.TIME_ZONE
)

# Задачи перечитываются при migrate

# Пример задачи запускаемой каждый день в 14:41
# from .tests import test_job
# scheduler.add_job(
#     test_job,
#     'cron',
#     hour=14, minute=41,
#     id='test_task',
#     name='Тестовая задача',
#     replace_existing=True
# )
# Пример задачи запускаемой каждые 20 минут
# scheduler.add_job(
#     test_job,
#     'interval',
#     minutes=20,
# )