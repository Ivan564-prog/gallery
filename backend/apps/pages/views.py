from rest_framework.decorators import action
from rest_framework.response import Response
from core.mixins import BaseModelViewSet
from core.helpers import get_pagination_page
from . import serializers
from . import models
        


class PageViewSet(BaseModelViewSet):
    queryset = models.Page.objects.active()
    serializer_class = serializers.PageSerializer

    STATIC_PAGES = [
        {'title': 'Контакты', 'link': '/contacts'},
        {'title': 'Каталог', 'link': '/catalog'},
        {'title': 'Обработка персональных данных', 'link': '/personal-data'},
        {'title': 'Политика конфиденциальности', 'link': '/privacy-policy'},
    ]
    
    @action(methods=['GET'], detail=False, url_path='static_sitemap')
    def get_static_sitemap(self, *args, **kwargs):
        return Response(self._get_sitemap([item['link'] for item in self.STATIC_PAGES]))
    
    @action(methods=['GET'], detail=False, url_path='labeled_static_sitemap')
    def get_labeled_static_sitemap(self, *args, **kwargs):
        return Response(self.STATIC_PAGES)
    
    @action(methods=['GET'], detail=True, url_path='subpages')
    def get_subpages(self, request, *args, **kwargs):
        return Response(get_pagination_page(
            request=request,
            queryset=self.get_object().subpages.active(),
            serializer_class=serializers.PageListSerializer
        ))