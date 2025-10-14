from rest_framework import serializers
from . import models


class BookTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BookType
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        exclude = (
            'description',
            'file',
            'type',
            'is_new',
        )


class BookSerializer(serializers.ModelSerializer):
    type = BookTypeSerializer()

    class Meta:
        model = models.Book
        fields = '__all__'

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = BookListSerializer()
        return serializers.ListSerializer(*args, **kwargs)