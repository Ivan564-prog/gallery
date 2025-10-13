from rest_framework import serializers
from .. import models


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'link',
            'image',
            'price',
            'price_old',
            'slug',
        )