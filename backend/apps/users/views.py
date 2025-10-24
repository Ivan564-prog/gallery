from . import models, serializers
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth import authenticate, login, logout
from apps.local_hierarchy.models import Diocese
# from apps.local_hierarchy.serializers import InviteSerializer
from apps.users.models import User
from core.logger import logger


class UserViewSet(ViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    username_field = models.User.USERNAME_FIELD
    ROLE_MAP = {
            'chief': 'missionary',
            'admin': 'chief',
            'root': 'admin',
    }

    def list(self, request):
        """Отображение инормации о текущем пользователе"""
        if not request.user.is_authenticated or not request.user.is_active:
            return Response(status=403)
        return Response(
            self.serializer_class(request.user, context={'request': request}).data)
    
    def patch(self, request):
        """Изменение информации о текущем пользователе"""
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Деактивация роли пользователя"""
        try:
            object = request.user.get_related_users().get(pk=pk)
        except:
            return Response(status=404)
        object.deactivate()
        return Response(status=204)
    
    @action(methods=['POST'], detail=False)
    def register(self, request):
        """Регистрация"""
        code = request.data.get('code', None)
        try:
            invite = models.Invite.objects.get(code=code)
        except:
            Response({'code': 'Код не существует или срок его действия закончился'}, status=400)
        serializer = getattr(serializers, f'Register{invite.role.capitalize()}Serializer')(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        object = serializer.save()
        models.Invite.objects.get(code=request.data.get('code')).set_fields(object)
        return Response(self.serializer_class(object, context={'request': request}).data)
    
    @action(methods=['POST'], detail=False, url_path='invite')
    def send_invite(self, request):
        """
            Отправка приглашения пользователя
            Если пользователь деактивирован, то пользователь активируется и устанавливается на приглашенную роль
            Если пользователь миссионер, а приглашение на должность выше, то пользователь изменяет свой статус
            Если пользователь миссионер, а приглашение так же на миссионера - ошибка
            Если пользователь старший миссионер, администрация или главный админ - ошибка
        """
        email = request.data.get('email')
        diocese = Diocese.objects.get(pk=request.data.get('diocese')) if request.user.role == 'root' else request.user.diocese
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        if user is None:
            invite = models.Invite.objects.create(
                invite_by=request.user,
                email=request.data.get('email'),
                diocese=diocese,
                role=self.ROLE_MAP[request.user.role],
            )
            invite.send(request)
            return Response({
                'status': 'created',
                'message': 'Приглашение успешно отправлено',
                'invite': serializers.InviteSerializer(invite, context={'request': request}).data,
            }, status=201)
        else:
            success, message = diocese.set_role(user, self.ROLE_MAP[request.user.role])
            if success:
                return Response(
                    {
                        'status': 'updated',
                        'message': message,
                        'user':  serializers.UserListSerializer(User.objects.get(email=email), context={'request': request}).data,
                    },
                    status=200,
                )
            else:
                return Response({'message': message}, status=400)
    
    @action(methods=['GET'], detail=False)
    def check_register(self, request):
        """Проверка кода регистрации"""
        invites = models.Invite.objects.filter(code=request.GET.get('code'))
        return Response({
            'success': invites.exists() and timezone.now() < invites.get().deadline,
            'role': invites.exists() and invites.get().role,
        })
        
    @action(methods=['POST'], detail=False)
    def authorize(self, request):
        """Авторизация"""
        serializers.AuthorizeSerializer(data=request.data).is_valid(raise_exception=True)
        user = authenticate(**request.data)
        login(self.request, user)
        return Response(self.serializer_class(user).data)
    
    @action(methods=['POST'], detail=False)
    def logout(self, request):
        """Выход из аккаунта"""
        logout(request)
        return Response()
    
    @action(methods=['POST'], detail=False)
    def send_reset_password(self, request):
        """Отправка письма с ссылкой для изменения пароля"""
        serializers.AuthorizeSerializer(data=request.data, partial=True).is_valid(raise_exception=True)
        models.User.objects.get(**request.data).send_reset_link(request)   
        return Response({'success': True})
    
    @action(methods=['GET'], detail=False)
    def check_reset(self, request):
        """Проверка кода изменения пароля"""
        data = request.GET
        id = data.get('id', None)
        code = data.get('code', None)
        if not models.User.objects.filter(id=id, reset_code__isnull=False, reset_code=code).exists():
            return Response(status=404)
        return Response() 

    @action(methods=['POST'], detail=False)
    def reset_password(self, request):
        """Изменение пароля по коду"""
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
        """Деактивация приглашения"""
        try:
            invite = request.user.get_invites().get(id=invite_id)
        except:
            return Response({'message': 'Приглашение не найдено'}, status=404)
        invite.is_active = False
        invite.save()
        return Response(status=204)

    @action(methods=['GET'], detail=False, url_path='dioces_users')
    def get_diocese_users(self, request):
        """Получение текущий, приглашенных и переводящийхся пользователей епархии(епархии в которой пользователь главный миссионер)"""
        user = request.user
        return Response({
            'transfers': serializers.TransferSerializer(user.get_transfers(), many=True, context={"request": request}).data,
            'invites': serializers.InviteSerializer(user.get_invites(), many=True).data,
            'users': serializers.UserListSerializer(user.get_invite_users(), many=True, context={'request': request}).data,
        })
    
    @action(methods=['PATCH'], detail=False, url_path='transfer_management/(?P<transfer_id>[^/.]+)')
    def transfer_management(self, request, transfer_id):
        """Управление трансферами(принятие/отклонение)"""
        actions = [
            'accept',
            'close',
        ]
        action = request.data.get('action')
        if action in actions:
            transfer = request.user.get_transfers().get(id=transfer_id, status='created')
            getattr(transfer, action)()