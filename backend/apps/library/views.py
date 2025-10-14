from core.mixins import BaseModelViewSet
from . import models, serializers


class BookModelViewSet(BaseModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        queryset = queryset.exclude(status='deleted')
        if self.request.user.status != 'root':
            queryset = queryset.exclude(status='draft')
        book_type_id = self.request.GET.get('book_type')
        if book_type_id:
            queryset = queryset.filter(type__id=book_type_id)
        return queryset
    
    def perform_destroy(self, instance):
        instance.status = 'deleted'
        instance.save()


class BookTypeModelViewSet(BaseModelViewSet):
    queryset = models.BookType.objects.all()
    serializer_class = serializers.BookTypeSerializer