from django.contrib import admin
from streamfield.admin import StreamBlocksAdmin
from . import models


""" Для переопределения admin класса создайте класс с именем <ModelName>Admin он автоматически переопределит необходимый класс """


class BaseBlock(StreamBlocksAdmin):

    def has_module_permission(self, request):
        return False


class GalleryItemAdmin(admin.TabularInline):
    template = 'admin/widgets/multiupload_stacked.html'
    model = models.GalleryItem
    extra = 0


@admin.register(models.GalleryBlock)
class GalleryBlockAdmin(BaseBlock):
    inlines = (GalleryItemAdmin, )

    def save_model(self, request, obj, form, change):
        obj.save()
        for afile in request.FILES.getlist('multifile_GalleryItem'):
            obj.images.create(image=afile)


class FileItemAdmin(admin.TabularInline):
    model = models.FileItem
    extra = 0


@admin.register(models.FileBlock)
class FileBlockAdmin(BaseBlock):
    inlines = (FileItemAdmin, )


""" Авто формирование блоков """
# фабрика админ классов
def get_base_block(many_to_many_fields, inline_list):
    class BaseBlock(StreamBlocksAdmin):
        filter_horizontal = many_to_many_fields
        inlines = inline_list

        def has_module_permission(self, request):
            return False
    return BaseBlock


# фабрика админ инлайнов
def get_base_inline(inline_model):
    class BaseTabularInline(admin.TabularInline):
        model = inline_model
        extra = 0
    return BaseTabularInline


for content_block in models.get_content_blocks():
    if globals().get(f'{content_block.__name__}Admin'):
        continue
    many_to_many_fields = []
    inline_list = []
    for field in content_block._meta.get_fields():
        if field.__class__.__name__ == 'ManyToManyField':
            many_to_many_fields.append(field.name)
        elif field.__class__.__name__ == 'ManyToOneRel':
            inline_list.append(get_base_inline(field.related_model))
    admin.site.register(content_block, get_base_block(many_to_many_fields, inline_list))


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    pass