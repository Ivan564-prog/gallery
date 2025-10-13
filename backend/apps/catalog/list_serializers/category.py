from rest_framework import serializers
from .. import models


class CategoryListSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()
    # product_count = serializers.ReadOnlyField()

    class Meta:
        fields = (
            'title',
            'slug',
            'link',
            'image',
            'children',
        )
        model = models.Category

    def get_children(self, obj):
        return CategoryListSerializer(obj.children.active(), many=True).data