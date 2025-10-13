from rest_framework import serializers
from apps.catalog.serializers import ProductListSerializer
from . import models


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = models.CartItem
        exclude = (
            'cart',
        )


class CartSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    positions = CartItemSerializer(many=True)

    class Meta:
        model = models.Cart
        fields = (
            'id',
            'positions',
            'count',
            'total',
        )
    
    def get_positions(self, obj):
        return CartItemSerializer(obj.cart_items, many=True).data

    def get_count(self, obj):
        return obj.count

    def get_total(self, obj):
        return obj.total