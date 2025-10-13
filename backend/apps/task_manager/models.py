from core.logger import logger
import importlib
import json
from django.db import models


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
        getattr(importlib.import_module(module), func_name)(*func_args, **func_kwargs)

    def start_as_task(self):
        module, func_name = self.func_name.split('|')
        func_args = json.loads(self.args)
        func_kwargs = json.loads(self.kwargs)
        getattr(importlib.import_module(module), func_name).delay(*func_args, **func_kwargs)