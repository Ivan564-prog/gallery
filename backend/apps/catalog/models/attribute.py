from django.db import models


class AttributeName(models.Model):
    title = models.CharField(verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'Имя атрибута'
        verbose_name_plural = 'Имена атрибутов'

    def __str__(self):
        return self.title
    

class AttributeValue(models.Model):
    value = models.CharField(verbose_name='Значение')

    class Meta:
        verbose_name = 'Значение атрибута'
        verbose_name_plural = 'Значения атрибута'

    def __str__(self):
        return self.value
    

class AttributeProduct(models.Model):
    product = models.ForeignKey(
        'catalog.Product', verbose_name='Продукт', on_delete=models.CASCADE, related_name='attributes',)
    attribute_name = models.ForeignKey(
        AttributeName, verbose_name='Имя атрибута', on_delete=models.CASCADE, related_name='attrs')
    attribute_value = models.ForeignKey(
        AttributeValue, verbose_name='Значение', on_delete=models.CASCADE, related_name='attrs')
    
    class Meta:
        verbose_name = 'Атрибут продукта'
        verbose_name_plural = 'Атрибуты продуктов'

    def __str__(self):
        return f'{self.product.title} - {self.attribute_name.title}: {self.attribute_value.value}'