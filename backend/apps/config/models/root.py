from django.db import models
from solo.models import SingletonModel
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from admin_interface.models import Theme
from core.models import TimestampModelMixin
from core.logger import logger


class RootSettings(TimestampModelMixin, SingletonModel):
    address = models.CharField(
        verbose_name='Адрес', max_length=255, null=True)
    phone = models.CharField(
        verbose_name='Телефон', max_length=255, null=True)
    email = models.CharField(
        verbose_name='Почта', max_length=255, null=True)
    company_name = models.CharField(
        verbose_name='Имя компании')
    logo = models.ImageField(
        verbose_name='Логотип', upload_to='images/settings/', null=True)
    favicon = models.ImageField(
        verbose_name='Фавикон', upload_to='images/settings/', null=True)

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
    if sender.name != 'apps.config':
        return
    theme = Theme.objects.get_active()
    theme.show_inlines_as_tabs = True
    theme.save()