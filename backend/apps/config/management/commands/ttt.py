from django.core.management import BaseCommand
import requests
from apps.reports.models import Quarter, Report
from apps.local_hierarchy.models import Diocese
from apps.users.models import User
from datetime import datetime
from core.logger import logger


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(email='test4@exapmle.com')
        diocese = Diocese.objects.all()[31]
        # user.reset_manage_role()
        # print(user.admin_in)
        # print(diocese)
        
        diocese._set_role(user, 'admin')