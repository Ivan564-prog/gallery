from . import models, serializers
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate, login, logout
from apps.local_hierarchy.models import Diocese
# from apps.local_hierarchy.serializers import InviteSerializer
from apps.users.models import User
from core.logger import logger


class UserViewSet(ViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    username_field = models.User.USERNAME_FIELD

    def list(self, request):
        """Отображение инормации о текущем пользователе"""
        if request.user.is_authenticated and request.user.is_active:
            return Response(
                self.serializer_class(request.user, context={'request': request}).data)
        return Response()
    
    def patch(self, request):
        """Изменение информации о текущем пользователе"""
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=False)
    def register(self, request):
        """Регистрация"""
        serializer = serializers.RegisterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        object = serializer.save()
        models.Invite.objects.get(code=request.data.get('code')).set_fields(object)
        return Response(self.serializer_class(object, context={'request': request}).data)
    
    @action(methods=['POST'], detail=False, url_path='invite')
    def send_invite(self, request):
        """
            Отправка приглашения пользователя
            Если пользователь миссионер, а приглашение на должность выше, то пользователь изменяет свой статус
            Старый аккаунт администрации или 
        """
        role_map = {
            'chief': 'missionary',
            'admin': 'chief',
            'root': 'admin',
        }
        email = request.data.get('email')
        diocese = Diocese.objects.get(pk=request.data.get('diocese')) if request.user.status == 'root' else request.user.diocese
        if not User.objects.filter(email=email).exists():
            invite = models.Invite.objects.create(
                invite_by=request.user,
                email=request.data.get('email'),
                diocese=diocese,
                role=role_map[request.user.status],
            )
            invite.send(request)
            return Response({
                'status': 'created',
                'invite': serializers.InviteSerializer(invite, context={'request': request}).data,
            }, status=201)
        elif User.objects.filter(email=email).get().status == 'missionary' and role_map[request.user.status] in ['chief', 'admin']:
            user = User.objects.filter(email=email).get()
            user.diocese = diocese
            if role_map[request.user.status] == 'chief':
                if diocese.chief is None:
                    user.chief_in = diocese
                else:
                    return Response({'message': 'Епархия уже имеет ответственного за ЕМО'}, status=400)
            else:
                if diocese.admin is None:
                    user.admin_in = diocese
                else:
                    return Response({'message': 'Епархия уже имеет аккаунт администрации'}, status=400)
            user.save()
            return Response({
                'status': 'updated',
                'user':  serializers.UserListSerializer(user, context={'request': request}).data,
            })
        else:
            return Response({'email': 'Такой пользователь уже существует'}, status=400)
    
    @action(methods=['GET'], detail=False)
    def check_register(self, request):
        invites = models.Invite.objects.filter(code=request.GET.get('code'))
        return Response(invites.exists() and timezone.now() < invites.get().deadline)
        
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
    
    @action(methods=['DELETE'], detail=False, url_path='invite/(?P<invite_id>[^/.]+)')
    def disable_invite(self, request, invite_id):
        try:
            invite = request.user.get_invites().get(id=invite_id)
        except:
            return Response({'message': 'Приглашение не найдено'}, status=404)
        invite.is_active = False
        invite.save()
        return Response(status=204)

    
    @action(methods=['GET'], detail=False, url_path='dioces_users')
    def get_diocese_users(self, request):
        user = request.user
        return Response({
            'transfers': serializers.TransferSerializer(user.get_transfers(), many=True, context={"request": request}).data,
            'invites': serializers.InviteSerializer(user.get_invites(), many=True).data,
            'users': serializers.UserListSerializer(user.get_invite_users(), many=True, context={'request': request}).data,
        })
    
    @action(methods=['PATCH'], detail=False, url_path='transfer_management/(?P<transfer_id>[^/.]+)')
    def transfer_management(self, request, transfer_id):
        actions = [
            'accept',
            'close',
        ]
        action = request.data.get('action')
        if action in actions:
            transfer = request.user.get_transfers().get(id=transfer_id, status='created')
            getattr(transfer, action)()