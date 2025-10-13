from django.core.management import BaseCommand
import os
from apps.task_manager.tests import test_task


class Command(BaseCommand):

    def handle(self, *args, **options):
        test_task.delay('test', 'ttt', my='task', test=True)
        # with open('/app/test', 'w') as f:
        #     f.write('tt')
        # return 'test'