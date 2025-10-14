from rest_framework import serializers
from . import models


class BookTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BookType
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    is_new = serializers.ReadOnlyField()
    on_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = models.Book
        exclude = (
            'description',
            'type',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wishlist_ids = self.context.get('request').user.get_book_wishlist().get_book_ids()

    def get_on_wishlist(self, instance):
        return instance.pk in self.wishlist_ids
        


class BookSerializer(serializers.ModelSerializer):
    type = BookTypeSerializer()

    class Meta:
        model = models.Book
        fields = '__all__'

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = BookListSerializer(*args, **kwargs)
        return serializers.ListSerializer(*args, **kwargs)