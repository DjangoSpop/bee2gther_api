from django.db import models
from django.utils import timezone
from django.conf import settings


def one_week_from_now():
    return timezone.now() + timezone.timedelta(weeks=1)


class GroupBuy(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='groupbuys')
    created_at = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=one_week_from_now)
    is_active = models.BooleanField(default=True)
    min_quantity = models.PositiveIntegerField(default=0)
    max_quantity = models.PositiveIntegerField(default=0)
    target_quantity = models.PositiveIntegerField(default=0)
    current_quantity = models.PositiveIntegerField(default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Group Buy for {self.product.name}"


class GroupBuyParticipation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_buy = models.ForeignKey(GroupBuy, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} in {self.group_buy}"
class Meta:
    unique_together = ('group_buy', 'user')
