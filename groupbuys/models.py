from django.db import models
from users.models import CustomUser
from products.models import Product
from django.utils import timezone as tz


def one_week_from_now():
    return tz.now() + tz.timedelta(weeks=1)


class GroupBuy(models.Model):
    group = models.ManyToManyField(CustomUser, related_name='groupbuys_group')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ManyToManyField(CustomUser,  related_name='groupbuys_users')
    created_at = models.DateTimeField(default=tz.now)
    is_active = models.BooleanField(default=True)
    end_date = models.DateTimeField(default=one_week_from_now)
    start_time = models.DateTimeField(default=tz.now)
    min_quantity = models.PositiveIntegerField(default=0)
    max_quantity = models.PositiveIntegerField(default=0)
    target_quantity = models.PositiveIntegerField(default=0)
    current_quantity = models.PositiveBigIntegerField(default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='active')
    
    def __str__(self):
        return f"Group Buy for {self.product.name}"
    
class Participation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group_buy = models.ForeignKey(GroupBuy, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.CustomUser.username} in {self.group_buy.product.name}"