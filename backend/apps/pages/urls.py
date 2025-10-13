from rest_framework import routers
from . import views


pages_router = routers.SimpleRouter()
pages_router.register('pages', views.PageViewSet)