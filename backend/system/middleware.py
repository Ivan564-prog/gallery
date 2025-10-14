import re
import json
import logging
from django.http import QueryDict


logger = logging.getLogger('main')


class SwitchNameingStyleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not '/admin/' in request.build_absolute_uri():
            self.process_request(request)
            response = self.get_response(request)
            response = self.process_response(request, response)
        else:
            response = self.get_response(request)
        return response

    def camel_to_snake(self, name):
        return re.sub('([A-Z])', r'_\1', name).lower().lstrip('_')

    def snake_to_camel(self, name):
        parts = name.split('_')
        return parts[0] + ''.join(part.title() for part in parts[1:])

    def convert_keys(self, data):
        if isinstance(data, dict):
            return {self.snake_to_camel(key): self.convert_keys(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_keys(item) for item in data]
        else:
            return data

    def process_request(self, request):
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            new_data = {self.camel_to_snake(key): value for key, value in data.items()}
            request._body = json.dumps(new_data).encode('utf-8')
            
        if request.GET:
            query_dict = QueryDict(mutable=True)
            for key, value in request.GET.lists():
                query_dict.setlist(self.camel_to_snake(key), value)
            request.GET = query_dict

    def process_response(self, request, response):
        try:
            response_data = json.loads(response.content)
            new_response_data = self.convert_keys(response_data)
            response.content = json.dumps(new_response_data).encode('utf-8')
            response['Content-Length'] = len(response.content)
        except Exception as e:
            pass

        return response


class HostOverrideMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request.META['HTTP_X_FORWARDED_HOST'] = request.META["HOST"]
        except KeyError:
            request.META['HTTP_X_FORWARDED_HOST'] = request.META["HTTP_HOST"]

        # request.META['X-Forwarded-Proto'] = ''
        request.META['wsgi.url_scheme'] = 'https'
        return self.get_response(request)