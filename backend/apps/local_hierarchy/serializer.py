from rest_framework import serializers
from .models import Diocese


class DioceseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diocese
        fields = (
            'id',
            'title',
        )