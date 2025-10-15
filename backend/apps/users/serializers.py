from rest_framework import serializers
from . import models
from core.logger import logger
from core.serializers import PhoneSerializerValidator, EmailSerializerValidator
from django.contrib.auth import authenticate
from django.utils import timezone


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


class UserSerializer(UserPasswordSerializer, PhoneSerializerValidator, EmailSerializerValidator, serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    
    class Meta:
        model = models.User
        exclude = (
            'password',
            'last_login',
            'is_superuser',
            'is_staff',
            'date_joined',
            'reset_code',
            'reset_deadline',
            'is_active',
            'groups',
            'user_permissions',
        )

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


class RegisterSerializer(PhoneSerializerValidator, UserSerializer):
    code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    patronumic = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(format='%d:%m:%Y', required=True)
    city = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = models.User
        fields = (
            'name',
            'surname',
            'patronumic',
            'date_of_birth',
            'city',
            'phone',
            'password1',
            'password2',
            'code',
        )

    def validate_code(self, code):
        invites = models.Invite.objects.filter(is_active=True, code=code)
        if not models.Invite.objects.filter(code=code).exists() or timezone.now() > invites.get().deadline:
            raise serializers.ValidationError("Код не существует или срок его действия закончился")
        self.invite = invites.get()

    def create(self, validated_data):
        del validated_data['code']
        validated_data['email'] = self.invite.email
        validated_data[models.User.USERNAME_FIELD] = validated_data[models.User.USERNAME_FIELD].lower()
        models.User.objects.filter(**{'is_active': False, models.User.USERNAME_FIELD: validated_data[models.User.USERNAME_FIELD]}).delete()
        password = validated_data['password1']
        del validated_data['password1']
        del validated_data['password2']
        obj = models.User.objects.create(**validated_data)
        obj.set_password(password)
        obj.save()
        return obj
