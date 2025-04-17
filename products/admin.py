from django.contrib import admin

from products.models import Product, Category, CartItem, Favorite, Order, OrderItem


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'in_stock')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'address', 'phone', 'email', 'status', 'total_price', 'create_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')