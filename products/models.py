from django.db import models
from users.models import CustomUser
from django.utils import timezone as tz

from django.conf import settings




class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    min_quantity = models.PositiveIntegerField()
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    images = models.ImageField(upload_to='products_images/',blank=True, null=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(default=tz.now)

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return super().__str__()
