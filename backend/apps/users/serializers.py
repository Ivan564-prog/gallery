from rest_framework import serializers
from . import models
import re
from core.logger import logger
from core.serializers import EmailSerializerValidator
from django.contrib.auth import authenticate
from django.utils import timezone


class ActivationSerializer(serializers.Serializer):

    id = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        users = models.User.objects.filter(id=attrs['id'])
        if not users.exists():
            raise serializers.ValidationError("Аккаунт не найден")
        user = users.get()
        if user.is_active:
            raise serializers.ValidationError("Аккаунт уже активирован")
        if user.activation_code != attrs['code']:
            raise serializers.ValidationError("Код активации не верен")
        if user.activation_deadline < timezone.now():
            user.send_activation_code(self.request)
            raise serializers.ValidationError("Код активации устарел. Новый код активации отравлен вам на почту")
        return attrs

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('context', {}).get('request', None)
        return super().__init__(*args, **kwargs)


class AuthorizeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = (
            models.User.USERNAME_FIELD,
            'password',
        )

    def __init__(self, *args, **kwargs):
        setattr(self, f'validate_{models.User.USERNAME_FIELD}', self.validate_username)
        self.fields[models.User.USERNAME_FIELD] = serializers.CharField(write_only=True)
        return super().__init__(*args, **kwargs)

    def validate_username(self, username):
        if not models.User.has_user(username):
            raise serializers.ValidationError("Такого пользователя не существует")
        return username

    def validate_password(self, password):
        if models.User.has_user(self.initial_data.get(models.User.USERNAME_FIELD)):
            if not authenticate(**self.initial_data):
                raise serializers.ValidationError("Пароль не верен")
        return password


class UserPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get('password1', '') != attrs.get('password2', ''):
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    
    def validate_password1(self, password1):
        if len(password1) < 6:
            raise serializers.ValidationError("Минимальная длина пароля 6 символов")
        return password1


class UserSerializer(UserPasswordSerializer, EmailSerializerValidator, serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        exclude = (
            'password',
            'last_login',
            'is_superuser',
            'is_staff',
            'date_joined',
            'activation_code',
            'activation_deadline',
            'reset_code',
            'reset_deadline',
            'is_active',
            'groups',
            'user_permissions',
        )
        
    def create(self, validated_data):
        validated_data[models.User.USERNAME_FIELD] = validated_data[models.User.USERNAME_FIELD].lower()
        models.User.objects.filter(**{'is_active': False, models.User.USERNAME_FIELD: validated_data[models.User.USERNAME_FIELD]}).delete()
        password = validated_data['password1']
        del validated_data['password1']
        del validated_data['password2']
        obj = models.User.objects.create(**validated_data)
        obj.set_password(password)
        obj.save()
        return obj

    def update(self, instance, validated_data):

        password = validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        validated_data.pop(models.User.USERNAME_FIELD, None)
        if password:
            instance.set_password(password)

        for key in validated_data.keys():
            setattr(instance, key, validated_data.get(key, getattr(instance, key)))
        instance.save()
        return instance
    
class RegisterSerializer(UserSerializer):

    class Meta:
        model = models.User
        fields = (
            models.User.USERNAME_FIELD,
            'password1',
            'password2',
        )