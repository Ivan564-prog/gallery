from rest_framework.routers import SimpleRouter
from . import views


carts_router = SimpleRouter()
carts_router.register('', views.CartViewSet)