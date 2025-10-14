from django.db import models
from django.utils import timezone
from core.models import TimestampModelMixin


class Diary(models.Model, TimestampModelMixin):
    STATUSES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('delited', 'Удален'),
    )
    status = models.CharField(
        verbose_name='Статус', choices=STATUSES, default='draft')
    title = models.CharField(
        verbose_name='Заголовок')
    date = models.DateField(
        verbose_name='Дата', null=True, blank=True)
    place = models.CharField(
        verbose_name='Место проведения', null=True, blank=True)
    member_count = models.CharField(
        verbose_name='Количество участников', null=True, blank=True)
    held_in_diocese = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='Проведено в епархии', related_name='helded_diocese', null=True, blank=True)
    created_by_diocese = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='Создано в епархии', related_name='created_diaries', null=True, blank=True)
    creator = models.ForeignKey(
        'users.User', verbose_name='Создан пользователем', on_delete=models.CASCADE, related_name='diaries')
    type = models.CharField(
        verbose_name='Тип', null=True, blank=True)
    short_description = models.TextField(
        verbose_name='Краткое описание', null=True, blank=True)
    advantages = models.TextField(
        verbose_name='Описание', null=True, blank=True)
    notice = models.TextField(
        verbose_name='Заметки', null=True, blank=True)

    published_at = models.DateTimeField(
        verbose_name='Дата публикации', null=True, blank=True)

    class Meta:

        verbose_name = 'Дневник'
        verbose_name_plural = 'Дневники'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        prev_status = self.status 
        res = super().save(*args, **kwargs)
        if prev_status != 'published' and self.status == 'published':
            self.published_at = timezone.now()
        return res
    

class DiaryImage(models.Model):
    diary = models.ForeignKey(Diary, verbose_name='Дневник', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Изображение', upload_to='images/diary/')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'Изображение №{self.pk}'
    

class Comment(TimestampModelMixin, models.Model):
    author = models.ForeignKey('users.User', verbose_name='Автор', on_delete=models.CASCADE, related_name='comments')
    diary = models.ForeignKey(Diary, verbose_name='Дневник', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий к ${self.diary.title} от ${self.author.email}'
    