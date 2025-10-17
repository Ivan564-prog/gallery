from rest_framework import serializers
from . import models


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notice
        fields = (
            'id',
            'title',
            'text',
            'is_viewed',
            'created_at',
        )

    