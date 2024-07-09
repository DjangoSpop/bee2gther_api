from django.contrib import admin
from .models import Order,OrderedItem  # Assuming OrderItem is another model related to Order

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderedItem  # Assuming OrderItem is the correct related model
    raw_id_fields = ['order']  # Ensure 'order' is a ForeignKey in OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_at', 'updated_at']  # Corrected 'orders' to valid fields