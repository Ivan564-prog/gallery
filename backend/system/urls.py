from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

from apps.users.urls import user_router
from apps.pages.urls import pages_router
from apps.carts.urls import carts_router
from apps.orders.urls import orders_router
from apps.catalog.urls import catalog_router
from apps.wishlist.urls import wishlist_router
from apps.config.urls import config_router
from apps.feedback.urls import feedback_router
from apps.apiship.urls import apiship_router


urlpatterns = [
    path('streamfield/', include('streamfield.urls')),
    path('tinymce/', include('tinymce.urls')),

    path('admin/style/<str:filename>', views.admin_style),
    path('admin/script/<str:filename>', views.admin_script),
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots),
    
    path('api/v1/', include(pages_router.urls)),
    path('api/v1/user/', include(user_router.urls)),
    path('api/v1/cart/', include(carts_router.urls)),
    path('api/v1/order/', include(orders_router.urls)),
    path('api/v1/feedback/', include(feedback_router.urls)),
    path('api/v1/wishlist/', include(wishlist_router.urls)),
    path('api/v1/config/', include(config_router.urls)),
    path('api/v1/catalog/', include(catalog_router.urls)),
    path('api/v1/apiship/', include(apiship_router.urls)),
    path('api/v1/csrf_generate/', views.csrf_gen),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)