from rest_framework.routers import SimpleRouter
from . import views


library_router = SimpleRouter()
library_router.register('book', views.BookModelViewSet)
library_router.register('book_type', views.BookTypeModelViewSet)