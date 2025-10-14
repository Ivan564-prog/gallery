from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Metropolis)
class MetropolisAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Diocese)
class DioceseAdmin(admin.ModelAdmin):
    pass