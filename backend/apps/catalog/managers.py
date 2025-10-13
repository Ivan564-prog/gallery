from django.db import models
import re
import logging
from apps.carts.models import Cart


logger = logging.getLogger('main')


class CategoryQueryset(models.QuerySet):
    
    def active(self):
        return self.filter(is_active=True)


class CategoryManager(models.Manager):

    def get_queryset(self):
        return CategoryQueryset(self.model)

    def active(self):
        return self.get_queryset().active()
    

class ProductQueryset(models.QuerySet):

    ATTRIBUTE_PATTERN = r'a\d+'
    ORDERINGS = [
        'title',
        'popular',
        'price',
        '-price',
    ]
    
    def active(self):
        return self.filter(is_active=True)

    def _filter_by_attribute(self, name_id, value_ids):
        query = models.Q(
            attributes__attribute_name__id=name_id,
            attributes__attribute_value__id=value_ids[0]
        )
        for value_id in value_ids[1:]:
            query |= models.Q(
                attributes__attribute_name__id=name_id,
                attributes__attribute_value__id=value_id
            )
        return self.filter(query)
    
    def _filter_by_attributes(self, request):
        for key in request.GET.keys():
            if re.fullmatch(self.ATTRIBUTE_PATTERN, key):
                try:
                    self._filter_by_attribute(key.replace('a',''), request.GET.getlist(key))
                except:
                    pass
        return self
    
    def _filter_by_query(self, request):
        query = request.GET.get('query', None)
        if query is not None:
            if len(query) > 1:
                self = self.filter(models.Q(title__icontains=query) | models.Q(code__icontains=query))
            else:
                self = self.none()
        return self
    
    def _filter_by_static_attributes(self, request):
        if 'hit' in request.GET and request.GET['hit'] != 'false':
            self = self.queryset.filter(is_hit=True)
        if 'new' in request.GET and request.GET['new'] != 'false':
            self = self.queryset.filter(is_new=True)
        if 'sale' in request.GET and request.GET['sale'] != 'false':
            self = self.queryset.filter(price_old__gt=0)
        return self
    
    def _filter_by_price(self, request):
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)
        if min_price is not None and min_price.isdigit():
            self = self.filter(price__gte=int(min_price))
        if max_price is not None and max_price.isdigit():
            self = self.filter(price__lte=int(max_price))
        return self
    
    def get_extremum_prices(self):
        return self.aggregate(min_price=models.Min('price'), max_price=models.Max('price'))
    
    def get_attributes(self):
        self = self.prefetch_related('attributes__attribute_name', 'attributes__attribute_value')
        attributes = {}
        for product in self:
            for attribute in product.attributes.all():
                if not attribute.attribute_name.id in attributes:
                    attributes[attribute.attribute_name.id] = {
                        'id': attribute.attribute_name.id,
                        'title': attribute.attribute_name.title,
                        'values': {}
                    }
                if not attribute.attribute_value.id in attributes[attribute.attribute_name.id]['values']:
                    attributes[attribute.attribute_name.id]['values'][attribute.attribute_value.id] = {
                        'id': attribute.attribute_value.id,
                        'value': attribute.attribute_value.value,
                    }
        result = []
        for attribute in attributes.values():
            result.append({
                'id': attribute['id'],
                'title': attribute['title'],
                'values': list(attribute['values'].values())
            })
        return result
    
    def annotate_cart_count(self, request):
        cart = Cart.get_from_request(request)
        cart_count_subquery = cart.positions.filter(product=models.OuterRef('id')).values('quantity')[:1]
        return self.annotate(cart_quantity=models.functions.Coalesce(models.Subquery(cart_count_subquery), models.Value(0)))
    
    def filter_by_request(self, request):
        self = self._filter_by_query(request)
        self = self._filter_by_price(request)
        self = self._filter_by_static_attributes(request)
        self = self._filter_by_attributes(request)
        return self

    def order_by_request(self, request):
        ordering = request.GET.get('ordering', None)
        return self.order_by(ordering if ordering in self.ORDERINGS else 'popular')


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQueryset(self.model)

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def filter_by_request(self, request):
        return self.get_queryset().filter_by_request(request)

    def order_by_request(self, request):
        return self.get_queryset().order_by_request(request)