from django.contrib import admin
from .models import Product



class Product (admin.ModelAdmin):
    list_display = ['name', 'price','seller', 'stock', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at', 'updated_at']
   
# Register your models here.
