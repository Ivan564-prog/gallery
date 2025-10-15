from rest_framework import serializers
from . import models
from apps.users.models import User


class CreatorSerializer(serializers.ModelSerializer):
    diocese_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'status',
            'image',
        )



class DiaryListSerializer(serializers.ModelSerializer):
    in_wishlist = serializers.SerializerMethodField()
    creator = CreatorSerializer()

    class Meta:
        model = models.Diary
        fields = (
            'id',
            'creator',
            'title',
            'short_description',
            'published_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wishlist_ids = self.context['request'].user.get_diary_wishlist().get_diary_ids()

    def get_diocese_name(self, obj):
        return obj.held_in_diocese.title

    def get_in_wishlist(self, obj):
        return obj.pk in self.wishlist_ids


class DiarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Diary
        exclude = (
            'created_by_diocese',
            'creator',
            'updated_at',
            'created_at',
        )