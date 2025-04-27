from django.shortcuts import render

from .models import Product


# Create your views here.

def homepage(request):
    return render(request, "homepage.html", {"title": "Главная страница"})

def products_list(request):
    products = Product.objects.all()

    sort_param = request.GET.get('sort')
    if sort_param == 'price_asc':
        products = products.order_by('price')
    elif sort_param == 'price_desc':
        products = products.order_by('-price')
    elif sort_param == 'date':
        products = products.order_by('-create_at')

    return render(request, "products/products_list.html", {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "products/product_detail.html", {"product": product})
