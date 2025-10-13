from rest_framework.routers import SimpleRouter
from . import views


feedback_router = SimpleRouter()
feedback_router.register('', views.FeedbackViewSet)