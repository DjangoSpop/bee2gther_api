from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from cart.views import CartView, AddToCartView
from categories.views import CategoriesViewSet
from groupbuys.views import GroupBuyViewSet, JoinGroupBuyView, ParticipationViewSet, GroupBuyDetailView,GroupListView
from orders.views import OrderViewSet
from products.views import ProductViewSet, ProductListView, ProductDetailView
from users.views import UserViewSet, RegisterView
from .views import home, WelcomeView

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'groupbuys', GroupBuyViewSet, basename='groupbuy')
router.register(r'participations',ParticipationViewSet , basename='participation')
router.register(r'categories',CategoriesViewSet, basename='categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/groupbuys/', include('groupbuys.urls')),
    path('api/categories/', include('categories.urls')),
    path('', ProductListView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('groupbuys/', GroupListView.as_view(), name='group-buy'),
    path('groupbuys/<int:pk>/', GroupBuyDetailView.as_view(), name='groupbuy-detail'),
    path('groupbuys/<int:pk>/join/', JoinGroupBuyView.as_view(), name='join-group-buy'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    # Remove this line as it's redundant and has a typo
    # path('api/groupbuys/particpants', include('particpation.urls'))
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)