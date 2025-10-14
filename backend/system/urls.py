from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

from apps.users.urls import user_router
from apps.config.urls import config_router
from apps.local_hierarchy.urls import local_hierarchy_router
from apps.library.urls import library_router
from apps.notification.urls import notification_router
from apps.wishlist.urls import wishlist_router


urlpatterns = [
    # URL что бы исключить warning
    path('i18n/', include('django.conf.urls.i18n')),
    # Технические URLs
    path('streamfield/', include('streamfield.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/style/<str:filename>', views.admin_style),
    path('admin/script/<str:filename>', views.admin_script),
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots),
    
    # URLs приложений
    path('api/v1/user/', include(user_router.urls)),
    path('api/v1/config/', include(config_router.urls)),
    path('api/v1/local_hierarchy/', include(local_hierarchy_router.urls)),
    path('api/v1/library/', include(library_router.urls)),
    path('api/v1/notification/', include(notification_router.urls)),
    path('api/v1/wishlist/', include(wishlist_router.urls)),

    path('api/v1/csrf_generate/', views.csrf_gen),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)