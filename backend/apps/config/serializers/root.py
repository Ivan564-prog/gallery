from rest_framework import serializers
from ..models import RootSettings


class RootSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RootSettings
        exclude = (
            'robots',
        )