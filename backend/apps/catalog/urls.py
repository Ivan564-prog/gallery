from rest_framework.routers import SimpleRouter
from . import views


catalog_router = SimpleRouter()
catalog_router.register('category', views.CategoryViewSet)
catalog_router.register('product', views.ProductViewSet)