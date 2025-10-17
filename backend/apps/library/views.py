from core.mixins import BaseModelViewSet
from django.db.models import Case, When, Value, IntegerField
from . import models, serializers
from core.logger import logger
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


class BookModelViewSet(BaseModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    lookup_field = 'pk'

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method != 'GET':
            return serializers.CreateBookSerializer
        return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(serializers.BookListSerializer(item, context={'request': request}).data, status=HTTP_201_CREATED)

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        queryset = queryset.exclude(status='deleted')
        if self.request.user.status != 'root':
            queryset = queryset.exclude(status='draft')
        book_type_id = self.request.GET.get('book_type')
        if book_type_id:
            queryset = queryset.filter(type__id=book_type_id)
        if self.request.GET.get('in_wishlist', None):
            wish_pks = self.request.user.get_book_wishlist().get_book_ids()
            logger.info(wish_pks)
            queryset = queryset.filter(pk__in=wish_pks)
        return queryset.annotate(
            is_published=Case(
                    When(published_at__isnull=True, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )).order_by('-is_published', '-published_at')
    
    def perform_destroy(self, instance):
        instance.status = 'deleted'
        instance.save()


class BookTypeModelViewSet(BaseModelViewSet):
    queryset = models.BookType.objects.all()
    serializer_class = serializers.BookTypeSerializer