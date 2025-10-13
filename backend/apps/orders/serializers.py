from rest_framework import serializers
from . import models
from apps.carts.models import Cart
from apps.catalog.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = models.OrderItem
        exclude = (
            'order',
        )


class OrderSerializer(serializers.ModelSerializer):
    positions = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = models.Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs['context'].get('request')
        self.cart = Cart.get_from_request(self.request)
        return super().__init__(*args, **kwargs)

    def validate(self, attrs):
        if not self.cart.cart_items.count():
            raise serializers.ValidationError("Корзина пуста")
        return attrs
        
    def create(self, validated_data):
        obj = models.Order.objects.create(**validated_data)
        for cart_item in self.cart.get_cart_items():
            obj.positions.create(
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        if self.request.user.is_authenticated:
            obj.user = self.request.user
            obj.save()
        self.cart.clear()
        return obj