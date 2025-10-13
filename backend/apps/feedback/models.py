from django.db import models
from core.models import TimestampModelMixin


class Feedback(TimestampModelMixin, models.Model):
    email = models.CharField(
        verbose_name='Почта', max_length=255, null=True)
    phone = models.CharField(
        verbose_name='Телефон', max_length=255, null=True)
    name = models.CharField(
        verbose_name='Имя', max_length=255, null=True)
    product = models.ForeignKey(
        'catalog.Product', related_name='Продукт', on_delete=models.PROTECT, null=True, blank=True)
    extra = models.TextField(
        verbose_name='Дополнительно', null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    
    def __str__(self):
        return f'Заявка №{self.pk} от {self.email}'

    def get_extra(self):
        return self.extra and self.extra.replace('\n', '\n<br>\n')
    
    def get_email_params(self):
        return {
            'Почта': self.email,
            'Телефон': self.phone,
            'Имя': self.name,
            'Продукт': self.product and self.product.title,
            'Дополнительно': self.get_extra(),
        }

        
class AdminEmail(TimestampModelMixin, models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name = 'Почта администратора'
        verbose_name_plural = 'Почты администраторов'

    def __str__(self):
        return self.email