from django.db import models
from solo.models import SingletonModel
from core.models import SeoBase


class IndexSettings(SingletonModel, SeoBase):
    content = models.ForeignKey(
        'content.Content', verbose_name='Контент', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Настройки главной'
        verbose_name_plural = 'Настройки главной'

    def __str__(self):
        return 'Настройки главной'

    @classmethod
    def get_settings(cls):
        if not cls.objects.all().exists():
            cls.objects.create()
        return cls.objects.get()