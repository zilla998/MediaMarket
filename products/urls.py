from django.urls import path

from .views import (products_list, product_detail, homepage,
                    category_sort, category_filter, product_cart,
                    about_us, add_product_to_cart, remove_product_from_cart,
                    favorite_product, add_product_to_favorite, remove_product_to_favorite,
                    product_checkout, users_order, order_repeat)

app_name = "products"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("about-us/", about_us, name="about_us"),
    path("catalog/", products_list, name="products_list"),
    path("product_detail/<pk>", product_detail, name="product_detail"),
    path("category/sort/", category_sort, name="category_sort"),
    path("category/filter/", category_filter, name="category_filter"),
    path("cart/", product_cart, name="product_cart"),
    path("cart/add/<pk>", add_product_to_cart, name="add_product_to_cart"),
    path("cart/remove/<pk>", remove_product_from_cart,
         name="remove_product_from_cart"),
    path("favorite/", favorite_product, name="favorite_product"),
    path("favorite/add/<pk>", add_product_to_favorite,
         name="add_product_to_favorite"),
    path("favorite/remove/<pk>", remove_product_to_favorite,
         name="remove_product_to_favorite"),
    path("checkout/", product_checkout, name="product_checkout"),
    # path('checkout/select-shipping/', select_shipping, name='select_shipping'),
    path("users_order/", users_order, name="users_order"),
    path('order-repeat/<int:pk>/', order_repeat, name='order_repeat'),
]
