from rest_framework import serializers
from . import models


class PageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Page
        fields = [
            'id',
            'title',
            'slug',
            'link',
            'image',
        ]