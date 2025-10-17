from rest_framework.routers import SimpleRouter
from . import views


notification_router = SimpleRouter()
notification_router.register('', views.NoticeViewSet)