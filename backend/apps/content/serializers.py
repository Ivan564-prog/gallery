from rest_framework import serializers
from . import models
import logging
from apps.pages.models import Page
from apps.catalog.list_serializers.product import ProductListSerializer
from apps.pages.list_serializers import PageListSerializer


logger = logging.getLogger('main')


"""
    Формарование сериалайзеров полностью автоматическое
    При необходимости переопределить какой либо сериалайзер у модели создать сераилизатор с именем как у модели и приставкой Serializer
"""

class HeadingBlockSerializer(serializers.ModelSerializer):
    posts = PageListSerializer(many=True)
    heading = serializers.SlugRelatedField(slug_field='slug', queryset=Page.objects.all())

    class Meta:
        model = models.HeadingBlock
        fields = (
            'id',
            'posts',
        )


class FileItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FileItem
        fields = (
            'file',
            'filename',
            'size',
        )


class ProductBlockSerializer(serializers.ModelSerializer):
    active_products = ProductListSerializer(many=True)

    class Meta:
        model = models.ProductBlock
        fields = (
            'title',
            'active_products',
        )
    

class BaseSubElemSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        if 'model' in kwargs:
            model = kwargs.pop('model')
            super().__init__(*args, **kwargs)
            self.Meta.model = model
        else:
            super().__init__(*args, **kwargs)
            model = self.instance.__class__
            self.Meta.model = model

    class Meta:
        model = None
        fields = '__all__'


class BaseBlockSerializer(serializers.ModelSerializer):
    block_name = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model = self.instance.__class__
        self.Meta.model = model
        self.init_related_fields(model)

    def init_related_fields(self, model):
        fk_fields = [field for field in model._meta.get_fields() if field.get_internal_type() == 'ForeignKey']
        for field in fk_fields:
            subelement_model = getattr(self.instance, field.name).model
            subelement_serializername = subelement_model.__name__ + 'Serializer'
            if subelement_serializername in globals():
                self.fields[field.name] = globals()[subelement_serializername](many=True)
            else:
                self.fields[field.name] = BaseSubElemSerializer(model=subelement_model, many=True)

    def get_block_name(self, obj):
        return 'Block' + obj.__class__.__name__.replace('Block', '')

    class Meta:
        models = None
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Content
        fields = '__all__'

    def _serialize(self, obj, model):
        custom_serializer_name = model.__name__ + 'Serializer'
        if custom_serializer_name in globals():
            data = globals()[custom_serializer_name](obj, context=self.context).data
            data['block_name'] = 'Block' + obj.__class__.__name__.replace('Block', '')
        else:
            data = BaseBlockSerializer(obj, context=self.context).data
        return data

    def to_representation(self, instance):
        output = []
        model_list = instance.stream.model_list
        for elem in instance.stream.value:
            for model in model_list:
                if model.__name__ == elem['model_name']:
                    id = elem['id']
                    if id > 0:
                        obj = model.objects.get(id=id)
                        output.append(self._serialize(obj, model))
        return output