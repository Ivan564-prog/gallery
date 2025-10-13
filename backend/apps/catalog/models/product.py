from core.models import SeoBase
from django.db import models
from tinymce.models import HTMLField
from ..managers import ProductManager
from core.models import TimestampModelMixin


class ProductDelivery(models.Model):
    width = models.PositiveIntegerField(verbose_name='Ширина', default=0)
    height = models.PositiveIntegerField(verbose_name='Высота', default=0)
    length = models.PositiveIntegerField(verbose_name='Длина', default=0)
    weight = models.PositiveIntegerField(verbose_name='Вес', default=0)

    class Meta:
        abstract = True


class Product(SeoBase, ProductDelivery, TimestampModelMixin):

    is_active = models.BooleanField(
        verbose_name='Активность', default=True)
    title = models.CharField(
        verbose_name='Заголовок', max_length=255)
    slug = models.CharField(
        verbose_name='Слаг', max_length=255, unique=True)
    code = models.CharField(
        verbose_name='Артикул', null=True, blank=True)
    
    is_hit = models.BooleanField(
        verbose_name='Хит', default=True)
    is_new = models.BooleanField(
        verbose_name='Новинка', default=True)
    
    category = models.ForeignKey(
        'catalog.Category', verbose_name='Категории', on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(
        verbose_name='Изображение', max_length=255, upload_to='images/product/', null=True, blank=True)
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)
    
    content = models.ForeignKey(
        'content.Content', verbose_name='Контент', on_delete=models.SET_NULL, null=True, blank=True)

    price = models.PositiveIntegerField(
        verbose_name='Цена', default=0)
    price_old = models.PositiveIntegerField(
        verbose_name='Старая цена', default=0)
    quantity = models.PositiveIntegerField(
        verbose_name='Количество', default=0)

    popular = models.PositiveIntegerField(
        verbose_name='Посещения', default=0)
    
    objects = ProductManager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return f'{self.category.get_absolute_url()}/{self.slug}'
    
    def visite(self):
        self.popular += 1
        self.save()
    
    @property
    def breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        del breadcrumbs[-1]['link']
        return breadcrumbs
    
    def get_breadcrumbs(self):
        breadcrumbs = self.category.get_breadcrumbs()
        breadcrumbs.append({
            'title': self.title,
            'link': self.link,
        })
        return breadcrumbs
    
    @property
    def link(self):
        return self.get_absolute_url()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(
        verbose_name='Изображение', max_length=255, upload_to='images/product-gallery/')
    
    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural = 'Элемент галлереи'

    def __str__(self):
        return f'Элемент галлереи №{self.pk}'