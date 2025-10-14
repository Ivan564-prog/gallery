from django.contrib import admin
from . import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BookType)
class BookTypeAdmin(admin.ModelAdmin):
    pass