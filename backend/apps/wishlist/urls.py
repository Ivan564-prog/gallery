from rest_framework.routers import SimpleRouter
from . import views


wishlist_router = SimpleRouter()
wishlist_router.register('book', views.BookWishlist)