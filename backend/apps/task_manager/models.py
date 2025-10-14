from .scheduler import scheduler
from core.logger import logger
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from django.db import models
from django.dispatch import receiver
import importlib
import json


class DjangoJobProxy(DjangoJob):

    class Meta:
        proxy = True
        verbose_name = 'Рассписание'
        verbose_name_plural = 'Рассписание'


class DjangoJobExecutionProxy(DjangoJobExecution):

    class Meta:
        proxy = True
        verbose_name = 'Рассписание (Выполнения)'
        verbose_name_plural = 'Рассписание (Выполнения)'


class Task(models.Model):
    SUCCESS = 'success'
    ERROR = 'error'
    STATUSES = (
        (SUCCESS, 'Успех'),
        (ERROR, 'Ошибка'),
    )
    func_name = models.CharField(verbose_name='Функция', max_length=255)
    args = models.TextField(verbose_name='Позиционные аргументы', null=True, blank=True)
    kwargs = models.TextField(verbose_name='Именованные аргументы', null=True, blank=True)
    result = models.TextField(verbose_name='Результат', null=True, blank=True)

    status = models.CharField(verbose_name='Статус', max_length=50, choices=STATUSES, null=True, blank=True)
    pid = models.CharField(max_length=200)
    error = models.TextField(verbose_name='Ошибка', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    closed_at = models.DateTimeField(verbose_name='Завершена', blank=True, null=True)

    watched = models.BooleanField(verbose_name='Просмотрено', default=False)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    @property
    def func_args(self):
        return str(json.loads(self.args))

    @property
    def func_kwargs(self):
        return str(json.loads(self.kwargs))

    @classmethod
    def unwatched_errors(cls):
        return cls.objects.filter(watched=False, status=cls.ERROR).count()

    def get_status_icon(self):
        if self.status == self.SUCCESS:
            return ' ️✅'
        elif self.status == self.ERROR:
            return ' ❌'
        return ' ⏳'

    def __str__(self):
        return self.func_name + self.get_status_icon() + ('' if self.watched else ' ◉')

    def start(self):
        module, func_name = self.func_name.split('|')
        func_args = json.loads(self.args)
        func_kwargs = json.loads(self.kwargs)
        return getattr(importlib.import_module(module), func_name)(*func_args, **func_kwargs)

    def start_as_task(self):
        module, func_name = self.func_name.split('|')
        func_args = json.loads(self.args)
        func_kwargs = json.loads(self.kwargs)
        getattr(importlib.import_module(module), func_name).delay(*func_args, **func_kwargs)


@receiver(models.signals.post_migrate)
def set_django_admin_settings(sender, **kwargs):
    if sender.name != 'apps.task_manager':
        return
    if scheduler.running:
        scheduler.shutdown()
    job_ids = [i.id for i in scheduler.get_jobs()]
    DjangoJob.objects.exclude(id__in=job_ids).delete()
    scheduler.start()
    logger.info('Scheduler restarted')