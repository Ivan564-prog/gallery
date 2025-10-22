from core.mixins import BaseModelViewSet
from core.permissions import IsAdministration 
from . import models, serializers
from apps.diaries.models import Diary
from rest_framework.response import Response
from rest_framework.decorator import action


class ReportViewSet(BaseModelViewSet):

    permission_classes = [IsAdministration,]
    
    def get_queryset(self):
        queryset = models.Report.objects.all()
        user = self.request.user
        if user.status in ['chief', 'admin']:
            queryset = queryset.filter(diocese=user.chief_in or user.admin_in)
        queryset = self.search(queryset)
        return queryset
    
    def search(self, queryset):
        # тут фильтры queryset-а при поиске от root аакаунта
        return queryset
    
    @action(methods=['GET'], url_path='current')
    def get_current(self, request):
        user = self.request.user
        report = models.Report.get_current(user.chief_in or user.admin_in)
        return Response(serializers.ReportSerializer(report, context={'request': request}).data)
    
    @action(methods=['GET'], url_path='current')
    def toggle_diary(self, request):
        user = self.request.user
        report = models.Report.get_current(user.chief_in or user.admin_in)
        report.toggle_diary(Diary.objects.get(id=request.GET.get('diary_id')))
        return 