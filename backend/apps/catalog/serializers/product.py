from rest_framework import serializers
from .. import models
from .attribute import AttributeProductSerializer
from ..list_serializers.product import ProductListSerializer
from apps.content.serializers import ContentSerializer


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        exclude = (
            'product',
        )


class ProductSerializer(serializers.ModelSerializer):
    breadcrumbs = serializers.ReadOnlyField()
    gallery = ProductImageSerializer(many=True)
    attributes = AttributeProductSerializer(many=True)
    content = ContentSerializer()

    class Meta:
        fields = '__all__'
        model = models.Product

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = ProductListSerializer()
        return serializers.ListSerializer(*args, **kwargs)