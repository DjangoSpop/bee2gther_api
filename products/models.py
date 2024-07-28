from django.db import models
from django.core.validators import MinValueValidator
from categories.models import Category
from groupbuys.models import GroupBuy
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        default=Decimal('0.01')  # Default price of 0.01
    )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    group_buy = models.OneToOneField(GroupBuy, related_name='associated_product', on_delete=models.SET_NULL, null=True,
                                     blank=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    main_image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"