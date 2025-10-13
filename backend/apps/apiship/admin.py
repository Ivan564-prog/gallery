from django.contrib import admin
from .models import ApishipSettings
from solo.admin import SingletonModelAdmin


# Раскоментить при настройке интеграции
# @admin.register(ApishipSettings)
# class ApishipSettingsAdmin(SingletonModelAdmin):
#     readonly_fields = ('from_city_guid', )