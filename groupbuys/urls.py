from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupBuyViewSet

router = DefaultRouter()
router.register(r'group-buys', GroupBuyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]