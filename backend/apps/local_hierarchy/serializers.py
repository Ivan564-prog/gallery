from rest_framework import serializers
from .models import Diocese, Metropolis
from apps.users.models import User, Invite


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


class AdminDioceseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'image',
            'email',
        )


class DioceseInviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invite
        fields = (
            'id',
            'email',
        )


class DioceseExtendSerializer(serializers.ModelSerializer):
    admin = AdminDioceseSerializer()
    invite = serializers.SerializerMethodField()

    class Meta:
        model = Diocese
        fields = (
            'id',
            'title',
            'admin',
            'invite',
        )

    def get_invite(self, obj):
        invites = obj.invites.filter(is_active=True)
        if invites.exists():
            return DioceseInviteSerializer(invites[0], context=self.context).data