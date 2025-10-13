from django.db import models
from django.utils.functional import cached_property
from core.models import UniversalUserMixin
from apps.catalog.models import Product


class Wishlist(UniversalUserMixin, models.Model):
    """ Модель корзины пользователя """
    SESSION_KEY = 'wishlist_pk'
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Избранные товары"
        verbose_name_plural = "Избранные товары пользователей"

    def __str__(self):
        return f'Избранные пользователя {self.user}' if self.user_id \
                else f'Избранные неавторизованного пользователя ID:{self.pk}'
    
    @cached_property
    def products(self):
        return Product.objects.active().filter(wishlist_items__in=self.items.all())

    def toggle(self, product, **kwargs):
        """ Добавление товара в избранные """
        try:
            item = WishlistItem.objects.get(wishlist=self, product=product)
            self.remove(item)
        except WishlistItem.DoesNotExist:
            item = WishlistItem.objects.create(wishlist=self, product=product)

    def clear(self):
        """ Очистка """
        self.items.all().delete()


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.CASCADE,
        related_name='wishlist_items')

    class Meta:
        verbose_name = "Элемент избранных товаров"
        verbose_name_plural = "Элементы избранных товаров"
        ordering = ('-id',)

    def __str__(self):
        return f'Элемент корзины {self.id} {self.product.title}'
