from django.contrib import admin

from products.models import (
    Cart,
    Category,
    Favorite,
    Order,
    Product,
    ProductInCart,
    ProductInOrder,
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
    list_display = ("pk", "name", "price", "in_stock", "created_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "added_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "full_name",
        "address",
        "phone",
        "email",
        "status",
        "total_price",
        "created_at",
    )
    inlines = (ProductInOrderInlineModel,)
