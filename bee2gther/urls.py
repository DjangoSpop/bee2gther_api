from django.contrib import admin
from django.urls import path, include
from bee2gther import settings
from rest_framework.routers import DefaultRouter
from orders.views import OrderViewSet
from users.views import UserViewSet
from products.views import ProductViewSet
from groupbuys.views import GroupBuyViewSet
from django.conf.urls.static import static
from django.conf import settings
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'groupbuys', GroupBuyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/groupbuys/', include('groupbuys.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)