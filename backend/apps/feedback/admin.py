from django.contrib import admin
from . import models


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )


@admin.register(models.AdminEmail)
class AdminEmailAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )