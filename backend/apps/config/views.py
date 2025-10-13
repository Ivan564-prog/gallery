from core.mixins import BaseModelViewSet
from rest_framework.response import Response
from . import models, serializers


class DomainViewSet(BaseModelViewSet):
    queryset = models.Domain.objects.all()
    serializer_class = serializers.DomainSerializer


class IndexSettingsViewSet(BaseModelViewSet):
    queryset = models.IndexSettings.objects.all()
    serializer_class = serializers.IndexSettingsSerializer

    def list(self, request):
        return Response(self.serializer_class(
            models.IndexSettings.get_settings(), context={'request': request}).data)


class RootSettingsViewSet(BaseModelViewSet):
    queryset = models.RootSettings.objects.all()
    serializer_class = serializers.RootSettingsSerializer

    def list(self, request):
        return Response(self.serializer_class(
            models.RootSettings.get_settings(), context={'request': request}).data)