from .managers import CustomUserManager
from apps.reports.models import Report
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import timedelta
from core.models import TimestampModelMixin
from core.logger import logger
from core.helpers import send_mail
import random
import string
import hashlib
import secrets


def get_deadline():
    return timezone.now() + timedelta(days=14)


class Invite(models.Model):
    ROLES = (
        ('admin', 'Администратор епархии'),
        ('chief', 'Главный миссионер'),
        ('missionary', 'Миссионер'),
    )
    is_active = models.BooleanField(
        verbose_name='Активность', default=True)
    invite_by = models.ForeignKey(
        'users.User', verbose_name='Приглашение от', on_delete=models.CASCADE, related_name='invites', null=True)
    email = models.EmailField(
        verbose_name='Почта')
    role = models.CharField(
        verbose_name='Роль', choices=ROLES)
    diocese = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='Епархия', on_delete=models.CASCADE)
    code = models.CharField(
        verbose_name='Код', unique=True, db_index=True)
    deadline = models.DateTimeField(  
        verbose_name='Дата истечения приглашения', default=get_deadline)
    
    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

    def __str__(self):
        return f'Приглашение для {self.email}'
    
    def set_fields(self, user):
        self.is_active = False
        self.save()
        user.diocese = self.diocese
        if self.role == 'chief_in':
            user.chief_in = self.diocese
        elif self.role == 'admin_in':
            user.admin_in = self.diocese
        user.save()

    
    def send(self, request):
        subject = f'Приглашение в миссионерство'
        html_message = render_to_string(
            'mails/invite.html',
            {
                'request': request,
                'link': f'{request.scheme}://{request.get_host()}/registration?code={self.code}',
                'role': self.get_role_display(),
                'diocese': self.diocese.title,
            }
        )
        to = [self.email]
        send_mail.delay(subject, to, html_message)

    def set_code(self, save=True):
        self.code = hashlib.sha256(secrets.token_bytes(16)).hexdigest()
        if save:
            self.save()

    def save(self, *args, **kwargs):
        self.set_code(save=False)
        return super().save(*args, **kwargs)


class ResetPassword(models.Model):

    reset_code = models.CharField(
        verbose_name='Код активации', null=True, blank=True)
    reset_deadline = models.DateTimeField(
        verbose_name='Время до конца активации', null=True, blank=True)

    class Meta:
        abstract = True
    
    def _generate_reset_code(self):
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(16))
        self.reset_code = code
        self.reset_deadline = timezone.now() + timedelta(hours=1)
        self.save()
        return code

    def send_reset_link(self, request):
        self._generate_reset_code()
        subject = f'Сброс пароля'
        html_message = render_to_string(
            'mails/reset-password.html',
            {
                'request': request,
                'reset_link': f'{request.scheme}://{request.get_host()}/reset-password?id={self.pk}&code={self.reset_code}',
            }
        )
        to = [self.email]
        send_mail.delay(subject, to, html_message)


class User(
        ResetPassword,
        TimestampModelMixin,
        AbstractUser,
    ):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    first_name = None
    last_name = None
    
    is_active = models.BooleanField(
        'Активность', default=True)
    task_permission = models.BooleanField(
        'Доступ к задачам', default=False)
    email = models.EmailField(
        verbose_name='Почта', max_length=255, unique=True)
    diocese = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='Епархия', on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(
        verbose_name='Имя', null=True)
    surname = models.CharField(
        verbose_name='Фамилия', blank=True, null=True)
    patronymic = models.CharField(
        verbose_name='Отчество', blank=True, null=True)
    date_of_birth = models.DateField(
        verbose_name='День рождения', blank=True, null=True)
    city = models.CharField(
        verbose_name='Город проживания', null=True, blank=True)
    phone = models.CharField(
        verbose_name='Телефон', null=True, blank=True)
    image = models.ImageField(
        verbose_name='Изображение', upload_to='images/users/', null=True, blank=True)

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_book_wishlist(self):
        return self.book_wishlist.get_or_create(user=self)[0]

    def get_diary_wishlist(self):
        return self.diary_wishlist.get_or_create(user=self)[0]

    def full_name(self):
        return ' '.join([self.surname or '', self.name or '', self.patronymic or ''])
    
    def get_current_report(self):
        if hasattr(self, 'chief_in'):
            return Report.get_current(self.chief_in)
        elif hasattr(self, 'admin_in'):
            return Report.get_current(self.admin_in)


    @classmethod
    def has_user(cls, username_field):
        return cls.objects.filter(is_active=True).filter(**{cls.USERNAME_FIELD: username_field.lower()})
    
    @property
    def status(self):
        if hasattr(self, 'chief_in'):
            return 'chief'
        elif hasattr(self, 'admin_in'):
            return 'admin'
        elif self.is_superuser:
            return 'root'
        else:
            return 'missionary'
        
    @property
    def region(self):
        return self.diocese and self.diocese.region
    
    @property
    def country(self):
        return self.region and self.region.country


class Transfer(TimestampModelMixin, models.Model):
    STATUSES = (
        ('created', 'Создан'),
        ('accepted', 'Переведен'),
        ('closed', 'Закрыт'),
    )
    diocese_from = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='Из епархии', on_delete=models.CASCADE, related_name='transfers_from')
    diocese_to = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='В епархию', on_delete=models.CASCADE, related_name='transfers_to')
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='transfers')
    by_user = models.ForeignKey(
        User, verbose_name='Кем переведен', on_delete=models.CASCADE, related_name='inited_transfers')
    
    class Meta:
        verbose_name = 'Трансфер'
        verbose_name_plural = 'Трансферы'

    def __str__(self):
        return f'{self.user.email} из {self.diocese_from.title} в {self.diocese_to.title}({self.status})'
    

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not User.objects.all().exists():
        User.objects.create_superuser(
            email='support@place-start.ru',
            password='chme',
        )
        logger.info("Superuser created")  