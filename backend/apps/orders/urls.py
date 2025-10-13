from rest_framework.routers import SimpleRouter
from . import views


orders_router = SimpleRouter()
orders_router.register('', views.OrderViewSet)