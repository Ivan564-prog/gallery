from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from . import serializers, models
from rest_framework.exceptions import ValidationError


class CartViewSet(ViewSet):
    queryset = models.Cart.objects.all()

    def list(self, request):
        """ Получение корзины пользователя """
        cart = models.Cart.get_from_request(request)
        return Response(serializers.CartSerializer(cart, context={'request': request}).data)
    
    def destroy(self, request, pk):
        """ Удаление элемента корзины """
        cart = models.Cart.get_from_request(request)
        cart.positions.filter(product__pk=pk).delete()
        return Response(serializers.CartSerializer(cart, context={'request': request}).data)
    
    def update(self, request, pk=None):
        """ Изменение элемента корзины """
        cart = models.Cart.get_from_request(request)
        quantity = int(request.data.get('quantity', '1'))
        quantity = quantity if quantity >= 0 else 1
        position = cart.positions.get(product__pk=pk)
        if quantity > position.product.quantity:
            raise ValidationError({'__all__': ['Недостаточно товаров']})
        
        position.quantity = quantity
        position.save()
        return Response(serializers.CartSerializer(cart, context={'request': request}).data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def create(self, request):
        """ Создание элемента корзины """
        cart = models.Cart.get_from_request(request)

        product_id = request.data.get('product_id', None)
        quantity = int(request.data.get('quantity', '1'))
        cart.add_item(product_id, quantity)

        return Response(serializers.CartSerializer(cart, context={'request': request}).data)