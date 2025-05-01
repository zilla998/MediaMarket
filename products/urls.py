from django.urls import path

from .views import (products_list, product_detail, homepage,
                    category_sort, category_filter, product_cart,
                    about_us)

app_name = "products"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("about-us/", about_us, name="about_us"),
    path("catalog/", products_list, name="products_list"),
    path("product_detail/<pk>", product_detail, name="product_detail"),
    path("category/sort/", category_sort, name="category_sort"),
    path("category/filter/", category_filter, name="category_filter"),
    path("cart/", product_cart, name="product_cart"),
]