from django.shortcuts import render

from .models import Product


def homepage(request):
    return render(request, "homepage.html", {
        "title": "Главная страница"
    })

def about_us(request):
    return render(request, "about_us.html", {
        "title": "О нас"
    })


def products_list(request):
    products = Product.objects.all()

    return render(request, "products/products_list.html", {
        'products': products,
    })


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "products/product_detail.html", {
        "product": product
    })


def category_sort(request):
    products = Product.objects.all()

    sort_param = request.GET.get('sort')
    if sort_param == 'price_asc':
        products = products.order_by('price')
    elif sort_param == 'price_desc':
        products = products.order_by('-price')
    elif sort_param == 'date':
        products = products.order_by('-create_at')

    return render(request, "products/products_list.html", {
        'products': products
    })


def category_filter(request):
    products = Product.objects.all()
    filter_param = request.GET.get('filter')
    current_category = None
    
    if filter_param == 'electronic':
        products = products.filter(category__slug='electronic')
        current_category = 'electronic'
    elif filter_param == 'household_goods':
        products = products.filter(category__slug='household_goods')
        current_category = 'household_goods'
    elif filter_param == 'animal':
        products = products.filter(category__slug='animal')
        current_category = 'animal'
    elif filter_param == 'podarok':
        products = products.filter(category__slug='podarok')
        current_category = 'podarok'
        
    return render(request, "products/products_list.html", {
        'products': products,
        'current_category': current_category,
    })


def product_cart(request):

    return render(request, "products/product_cart.html", {'title': "Моя корзина"})