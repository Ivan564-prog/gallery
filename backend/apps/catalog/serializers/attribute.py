from rest_framework import serializers
from .. import models


class AttributeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeName
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeValue
        fields = '__all__'


class AttributeProductSerializer(serializers.ModelSerializer):

    attribute_name = AttributeNameSerializer()
    attribute_value = AttributeValueSerializer()

    class Meta:
        model = models.AttributeProduct
        exclude = (
            'product',
        )