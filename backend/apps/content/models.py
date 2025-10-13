from django.db import models
from streamfield.fields import StreamField
from tinymce.models import HTMLField
import os


def get_content_blocks():
    blocks = [
        SeoBlock,
        GalleryBlock,
        ProductBlock,
        FileBlock,
        HeadingBlock,
    ]
    for key, value in globals().items():
        if key[-5:] == 'Block' and not value in blocks:
           blocks.append(value) 

    return blocks

"""
    Блоки называть по типу <ИмяБлока>Block
    Имя блока на фронте формируется по принципу Block<ИмяБлока>
    Так же по этому паттерну блоки попадают в model_list streamfield`а
"""


class HeadingBlock(models.Model):
    title = models.CharField(verbose_name='Заголовок', null=True, blank=True)
    heading = models.ForeignKey('pages.Page', on_delete=models.CASCADE, verbose_name='Рубрика')
    limit = models.PositiveIntegerField(verbose_name='Ограничение', default=0)

    class Meta:
        verbose_name = 'Блок рубрики'
        verbose_name_plural = 'Блоки рубрики'

    def __str__(self):
        return f'Блок рубрики {self.heading.title}'
    
    @property
    def subpages(self):
        if self.limit:
            return self.heading.subpages.active()[:self.limit]


class FileBlock(models.Model):
    title = models.CharField(verbose_name='Заголовок', null=True, blank=True)

    class Meta:
        verbose_name = 'Блок с файлами'
        verbose_name_plural = 'Блоки с файлами'
    
    def __str__(self):
        return f'Блок с файлами №{self.pk}'
    

class FileItem(models.Model):
    block = models.ForeignKey(
        FileBlock, related_name='items', on_delete=models.CASCADE)
    file = models.FileField(
        verbose_name='Файл')
    name = models.CharField(
        verbose_name='Имя файла', null=True, blank=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return f'Файл №{self.name}'
    
    @property
    def filename(self):
        return self.name + '.' + self.file.name.split('.')[-1] if self.name else self.file.name
    
    @property
    def size(self):
        size = os.path.getsize(self.file.path)
        if size < 512000:
            size = size / 1024.0
            ext = 'Кб'
        elif size < 4194304000:
            size = size / 1048576.0
            ext = 'Мб'
        else:
            size = size / 1073741824.0
            ext = 'Гб'
        return f'{size:.2f} {ext}'


class ProductBlock(models.Model):
    title = models.CharField(verbose_name='Заголовок', null=True, blank=True)
    products = models.ManyToManyField('catalog.Product', verbose_name='Продукты', )

    class Meta:
        verbose_name = 'Блок продуктов'
        verbose_name_plural = 'Блоки продуктов'

    @property
    def active_products(self):
        return self.product.active()


class GalleryBlock(models.Model):
    IN_LINE_CHOICES = (
        # ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        # ('5', '5'),
    )
    in_line = models.CharField(verbose_name='Элементов в линии', max_length=1, default='3', choices=IN_LINE_CHOICES)

    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural = 'Галлереи'

    def __str__(self):
        return f'Галлерея №{self.pk}'


class GalleryItem(models.Model):
    gallery = models.ForeignKey(GalleryBlock, verbose_name='Галлерея', on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(verbose_name='Изображение', max_length=500, upload_to='content/gallery/')
    title = models.CharField(verbose_name='Подпись', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Элемент галлереи'
        verbose_name_plural = 'Элементы галлереи'

    def __str__(self):
        return f'Элемент галлереи {self.title if self.title else "№" + str(self.pk)}'


class SeoBlock(models.Model):
    LEFT = 'left'
    RIGHT = 'right'
    POSITIONS = (
        (LEFT, 'Слева'),
        (RIGHT, 'Справа'),
    )

    text = HTMLField(verbose_name='Текст')
    image = models.ImageField(verbose_name='Изображение', upload_to='images/content/', max_length=255, null=True, blank=True)
    position = models.CharField(verbose_name='Положение изображения', choices=POSITIONS, default=RIGHT)

    class Meta:
        verbose_name = 'Сео блок'
        verbose_name_plural = 'Сео блоки'
    
    def __str__(self):
        return f'СЕО-блок №{self.pk}'


class Content(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    stream = StreamField(model_list=get_content_blocks(), verbose_name="Содержимое")

    def __str__(self):
        return f'Контент: {self.title}'

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'
