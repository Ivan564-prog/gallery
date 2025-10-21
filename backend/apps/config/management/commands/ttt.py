from django.core.management import BaseCommand
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get('http://localhost/api/v1/library/book/')
        print(r)