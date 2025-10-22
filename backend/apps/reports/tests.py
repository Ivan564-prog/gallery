# from django.test import TestCase
# from .models import Quarter, Report 
# from apps.local_hierarchy.models import Diocese, Metropolis, Country, Region
# from datetime import datetime


# class ReportModelTestCase(TestCase):

#     def test_get_current(self):
#         today = datetime.strptime('01.01.2024', '%d.%m.%Y')
#         current = Report.get_current(diocese=Diocese.objects.get(), today=today)
#         self.assertEqual(Quarter.objects.all().count() == 4)

#     @classmethod
#     def _set_up_quarter(cls):
#         Quarter.objects.create(title='1', start_period='01.01', end_period='03.10', start_send='03.01', end_send='03.20')
#         Quarter.objects.create(title='2', start_period='03.11', end_period='06.10', start_send='06.01', end_send='06.20')
#         Quarter.objects.create(title='3', start_period='06.11', end_period='09.10', start_send='09.01', end_send='09.20')
#         Quarter.objects.create(title='4', start_period='09.10', end_period='31.12', start_send='20.12', end_send='10.01')

#     @classmethod
#     def _set_up_local_hierarchy(cls):
#         country = Country.objects.create(title='Россия')
#         region = Region.objects.create(title='Московская область', country=country)
#         metropolis = Metropolis.objects.create(title='Московская', region=region)
#         Diocese.objects.create(title='Московская', metropolis=metropolis)

#     @classmethod
#     def setUpTestData(cls):
#         print(1)
#         cls._set_up_quarter()
        # cls._set_up_local_hierarchy()