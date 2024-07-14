# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupBuyViewSet, ParticipationViewSet

router = DefaultRouter()
router.register(r'group-buys', GroupBuyViewSet)
router.register(r'participations', ParticipationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]