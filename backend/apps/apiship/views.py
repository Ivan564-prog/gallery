from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import ApishipSettings
from apps.carts.models import Cart
import requests


class ApishipViewSet(ViewSet):
    queryset = ApishipSettings.objects.all()
    apiship_url = 'https://api.apiship.ru/v1'

    def __init__(self, *args, **kwargs):
        self.apiship_settings = ApishipSettings.get_settings()
        self.session = requests.Session()
        self.session.encoding = 'utf-8'
        self.session.headers['Authorization'] = self.apiship_settings.apiship_token
        return super().__init__(*args, **kwargs)

    @action(detail=False, methods=['GET'], url_path='address')
    def get_address(self, request):
        query = request.GET.get('query', '')
        response = self.apiship_settings.get_dadata().suggest(name="address", query=query)
        addresses = list(filter(lambda itm: itm["data"]["city_fias_id"] != None and itm["data"]["geo_lat"] != None and itm["data"]["geo_lon"] != None, response))
        return Response([{
            'id': address['data']['city_fias_id'],
            'name': address['value'],
        } for address in addresses])
    
    @action(detail=False, methods=['GET'], url_path='delivery_points')
    def get_delivery_points(self, request):
        if not self.apiship_settings.from_city_guid:
            return Response({'message': 'Не полные настройки интеграции apiship'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        providers = self.get_providers(request)
        return Response(self.get_points(providers))
    
    def get_points(self, providers):
        result = []
        for provider in providers:
            if not provider['tariffs']:
                continue
            min_tarif = min(provider['tariffs'], key=lambda x: x['deliveryCost'])
            points = self.session.get(self.apiship_url + f'/lists/points', params={'filter': "id=" + str(min_tarif["pointIds"])}).json()['rows']
            for point in points:
                result.append({
                    "id": point['id'],
                    "provider": point['providerKey'],
                    "address": point['address'],
                    "timetable": point['timetable'],
                    "timetable": point['timetable'],
                    "price": min_tarif['deliveryCost'],
                    "coorinate": f"{point['lat']},{point['lng']}",
                })
        return result
    
    def get_providers(self, request):
        cart = Cart.get_from_request(request)
        places = self.get_places(cart)
        recepient_guid = request.GET.get('to', None)
        if not recepient_guid:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        providers = self.session.post(self.apiship_url + '/calculator', json={
            'from': {'cityGuid': self.apiship_settings.from_city_guid},
            'to': {'cityGuid': recepient_guid},
            'places': places,
            'assessedCost': cart.total,
            'pickupTypes': [2], 
            'deliveryTypes': [2],
            'includeFees': True,
        })
        return providers.json()['deliveryToPoint']
    
    def get_places(self, cart):
        return [
            {
                "weight": position.product.weight,
                "width": position.product.width,
                "height": position.product.height,
                "length": position.product.length,
            } 
        for position in cart.positions.all()]