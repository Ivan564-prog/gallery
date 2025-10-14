from apps.task_manager.tests import test_task
from django.core.management import BaseCommand
from core.logger import logger
from apps.task_manager.models import Task
import os
import importlib
import json
import traceback
from django.utils import timezone


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--module', type=str)
        parser.add_argument('--func_name', type=str)
        parser.add_argument('--func_args', type=str)
        parser.add_argument('--func_kwargs', type=str)

    def get_log_file(self):
        log_path = '/app/logs/tasks.log'
        filemode = 'a' if os.path.exists(log_path) else 'w'
        return open(log_path, filemode)

    def handle(self, *args, **options):
        module = options['module']
        func_name = options['func_name']
        
        task = Task.objects.create(
            func_name=f'{module}|{func_name}',
            args=options['func_args'],
            kwargs=options['func_kwargs'],
            pid=os.getpid()
        )
        try:
            # getattr(importlib.import_module(module), func_name)(*func_args, **func_kwargs)
            
            task.result = task.start()
            task.status = Task.SUCCESS
        except Exception as e:
            task.status = Task.ERROR
            error_msg = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            logger.error(error_msg)
            task.error = error_msg
        finally:
            task.closed_at = timezone.now()
            task.save()