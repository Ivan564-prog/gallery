from rest_framework import serializers
from .models import Diocese, Metropolis


class DioceseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diocese
        fields = (
            'id',
            'title',
        )


class MetropolisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metropolis
        fields = '__all__'