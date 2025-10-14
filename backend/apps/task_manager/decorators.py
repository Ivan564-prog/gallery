import os
import subprocess
import json


class ClassMethodException(Exception):
    pass


class TaskDecorator:

    def is_method(self, func):
        return hasattr(func, '__self__') and func.__self__ is not None

    def get_log_file(self):
        log_path = '/app/logs/tasks.log'
        filemode = 'a' if os.path.exists(log_path) else 'w'
        return open(log_path, filemode)

    def __init__(self, func):
        if self.is_method(func):
            raise ClassMethodException('Задачей может быть только глобальная функция, а не метод класса')
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
        
    def delay(self, *args, **kwargs):
        subprocess.Popen(
            [
                'python', '-u', 'manage.py', 'start_task', 
                '--module', self.func.__module__,
                '--func_name', self.func.__name__,
                '--func_args', json.dumps(args),
                '--func_kwargs', json.dumps(kwargs),
            ],
            stdout=self.get_log_file(),
            stderr=self.get_log_file(),
            bufsize=1,
            text=True,
            universal_newlines=True
        )

def task(func):
    return TaskDecorator(func)