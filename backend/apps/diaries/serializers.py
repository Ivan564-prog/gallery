from rest_framework import serializers
from . import models
from apps.users.models import User


# class CreatorSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'id',
#             'id',
#             'id',
#             'id',
#             'id',
#         )


class DiaryListSerializer(serializers.ModelSerializer):
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = models.Diary
        fields = (
            'id',
            'creator',
            'title',
            'short_description',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wishlist_ids = self.context['request'].user.get_diary_wishlist().get_ids()

    def get_in_wishlist(self, instance):
        return instance.pk in self.wishlist_ids


class DiarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Diary
        exclude = (
            'created_by_diocese',
            'creator',
            'updated_at',
            'created_at',
        )