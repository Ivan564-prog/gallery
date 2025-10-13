from core.mixins import BaseModelViewSet
from core.logger import logger
from core.helpers import get_pagination_page
from . import models, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Case, When
import json


class ProductViewSet(BaseModelViewSet):
    queryset = models.Product.objects.active()
    serializer_class = serializers.ProductSerializer
    with_pagin = True

    def get_queryset(self):
        return self.queryset.filter_by_request(self.request).distinct().order_by_request(self.request)
    
    def retrieve(self, *args, **kwargs):
        self.get_object().visite()
        return super().retrieve(*args, **kwargs)

    @action(methods=['GET'], detail=False)
    def viewed(self, request):
        viewed = request.COOKIES.get('viewed')
        viewed_ids = json.loads(viewed) if viewed else []
        products = models.Product.objects.active() \
            .filter(pk__in=viewed_ids) \
            .order_by(Case(*[When(id=id, then=position) for position, id in enumerate(viewed_ids)]))
        return Response(self.serializer_class(products, many=True, context={'request': request}).data)


class CategoryViewSet(BaseModelViewSet):
    queryset = models.Category.objects.active()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(parent__isnull=True) if self.action == 'list' else self.queryset

    @action(methods=['GET'], detail=True)
    def products(self, request, slug):
        category = self.queryset.get(slug=slug)
        products = category.get_products().filter_by_request(self.request).distinct().order_by_request(self.request)
        return Response(get_pagination_page(
            request=request,
            queryset=products,
            serializer_class=serializers.ProductListSerializer
        ))

    @action(methods=['get'], detail=False, url_path='products/(?P<product_slug>[^/.]+)')
    def get_product_by_slug(self, request, product_slug, slug=None):
        category = get_object_or_404(self.queryset, slug=slug)
        product =  get_object_or_404(category.products.filter(is_active=True), slug=product_slug)
        product.visite()
        response = Response(serializers.ProductSerializer(product, context={'request': request}).data)
        response = self.add_viewed(response=response, request=request, product_id=str(product.id))
        return response
    
    def add_viewed(self, response, request, product_id):
        viewed = request.COOKIES.get('viewed')
        viewed_ids = json.loads(viewed) if viewed else []
        if product_id in viewed_ids:
            viewed_ids.remove(product_id)
        viewed_ids.insert(0, product_id)
        response.set_cookie('viewed', json.dumps(viewed_ids[:10]), max_age=2592000)
        return response