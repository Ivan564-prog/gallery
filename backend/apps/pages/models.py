from django.db import models
from core.managers import ActivedManager
from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel):
    is_active = models.BooleanField(
        verbose_name='Активность', max_length=255, default=True)
    title = models.CharField(
        verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(
        verbose_name='Слаг', max_length=255, unique=True)
    content = models.ForeignKey(
        'content.Content', verbose_name='Контент', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(
        verbose_name='Изображение', max_length=255, upload_to='images/pages/', null=True, blank=True)

    parent = TreeForeignKey(
        'self', verbose_name='Родительская страница', related_name='subpages', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(
        verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Обновлен', auto_now=True)
    
    objects = ActivedManager()

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title

    @property
    def link(self):
        return self.get_absolute_url()

    @property
    def breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        del breadcrumbs[-1]['link']
        return breadcrumbs
    
    def get_breadcrumbs(self):
        breadcrumbs = self.parent.breadcrumbs if self.parent else []
        breadcrumbs.append({
            'title': self.title,
            'link': self.link,
        })
        return breadcrumbs


    def get_absolute_url(self):
        return f'/{self.slug}'