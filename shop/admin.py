from django.contrib import admin
from .models import Category, Product, ShopAddress, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'characteristics', 'description','available', 'created']
    list_filter = ['available', 'created',]
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'hours']
admin.site.register(ShopAddress, AddressAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer', 'address', 'created', 'paid']
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']
admin.site.register(OrderItem, OrderItemAdmin)