from core.mixins import BaseModelViewSet
from .models import Diocese, Metropolis
from .serializer import DioceseSerializer, DioceseExtendSerializer, MetropolisSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class DioceseViewSet(BaseModelViewSet):
    queryset = Diocese.objects.all()
    serializer_class = DioceseSerializer
    with_pagin = False
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        if self.request.GET.get('query', None):
            queryset = queryset.filter(title__icontains=self.request.GET.get('query'))
        if self.request.GET.get('limit', None):
            queryset = queryset[:int(self.request.GET.get('limit'))]
        return queryset
    
    @action(methods=['GET'], detail=False, url_path='account')
    def get_extended_dioceses(self, request):
        return Response(DioceseExtendSerializer(self.get_queryset(), many=True, context={'request': request}).data)


class MetropolisViewSet(BaseModelViewSet):
    queryset = Metropolis.objects.all()
    serializer_class = MetropolisSerializer
    with_pagin = False

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        if self.request.GET.get('query', None):
            queryset = queryset.filter(title__icontains=self.request.GET.get('query'))
        if self.request.GET.get('limit', None):
            queryset = queryset[:int(self.request.GET.get('limit'))]
        return queryset