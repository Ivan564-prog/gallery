from apps.feedback.models import AdminEmail
from apps.config.models import RootSettings
from core.helpers import send_mail
from django.db import models
from django.template.loader import render_to_string
from core.models import TimestampModelMixin


class OrderPayment(models.Model):
    PAYMENT_TYPES = (
        ('upon_receipt', 'При получении'),
        ('requisites', 'По реквизитам')
    )
    payment_type = models.CharField(
        verbose_name='Тип оплаты', null=True, choices=PAYMENT_TYPES)
    payed = models.BooleanField(
        verbose_name='Оплачен', default=False)

    class Meta:
        abstract = True

    def get_payment_params(self):
        return {
            'Тип оплаты': self.get_payment_type_display(),
        }


class OrderDelivery(models.Model):
    DELIVERY_TYPES = (
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка')
    )

    delivery_type = models.CharField(
        verbose_name='Тип доставки', max_length=255, null=True)
    delivery_price = models.PositiveIntegerField(
        verbose_name='Стоимость доставки', default=0)
    delivery_address = models.TextField(
        verbose_name='Адрес доставки', blank=True, null=True)

    class Meta:
        abstract = True

    def get_delivery_price(self):
        return self.delivery_price
    
    def get_delivery_params(self):
        params = {
            'Тип доставки': self.get_delivery_price_display(),
        }
        if self.delivery_type != 'Самовывоз':
            params['Стоимость доставки'] = self.get_delivery_price() or 'Бессплатно'
            params['Адрес доставки'] = self.delivery_address
        return params


class Order(
        TimestampModelMixin,
        # OrderDelivery
        # OrderPayment
        models.Model,
    ):
    user = models.ForeignKey(
        'users.User', verbose_name='Пользовтель', on_delete=models.PROTECT, related_name='orders', null=True, blank=True)
    name = models.CharField(
        verbose_name='Имя', max_length=255)
    email = models.CharField(
        verbose_name='Почта', max_length=255, null=True)
    phone = models.CharField(
        verbose_name='Телфеон', max_length=25)
    comment = models.TextField(
        verbose_name='Комментарий', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.pk}'
    
    def get_delivery_price(self):
        """ При использовании доставки должен переопределятся из класса OrderDelivery """
        if hasattr(super(), 'get_delivery_price'):
            return super().get_delivery_price()
        return 0
    
    def get_delivery_params(self):
        """ При использовании доставки должен переопределятся из класса OrderDelivery """
        if hasattr(super(), 'get_delivery_params'):
            return super().get_delivery_params()
        return {}
    
    def get_payment_params(self):
        """ При использовании доставки должен переопределятся из класса OrderPayment """
        if hasattr(super(), 'get_payment_params'):
            return super().get_payment_params()
        return {}

    def get_email_params(self):
        params = {
            'ФИО': self.name,
            'Email': self.email,
            'Телефон': self.phone,
            'Комментарий к заказу': self.comment,
            **self.get_delivery_params(),
            **self.get_payment_params(),
        }
        return params

    @property
    def total(self):
        total = 0
        for position in self.positions.all():
            total += position.total
        total += self.get_delivery_price()
        return total
    
    def repeat(self):
        for item in self.positions.all():
            item.repeat()

    def send_notify(self, request):
        self._send_admin_notify(request)
        self._send_user_notify(request)

    def _send_admin_notify(self, request):
        subject = f'Заказ № {self.pk}'
        html_message = render_to_string(
            'mails/order.html', 
            {
                'order': self,
                'request': request,
                'admin': True,
                'settings': RootSettings.get_settings(),
            }
        )
        to = [ae.email for ae in AdminEmail.objects.all()]
        send_mail.delay(subject, to, html_message)

    def _send_user_notify(self, request):
        subject = f'Заказ № {self.pk}'
        html_message = render_to_string(
            'mails/order.html', 
            {
                'order': self,
                'request': request,
                'settings': RootSettings.get_settings(),
            }
        )
        to = [self.email]
        send_mail.delay(subject, to, html_message)


class OrderItem(TimestampModelMixin, models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='positions')
    product = models.ForeignKey(
        'catalog.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(
        verbose_name='Количество')
    price = models.PositiveIntegerField(
        verbose_name='Цена')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'Элемент заказ №{self.pk}'

    @property
    def total(self):
        return self.quantity * self.price
    
    def repeat(self):
        self.order.user.cart.add_item(
            product_id=self.product.pk,
            quantity=self.quantity,
        )