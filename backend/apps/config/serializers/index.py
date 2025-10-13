from rest_framework import serializers
from ..models import IndexSettings


class IndexSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndexSettings
        fields = '__all__'