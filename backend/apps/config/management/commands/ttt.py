from django.core.management import BaseCommand
import requests
from apps.reports.models import Quarter, Report
from apps.local_hierarchy.models import Diocese
from datetime import datetime
from core.logger import logger


class Command(BaseCommand):

    def handle(self, *args, **options):
        date = datetime.strptime('20.01.2024', '%d.%m.%Y')
        today = datetime.now()
        diocese = Diocese.objects.all()[0]
        
        # current_reports = Report.objects.filter(diocese=diocese, start_period__gte=today.date(), end_send__lte=today.date())
        # print(Report.objects.filter(diocese=diocese)[0].end_send)
        # return
        report = Report.get_current(diocese)
        # report.is_sended = True
        # report.save()
        logger.info(report.year)
        logger.info(f'period: {report.start_period.strftime('%d.%m.%Y')} - {report.end_period.strftime('%d.%m.%Y')}; sending: {report.start_send.strftime('%d.%m.%Y')} - {report.end_send.strftime('%d.%m.%Y')}')
        # for q in Quarter.objects.all().order_by('title'):
        #     start, end = Quarter._get_period(q.start_send, q.end_send, date.year)
        #     print(start.strftime('%d.%m.%Y') + ' - ' + end.strftime('%d.%m.%Y'))
        #     if start.date() <= date.date() and end.date() >= date.date():
        #         print(q)