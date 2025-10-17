from django.db import models
from core.models import TimestampModelMixin


class Notification(TimestampModelMixin, models.Model):

    title = models.CharField(
        verbose_name='Заголовок')
    text = models.TextField(
        verbose_name='Текст')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.title
    
    @property
    def chiefs_notices(self):
        return self.notices.filter(user__chief_in__isnull=False)
    

class Notice(TimestampModelMixin, models.Model):
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name='notices')
    user = models.ForeignKey(
        'users.User', verbose_name='Пользователь', on_delete=models.CASCADE, related_name='notices')
    is_viewed = models.BooleanField(
        verbose_name='Просмотрен', default=False)
    
    class Meta:
        verbose_name = 'Уведомление пользователя'
        verbose_name_plural = 'Уведомления пользователей'
        unique_together = (('notification', 'user'), )

    def __str__(self):
        return f'Уведомление "{self.notification.title}" для {self.user}'
    
    @property
    def title(self):
        return self.notification.title
    
    @property
    def text(self):
        return self.notification.text