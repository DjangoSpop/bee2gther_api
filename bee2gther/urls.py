from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from orders.views import OrderViewSet
from users.views import UserViewSet
from products.views import ProductViewSet
from groupbuys.views import GroupBuyViewSet, ParticipationViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'groupbuys', GroupBuyViewSet, basename='groupbuy')
router.register(r'participations', ParticipationViewSet, basename='participation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/groupbuys/', include('groupbuys.urls')),
    # Remove this line as it's redundant and has a typo
    # path('api/groupbuys/particpants', include('particpation.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)