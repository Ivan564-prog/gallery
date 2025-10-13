from core import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .helpers import get_pagination_page, get_host
from apps.config.models import Domain


class BaseModelViewSet(ModelViewSet):
    permission_classes = [permissions.IsSuperuserOrReadOnly]
    lookup_field = 'slug'
    with_pagin = False

    def _get_sitemap(self, link_list):
        domains = Domain.objects.filter(is_active=True)
        result = []
        for domain in domains:
            for link in link_list:
                result.append(f'{get_host(self.request)}{domain.get_link()}{link}')
        else:
            for link in link_list:
                result.append(f'{get_host(self.request)}{link}')
        return result

    @action(methods=['GET'], detail=False)
    def sitemap(self, *args, **kwargs):
        return Response(self._get_sitemap([item.get_absolute_url() for item in self.queryset.all()]))
    
    def _get_labeled_title(self, item):
        return item.title
    
    def _get_labeled_link(self, item):
        return get_host(self.request) + item.get_absolute_url()

    @action(methods=['GET'], detail=False)
    def labeled_sitemap(self, *args, **kwargs):
        return Response([
            {
                'title': self._get_labeled_title(item),
                'link': self._get_labeled_link(item),
            } for item in self.queryset.all()
        ])

    def list(self, request):
        if not self.with_pagin:
            return super().list(request)
        return Response(get_pagination_page(
            request=request,
            queryset=self.get_queryset(),
            serializer_class=self.serializer_class
        ))