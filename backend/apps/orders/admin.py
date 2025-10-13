
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    exclude = ('created_at', 'updated_at',)


# @admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, )
    exclude = ('created_at', 'updated_at',)