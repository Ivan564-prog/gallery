from django.db import models
from solo.models import SingletonModel
from dadata import Dadata


class ApishipSettings(SingletonModel):
    dadata_token = models.CharField(verbose_name='Dadata token', null=True)
    dadata_secret = models.CharField(verbose_name='Dadata secret', null=True)
    
    from_city = models.CharField(verbose_name='Город отправления', null=True, blank=True)
    from_city_guid = models.CharField(verbose_name='GUID города', null=True, blank=True)

    apiship_token = models.CharField(verbose_name='Apiship token', null=True)

    class Meta:
        verbose_name = 'Настройки apiship'
        verbose_name_plural = 'Настройки apiship'

    def __str__(self):
        return 'Настройки apiship'

    @classmethod
    def get_settings(cls):
        if not cls.objects.all().exists():
            cls.objects.create()
        return cls.objects.get()
    
    def get_dadata(self):
        return Dadata(self.dadata_token, self.dadata_secret)
    
    def save(self, *args, **kwargs):
        if self.from_city and not self.from_city_guid:
            self.from_city_guid = self.get_dadata().suggest(name="address", query=self.from_city)[0]['data']['city_fias_id']
        elif not self.from_city:
            self.from_city_guid = ''
            
        return super().save(*args, **kwargs)