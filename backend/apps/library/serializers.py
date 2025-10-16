from rest_framework import serializers
from . import models


class BookTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BookType
        fields = "__all__"


class BookListSerializer(serializers.ModelSerializer):
    is_new = serializers.ReadOnlyField()
    on_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = models.Book
        exclude = (
            'description',
            'type',
            'updated_at',
            'created_at',
            'published_at',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wishlist_ids = self.context.get('request').user.get_book_wishlist().get_book_ids()

    def get_on_wishlist(self, instance):
        return instance.pk in self.wishlist_ids
    


class CreateBookSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=models.BookType.objects.all())

    class Meta:
        model = models.Book
        exclude = (
            'updated_at',
            'created_at',
        )


class BookSerializer(serializers.ModelSerializer):
    type = BookTypeSerializer()
    similar = serializers.SerializerMethodField()

    class Meta:
        model = models.Book
        exclude = (
            'updated_at',
            'created_at',
        )

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = BookListSerializer(*args, **kwargs)
        return serializers.ListSerializer(*args, **kwargs)
    
    def get_similar(self, instance):
        return BookListSerializer(instance.get_similar(), many=True, context=self.context).data