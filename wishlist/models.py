from django.db import models
from users.models import CustomUser
from products.models import Product
from django.conf import settings
from django.contrib.auth import get_user_model

class Wishlist(models.Model):
    Users = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
