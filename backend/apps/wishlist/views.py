from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from . import models
from apps.catalog.models import Product
from apps.catalog.serializers import ProductSerializer


class WishlistViewSet(ViewSet):
    queryset = models.Wishlist.objects.all()

    @action(methods=['GET'], detail=False, url_path='ids')
    def get_products_ids(self, *args, **kwargs):
        wishlist = models.Wishlist.get_from_request(self.request)
        return Response(wishlist.products.values_list('id', flat=True))

    def list(self, request):
        wishlist = models.Wishlist.get_from_request(request)
        return Response(ProductSerializer(wishlist.products, many=True, context={'request': request}).data)

    def create(self, request):
        wishlist = models.Wishlist.get_from_request(request)
        product_id = request.data.get('product_id')
        product = Product.objects.get(pk=product_id)
        wishlist.toggle(product)
        return Response(wishlist.products.values_list('id', flat=True))