from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet

app_name = 'subscriptions'

router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plan')
router.register('active', SubscriptionViewSet, basename='active')

urlpatterns = [
    path('', include(router.urls)),
]
