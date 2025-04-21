from django.shortcuts import render

from .models import Product


# Create your views here.

def products_list(request):
    products = Product.objects.all()

    return render(request, "products/products_list.html", {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "products/prodcut_detail.html", {"product": product})
