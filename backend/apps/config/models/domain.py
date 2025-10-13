from django.db import models


class Domain(models.Model):
    is_active = models.BooleanField(verbose_name='Активность', default=True)
    slug = models.CharField(verbose_name='Слаг', unique=True, blank=True, default='')
    name = models.CharField(verbose_name='Имя')

    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'

    def __str__(self):
        return f'{self.name}:{self.slug}'
    
    def get_link(self):
        return f'/{self.slug}' if self.slug else ''