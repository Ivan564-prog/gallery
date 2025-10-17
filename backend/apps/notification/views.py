from . import models, serializers
from core.mixins import BaseModelViewSet


class NoticeViewSet(BaseModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user)
        queryset = queryset.select_related('notification')
        return queryset
    
    def retrive(self, *args, **kwargs):
        object = self.get_object()
        if not object.is_viewed:
            object.is_viewed = True
            object.save()
        return super().retrive(*args, **kwargs)