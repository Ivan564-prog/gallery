from rest_framework.routers import SimpleRouter
from . import views


apiship_router = SimpleRouter()
apiship_router.register('', views.ApishipViewSet)