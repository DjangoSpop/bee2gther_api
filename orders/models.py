from django.db import models
from django.conf import settings
from products.models import Product
from groupbuys.models import GroupBuy
from django.utils import timezone as tz

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=tz.now)
    updated_at = models.DateTimeField(default=tz.now)
    group_buy = models.ForeignKey('groupbuys.GroupBuy', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"