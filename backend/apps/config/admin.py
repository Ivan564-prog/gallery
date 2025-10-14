from django.contrib import admin
from . import models
from solo.admin import SingletonModelAdmin


@admin.register(models.RootSettings)
class RootSettingsAdmin(SingletonModelAdmin):
    
    fieldsets = (
        (None, {
            'fields': (
                ('address', 'email'),
                ('phone', 'company_name'),
                ('logo', 'favicon'),
                'scripts',
                'robots',
            ),
        }),
        ('Социальные сети', {
            'fields': (
                'vk_link',
                'rt_link',
                'mx_link',
                'yt_link',
                'tg_link',
                'wa_link',
                'dz_link',
                'ok_link',
            ),
        }),
    )
    exclude = (
        'created_at',
        'updated_at',
    )


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