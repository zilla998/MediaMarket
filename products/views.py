from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models import F

from .models import Product, CartItem


@receiver(user_logged_in)
def transfer_cart_items(sender, user, request, **kwargs):
    session_cart = request.session.get('cart', {})
    
    if session_cart:
        for product_id, quantity in session_cart.items():
            try:
                product = Product.objects.get(pk=product_id)
                cart_item, created = CartItem.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                    
            except Product.DoesNotExist:
                continue

        request.session['cart'] = {}
        request.session.modified = True

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
    if filter_param in ["electronic", "household_goods", "animal", "podarok"]:
        products = products.filter(category__slug=filter_param)
        current_category = filter_param

    # if filter_param == 'electronic':
    #     products = products.filter(category__slug='electronic')
    #     current_category = 'electronic'
    # elif filter_param == 'household_goods':
    #     products = products.filter(category__slug='household_goods')
    #     current_category = 'household_goods'
    # elif filter_param == 'animal':
    #     products = products.filter(category__slug='animal')
    #     current_category = 'animal'
    # elif filter_param == 'podarok':
    #     products = products.filter(category__slug='podarok')
    #     current_category = 'podarok'
        
    return render(request, "products/products_list.html", {
        'products': products,
        'current_category': current_category,
    })


def product_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_item = request.session.get('cart', {})
        cart_items = Product.objects.filter(pk__in=cart_item.keys())
    # recomended_products = Product.objects.order_by('?')[:4]
    return render(request, "products/product_cart.html", {
        # 'title': "Моя корзина",
        'cart_items': cart_items,
        # 'recommended_products': recomended_products,
    })


def add_product_to_cart(request, pk):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=pk).update(
            quantity=F('quantity') + 1
        )

    else:
        cart = request.session.get('cart', {})
        cart[pk] = cart.get(pk, 0) + 1
        request.session['cart'] = cart
    return redirect("products:product_cart")


def remove_product_from_cart(request, pk):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=pk).delete()

    else:
        cart = request.session.get('cart', {})
        if pk in cart:
            del cart[pk]
            request.session['cart'] = cart

    return redirect("products:product_cart")
