from django.contrib.auth.models import Group
from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Costumer)
class CotumerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zip', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_img']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(PlacedOrder)
class PlacedOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'costumer', 'product', 'quantity', 'order_date', 'status']

admin.site.unregister(Group)