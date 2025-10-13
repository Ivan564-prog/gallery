from django.contrib import admin
from . import models
from solo.admin import SingletonModelAdmin


@admin.register(models.RootSettings)
class RootSettingsAdmin(SingletonModelAdmin):
    pass


@admin.register(models.IndexSettings)
class IndexSettingsAdmin(SingletonModelAdmin):
    fields = (
        'content',
        'meta_title',
        'meta_description',
    )


# Раскоментить при настройке интеграции
# @admin.register(models.Bot)
# class BotAdmin(SingletonModelAdmin):
#     pass


# Раскоментить при использовании доменов
# @admin.register(models.Domain)
# class DomainAdmin(admin.ModelAdmin):
#     pass


# Скрытие из админки стандартных моделей
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy
from admin_interface.models import Theme


admin.site.unregister(Group)
admin.site.unregister(Theme)
try:
    admin.site.unregister(TokenProxy)
except:
    pass