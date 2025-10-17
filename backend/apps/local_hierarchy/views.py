from core.mixins import BaseModelViewSet
from .models import Diocese, Metropolis
from .serializer import DioceseSerializer, MetropolisSerializer


class DioceseViewSet(BaseModelViewSet):
    queryset = Diocese.objects.all()
    serializer_class = DioceseSerializer
    with_pagin = False

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        if self.request.GET.get('query', None):
            queryset = queryset.filter(title__icontains=self.request.GET.get('query'))
        if self.request.GET.get('limit', None):
            queryset = queryset[:int(self.request.GET.get('limit'))]
        return queryset
    

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