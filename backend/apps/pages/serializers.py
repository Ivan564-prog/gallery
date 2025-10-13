from rest_framework import serializers
from apps.content.serializers import ContentSerializer
from . import models
from .list_serializers import PageListSerializer


class PageSerializer(serializers.ModelSerializer):
    content = ContentSerializer()
    breadcrumbs = serializers.ReadOnlyField()
    
    class Meta:
        model = models.Page
        fields = '__all__'

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = PageListSerializer()
        return serializers.ListSerializer(*args, **kwargs)