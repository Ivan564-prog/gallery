
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from . import models, serializers


class OrderViewSet(ViewSet):
    queryset = models.Order.objects.all()

    def create(self, request):
        data = request.data
        serializer = serializers.CreateOrderSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order.send_notify(request)
        return Response()
    
    @action(methods=['POST'], detail=True)
    def repeat(self, request, pk):
        request.user.orders.get(id=pk).repeat()