from django.contrib import admin
from . import models


@admin.register(models.Quarter)
class QuarterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    pass