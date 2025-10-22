from . import models, serializers
from core.mixins import BaseModelViewSet
from core.permissions import IsRoot
from core.helpers import get_pagination_page
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.users.serializers import UserListSerializer
from core.logger import logger



class NoticeViewSet(BaseModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user)
        queryset = queryset.select_related('notification')
        return queryset
    
    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        if not object.is_viewed:
            object.is_viewed = True
            object.save()
        return object
    
    @action(methods=['GET'], detail=True, url_path='viewing', permission_classes=[IsRoot,])
    def get_viewing(self, request, id, *args):
        obj = self.get_object()
        return Response(get_pagination_page(request=request, queryset=obj.notification.get_unsuspecting_users(), serializer_class=UserListSerializer))