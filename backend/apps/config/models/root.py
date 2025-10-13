from django.db import models
from solo.models import SingletonModel
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from admin_interface.models import Theme


class SocialNetworkSettings(models.Model):
    vk_link = models.CharField(
        verbose_name='Ссылка на ВКонтакте', max_length=255, null=True, blank=True)
    tg_link = models.CharField(
        verbose_name='Ссылка на Телеграм', max_length=255, null=True, blank=True)
    wa_link = models.CharField(
        verbose_name='Ссылка на WhatsApp', max_length=255, null=True, blank=True)
    
    class Meta:
        abstract = True


class RootSettings(SocialNetworkSettings, SingletonModel):
    address = models.CharField(
        verbose_name='Адрес', max_length=255, null=True)
    phone = models.CharField(
        verbose_name='Телефон', max_length=255, null=True)
    email = models.CharField(
        verbose_name='Почта', max_length=255, null=True)
    company_name = models.CharField(
        verbose_name='Имя компании')

    scripts = models.TextField(
        verbose_name='Скрипты', null=True, blank=True)
    robots = models.TextField(default='User-agent: *\nDisallow: /')

    class Meta:
        verbose_name = 'Основные настройки'
        verbose_name_plural = 'Основные настройки'

    def __str__(self):
        return f'Основные настройки'

    @classmethod
    def get_settings(cls):
        if not cls.objects.all().exists():
            cls.objects.create()
        return cls.objects.get()



@receiver(post_migrate)
def set_django_admin_settings(sender, **kwargs):
    theme = Theme.objects.get_active()
    theme.show_inlines_as_tabs = True
    theme.save()