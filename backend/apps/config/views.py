from core.mixins import BaseModelViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from . import models, serializers
from apps.library.models import Book
from django.utils import timezone
from datetime import timedelta


class StatsViewSet(ViewSet):
    queryset = models.RootSettings.objects.none()

    def list(self, request):
        user = request.user
        
        return Response({
            'new_noticies': user.notices.filter(is_viewed=False).count(),
            'new_books': Book.objects.filter(published_at__isnull=False, published_at__lte=timezone.now() + timedelta(days=14)).count(),
            'new_wishlist': user.get_diary_wishlist().diaries.all().count(),
            'diaries_report': user.get_current_report() and user.get_current_report().diaries.all().count(),
        })


class DomainViewSet(BaseModelViewSet):
    queryset = models.Domain.objects.all()
    serializer_class = serializers.DomainSerializer


class RootSettingsViewSet(BaseModelViewSet):
    queryset = models.RootSettings.objects.all()
    serializer_class = serializers.RootSettingsSerializer

    def list(self, request):
        return Response(self.serializer_class(
            models.RootSettings.get_settings(), context={'request': request}).data)