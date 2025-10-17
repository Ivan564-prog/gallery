from rest_framework.routers import SimpleRouter
from . import views


local_hierarchy_router = SimpleRouter()
local_hierarchy_router.register('diocese', views.DioceseViewSet)
local_hierarchy_router.register('metropolis', views.MetropolisViewSet)