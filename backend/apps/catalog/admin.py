from core.models import SeoBase
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib import admin
from . import models


@admin.register(models.AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False


@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False


class AttributeProductInline(admin.TabularInline):
    model = models.AttributeProduct
    extra = 0


class ProductImageInline(admin.TabularInline):
    template = 'admin/widgets/multiupload_stacked.html'
    model = models.ProductImage
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = (
        'pk',
        'title',
        'slug',
        'code',
    )
    inlines = (ProductImageInline, AttributeProductInline, )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'is_active',)
    list_editable = ('is_active',)

    fieldsets = (
        (None, {
            'fields': (
                'is_active', 'title', 'slug',
                'category', 'image', 'code', 'description',
            ),
        }),
        ('Предложение', {
            'fields': (
                ('price', 'price_old'),
                'quantity',
            ),
        }),
        ('Размеры', {
            'fields': (
                'width', 'height', 'weight',
            ),
        }),
        ('SEO', {
            'fields': SeoBase.seo_fields
        })
    )

    def formfield_for_foreignkey(self, db_field, *args, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = models.Category.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()
        for afile in request.FILES.getlist('multifile_ProductImage'):
            obj.gallery.create(image=afile)


@admin.register(models.Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = (
        'pk',
        'title',
        'slug',
    )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'is_active',)
    list_editable = ('is_active',)
    fieldsets = (
        (None, {
            'fields': (
                'is_active', 'title', 'slug', 'description',
                'parent', 'image', 'content',
            )
        }),
        ('SEO', {
            'fields': SeoBase.seo_fields
        })
    )