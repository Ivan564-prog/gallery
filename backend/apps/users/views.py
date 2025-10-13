from . import models, serializers
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate, login, logout
from core.logger import logger
from apps.orders.serializers import OrderSerializer


class UserViewSet(ViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    username_field = models.User.USERNAME_FIELD

    def list(self, request):
        if request.user.is_authenticated and request.user.is_active:
            return Response(
                self.serializer_class(request.user).data)
        return Response()
    
    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=False)
    def register(self, request):
        self.queryset.filter(**{'is_active': False, self.username_field: request.data[self.username_field].lower()}).delete()
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        object = serializer.save()
        object.send_activation_code(request)
        return Response(self.serializer_class(object, context={'request': request}).data)
        
    @action(methods=['POST'], detail=False)
    def authorize(self, request):
        serializers.AuthorizeSerializer(data=request.data).is_valid(raise_exception=True)
        user = authenticate(**request.data)
        login(self.request, user)
        return Response(self.serializer_class(user).data)
    
    @action(methods=['POST'], detail=False)
    def logout(self, request):
        logout(request)
        return Response()
    
    @action(methods=['POST'], detail=False)
    def send_reset_password(self, request):
        serializers.AuthorizeSerializer(data=request.data, partial=True).is_valid(raise_exception=True)
        models.User.objects.get(**request.data).send_reset_link(request)   
        return Response({'success': True})
    
    @action(methods=['GET'], detail=False)
    def check_reset(self, request):
        data = request.GET
        id = data.get('id', None)
        code = data.get('code', None)
        if not models.User.objects.filter(id=id, reset_code__isnull=False, reset_code=code).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        return Response() 

    @action(methods=['POST'], detail=False)
    def reset_password(self, request):
        data = request.data
        id = data.get('id', None)
        code = data.get('code', None)
        user = models.User.objects.get(id=id, reset_code__isnull=False, reset_code=code, reset_deadline__gte=timezone.now())
        serializers.UserPasswordSerializer(data=request.data).is_valid(raise_exception=True)
        user.set_password(data['password1'])
        user.save()
        return Response()
    
    @action(methods=['GET'], detail=False)
    def activation(self, request):
        serializers.ActivationSerializer(data=request.GET, context={'request': request}).is_valid(raise_exception=True)
        models.User.objects.filter(id=request.GET['id']).update(is_active=True)
        return Response({
            'success': True,
            'message': 'Аккаунт успешно активирован'
        })
    
    @action(methods=['GET'], detail=False, url_path='orders')
    def get_orders(self, request):
        if request.user.is_authenticated:
            return Response(OrderSerializer(request.user.orders.all().order_by('-created_at'), many=True).data)