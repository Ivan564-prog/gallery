from django.contrib import admin
from . import models


class PageTypeListFilter(admin.SimpleListFilter):
    title = 'Тип страницы'
    parameter_name = 'page_type'

    def lookups(self, request, model_admin):
        return [
            ('headings', 'Рубрики'),
            ('posts', 'Посты'),
            ('pages', 'Страницы'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'posts':
            queryset = queryset.filter(parent__isnull=False).distinct()
        elif self.value() == 'pages':
            queryset = queryset.filter(parent__isnull=True, subpages__isnull=True).distinct()
        elif self.value() == 'headings':
            queryset = queryset.filter(parent__isnull=True, subpages__isnull=False).distinct()
        return queryset


class HeadingListFilter(admin.SimpleListFilter):
    title = 'Рубрика'
    parameter_name = 'heading'

    def lookups(self, request, model_admin):
        return [(heading.pk, heading.title) for heading in models.Page.objects.filter(parent__isnull=True, subpages__isnull=False).distinct()]

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(parent__pk=self.value())
        return queryset


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active', PageTypeListFilter, HeadingListFilter)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}