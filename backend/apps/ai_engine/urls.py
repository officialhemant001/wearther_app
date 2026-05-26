from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, ChatMessageViewSet

app_name = 'ai_engine'

router = DefaultRouter()
router.register('sessions', ChatSessionViewSet, basename='session')
router.register('messages', ChatMessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
