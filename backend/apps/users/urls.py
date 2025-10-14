from rest_framework.routers import SimpleRouter
from . import views


user_router = SimpleRouter()
user_router.register('', views.UserViewSet)