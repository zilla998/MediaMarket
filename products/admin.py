from django.contrib import admin

from products.models import (
    Product, Category, CartItem,
    Favorite, Order, OrderItem,
    Cart, ProductInCart, ProductInOrder
)


class ProductInOrderInlineModel(admin.TabularInline):
    model = ProductInOrder
    extra = 2


class ProductInCartInlineModel(admin.TabularInline):
    model = ProductInCart
    extra = 2



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("pk", "user")
    inlines = (ProductInCartInlineModel,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'in_stock', 'create_at')


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
    list_display = ("pk", 'user', 'full_name', 'address', 'phone', 'email', 'status', 'total_price', 'create_at')
    inlines = (ProductInOrderInlineModel,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')