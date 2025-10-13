from core.models import SeoBase
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ..managers import CategoryManager


class Category(MPTTModel, SeoBase):
    is_active = models.BooleanField(
        verbose_name='Активность', default=True)
    title = models.CharField(
        verbose_name='Название', max_length=255)
    slug = models.SlugField(
        verbose_name='Cлаг', max_length=255, unique=True)
    parent = TreeForeignKey(
        'self', verbose_name='Родительская категория', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    image = models.ImageField(
        verbose_name='Изображение', upload_to='images/category/', max_length=255, null=True, blank=True)
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True)
        
    content = models.ForeignKey(
        'content.Content', verbose_name='Контент', on_delete=models.SET_NULL, null=True, blank=True)

    sort = models.PositiveIntegerField(
        verbose_name='Сортировка', default=0)
    created_at = models.DateTimeField(
        verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Обновлен', auto_now=True)
    
    objects = CategoryManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('sort',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/catalog/{self.slug}'

    def get_products(self):
        return self.products.active().filter(category__in=self.get_descendants(include_self=True).filter(is_active=True))
    
    @property
    def attributes(self):
        return self.get_products().get_attributes()
    
    @property
    def extremum_prices(self):
        return self.get_products().get_extremum_prices()
    
    @property
    def product_count(self):
        return self.get_products().count()

    @property
    def breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        del breadcrumbs[-1]['link']
        return breadcrumbs
    
    def get_breadcrumbs(self):
        breadcrumbs = [{
            'title': 'Каталог',
            'link': '/catalog'
        }]
        if self.parent:
            breadcrumbs = self.parent.get_breadcrumbs()
        breadcrumbs.append({
            'title': self.title,
            'link': self.link,
        })
        return breadcrumbs

    @property
    def link(self):
        return self.get_absolute_url()