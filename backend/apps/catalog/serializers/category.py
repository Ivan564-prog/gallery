from rest_framework import serializers
from .. import models
from apps.content.serializers import ContentSerializer
from ..list_serializers.category import CategoryListSerializer


class CategorySerializer(serializers.ModelSerializer):
    breadcrumbs = serializers.ReadOnlyField()
    product_count = serializers.ReadOnlyField()
    attributes = serializers.ReadOnlyField()
    extremum_prices = serializers.ReadOnlyField()
    content = ContentSerializer()
    
    class Meta:
        exclude = (
            'lft',
            'rght',
            'level',
            'parent',
        )
        model = models.Category

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = CategoryListSerializer()
        return serializers.ListSerializer(*args, **kwargs)