from django.core.management import BaseCommand
from core.helpers import timer
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.test()
        
    @timer
    def test(self):
        time.sleep(873)