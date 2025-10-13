from django.db import models
from django.db.models import Sum, Case, When, F, Q
from django.conf import settings
from django.apps import apps
from rest_framework.exceptions import ValidationError
from core.models import UniversalUserMixin


class Cart(UniversalUserMixin, models.Model):
    """ Модель корзины пользователя """
    SESSION_KEY = 'cart_pk'
    
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины пользователей"

    def __str__(self):
        return f'Корзина пользователя {self.user}' if self.user_id \
                else f'Корзина неавторизованного пользователя ID:{self.pk}'

    @property
    def cart_items(self):
        return self.get_cart_items()

    @property
    def count(self):
        return self.cart_items.count()

    @property
    def total(self):
        total = 0
        for item in self.cart_items:
            total += item.total
        return total

    def get_cart_items(self):
        return self.positions.all().select_related('product').filter(quantity__lte=F('product__quantity'))
    
    def add_item(self, product_id, quantity):
        Product = apps.get_model('catalog', 'Product')
        try:
            product = Product.objects.get(pk=product_id)
        except:
            raise ValidationError({'__all__': ['Товары не выбраны']})
        
        position = {
            'product': product,
        }
            
        if product.quantity < quantity:
            raise ValidationError({'__all__': ['Недостаточно товаров']})
        pos_obj, created = self.positions.get_or_create(**position, defaults={'quantity': quantity})
        if not created:
            if pos_obj.quantity + quantity > product.quantity:
                raise ValidationError({'__all__': ['Недостаточно товаров']})
            pos_obj.quantity = pos_obj.quantity + quantity
            pos_obj.save()

    def clear(self):
        """Очистка корзины"""
        self.cart_items.delete()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='positions')
    product = models.ForeignKey(
        'catalog.Product', verbose_name='Товар', on_delete=models.CASCADE,
        related_name='cart_items')
    quantity = models.PositiveIntegerField(
        verbose_name='Количество', default=1)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        ordering = ('-id',)

    def __str__(self):
        return f"Элемент корзины {self.id} {self.product.title}"

    @property
    def total(self):
        return self.product.price * self.quantity
