from rest_framework import serializers
from core.serializers import EmailSerializerValidator, PhoneSerializerValidator
from . import models
from apps.catalog.models import Product


class FeedbackSerializer(EmailSerializerValidator, PhoneSerializerValidator, serializers.ModelSerializer):
    email = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=True, allow_blank=False)
    name = serializers.CharField(required=False, allow_blank=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = models.Feedback
        fields = '__all__'