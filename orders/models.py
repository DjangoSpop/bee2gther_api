from django.db import models
from django.conf import settings
from products.models import Product
from groupbuys.models import GroupBuy
from users.models import CustomUser
from django.utils import timezone as tz

class Order(models.Model):
    created_at = models.DateTimeField(default=tz.now)
    updated_at = models.DateTimeField(default=tz.now)
    group_buy = models.ForeignKey(Product, on_delete=models.CASCADE)
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
class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"