from . import views
from rest_framework.routers import SimpleRouter


config_router = SimpleRouter()
config_router.register('root', views.RootSettingsViewSet)
config_router.register('index', views.IndexSettingsViewSet)
config_router.register('domain', views.DomainViewSet)