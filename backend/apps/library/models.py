from django.db import models
from core.models import TimestampModelMixin
from django.utils import timezone
from datetime import timedelta


class BookType(models.Model):
    title = models.CharField(verbose_name='Название')

    class Meta:
        verbose_name = 'Тип книги'
        verbose_name_plural = 'Типы книги'

    def __str__(self):
        return self.title


class Book(TimestampModelMixin, models.Model):
    STATUSES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('delited', 'Удален'),
    )
    status = models.CharField(
        verbose_name='Статус', choices=STATUSES, default='draft')
    title = models.CharField(
        verbose_name='Заголовок')
    type = models.ForeignKey(
        BookType, verbose_name='Тип', related_name='books', on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='Изображение', upload_to='images/book/', null=True, blank=True)
    short_description = models.TextField(
        verbose_name='Краткое описание', null=True, blank=True)
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True)
    file = models.FileField(
        verbose_name='Файл', upload_to='files/book/', null=True, blank=True)
    published_at = models.DateTimeField(
        verbose_name='Дата публикации', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        prev_status = self.status 
        res = super().save(*args, **kwargs)
        if prev_status != 'published' and self.status == 'published':
            self.published_at = timezone.now()
        elif self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        return res
    
    @property
    def is_new(self):
        return (self.published_at + timedelta(days=14)) > timezone.now() if self.published_at else False
    
    def get_similar(self):
        return self.type.books.filter(status='published').exclude(pk=self.pk)
