from django.urls import path

from .views import products_list, product_detail, homepage

app_name = "products"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("catalog/", products_list, name="products_list"),
    path("product_detail/<pk>", product_detail, name="product_detail"),
]