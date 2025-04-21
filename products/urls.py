from django.urls import path

from .views import products_list, product_detail

app_name = "products"

urlpatterns = [
    path("", products_list, name="products_list"),
    path("product_detail/<pk>", product_detail, name="product_detail")
]