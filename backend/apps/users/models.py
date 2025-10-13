from .managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import timedelta
from core.logger import logger
from core.helpers import send_mail
import random
import string


class AbstractCompanyUser(models.Model):

    company_name = models.CharField(
        verbose_name='Название компании', max_length=255)
    company_inn = models.CharField(
        verbose_name='ИНН', max_length=20)
    company_kpp = models.CharField(
        verbose_name='КПП', max_length=20, null=True, blank=True)
    company_ogrn = models.CharField(
        verbose_name='ОГРН', max_length=20, null=True, blank=True)
    
    class Meta:
        abstract = True


class AbastractAdditionalInfo(models.Model):

    full_name = models.CharField(
        verbose_name='Полное имя', max_length=255)
    additional_email = models.EmailField(
        verbose_name='Доп. почта', max_length=255, null=True, blank=True)
    phone = models.CharField(
        verbose_name='Телефон', max_length=255)

    class Meta:
        abstract = True


class AccountActivation(models.Model):

    activation_code = models.CharField(
        verbose_name='Код активации', null=True, blank=True)
    activation_deadline = models.DateTimeField(
        verbose_name='Время до конца активации', null=True, blank=True)

    class Meta:
        abstract = True
    
    def _generate_activation_code(self):
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(16))
        self.activation_code = code
        self.activation_deadline = timezone.now() + timedelta(hours=1)
        self.save()
        return code
    
    def send_activation_code(self, request):
        self._generate_activation_code()
        subject = f'Подтверждение адреса электронной почты'
        html_message = render_to_string(
            'mails/register-confirm.html',
            {
                'request': request,
                'confirm_link': f'{request.scheme}://{request.get_host()}/account-confirm?id={self.pk}&code={self.activation_code}',
            }
        )
        to = [self.email]
        send_mail.delay(subject, to, html_message)


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
        # AbastractAdditionalInfo, 
        # AbstractCompanyUser,
        ResetPassword,
        AccountActivation,
        AbstractUser
    ):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    first_name = None
    last_name = None
    
    is_active = models.BooleanField(
        'Активность', default=False)
    task_permission = models.BooleanField(
        'Доступ к задачам', default=False)
    email = models.EmailField(
        verbose_name='Почта', max_length=255, unique=True)

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
    
    @classmethod
    def has_user(cls, email):
        return cls.objects.filter(is_active=True).filter(**{cls.USERNAME_FIELD: email.lower()})


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not User.objects.all().exists():
        User.objects.create_superuser(
            email='support@place-start.ru',
            password='chme',
            task_permission=True,
        )
        logger.info("Superuser created")  