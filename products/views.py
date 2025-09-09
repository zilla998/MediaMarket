from enum import pickle_by_enum_name

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from django.db.models import Q

from MediaMarket.settings import LOGIN_URL
from .forms import OrderForm
from .models import Product, CartItem, Favorite, Cart, ProductInCart, ProductInOrder, Order


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
    query = request.GET.get('q', '')
    products = Product.objects.all()
    print(products.query)
    if query:
        query_lower = query.lower()
        products = [product for product in products if
                    query_lower in product.name.lower() or query_lower in product.description.lower()]
    return render(request, "products/products_list.html", {
        'products': products,
        'query': query,
    })


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_in_cart, created = ProductInCart.objects.get_or_create(
            cart=cart,
            product=product
        )
        if created:
            product_in_cart.amount = quantity
        else:
            product_in_cart.amount += int(quantity)
        product_in_cart.save()
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
        cart = Cart.objects.get(user=request.user)
        cart_items = ProductInCart.objects.filter(
            cart=cart
        )
        total_price = cart.total_price()

    else:
        cart_item = request.session.get('cart', {})
        cart_items = Product.objects.filter(pk__in=cart_item.keys())
        total_price = 0
        for product in cart_items:
            product.total_price = product.price * cart_item[str(product.pk)]
            total_price += product.total_price

    recomended_products = Product.objects.order_by('?')[:4]
    return render(request, "products/product_cart.html", {
        'title': "Моя корзина",
        'cart_items': cart_items,
        'total_price': total_price,
        'recommended_products': recomended_products,
    })


def add_product_to_cart(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user)

        product_in_cart, created = ProductInCart.objects.get_or_create(
            cart=cart,
            product=product,
        )

        if not created:
            product_in_cart.amount += 1
            product_in_cart.save()

    else:
        cart = request.session.get('cart', {})
        cart[pk] = cart.get(pk, 0) + 1
        request.session['cart'] = cart

    return redirect("products:product_cart")


def remove_product_from_cart(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=pk)
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)

    else:
        cart = request.session.get('cart', {})
        if pk in cart:
            del cart[pk]
            request.session['cart'] = cart

    return redirect("products:product_cart")


@login_required(login_url=LOGIN_URL)
def favorite_product(request):
    if request.user.is_authenticated:
        favorite_items = Favorite.objects.filter(user=request.user)

    else:
        favorite_item = request.session.get('favorite', {})
        favorite_items = Product.objects.filter(pk__in=favorite_item.keys())

    recomended_products = Product.objects.order_by('?')[:4]
    return render(request, "products/product_favorite.html", {
        'title': "Избранное",
        'favorite_items': favorite_items,
        'recommended_products': recomended_products,
    })


@login_required(login_url=LOGIN_URL)
def add_product_to_favorite(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=pk)
        favorite_item, created = Favorite.objects.get_or_create(
            user=request.user,
            product=product,
        )

        if not created:
            favorite_item.save()

    else:
        favorite = request.session.get('favorite', {})
        favorite[pk] = favorite.get(pk, 0) + 1
        request.session['favorite'] = favorite

    return redirect(request.META.get('HTTP_REFERER', 'products:products_list'))


def remove_product_to_favorite(request, pk):
    if request.user.is_authenticated:
        Favorite.objects.filter(user=request.user, product_id=pk).delete()

    else:
        favorite = request.session.get('favorite', {})
        if pk in favorite:
            del favorite[pk]
            request.session['favorite'] = favorite

    return redirect("products:favorite_product")


def product_checkout(request):
    if request.method == "POST":

        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.get(user=request.user)
            cart_items = ProductInCart.objects.filter(
                cart=cart
            )
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.total_price()
            order.save()
            for item in cart_items:
                ProductInOrder.objects.create(
                    order=order,
                    product=item.product,
                    amount=item.amount
                )
            cart.products.clear()
            return redirect("products:homepage")
    else:
        data = {
            "full_name": request.user.get_full_name(),
            "email": request.user.email,
            "address": request.user.address_default
        }
        form = OrderForm(initial=data)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = ProductInCart.objects.filter(
            cart=cart
        )
        total_price = 0
        for cart_item in cart_items:
            cart_item.total_price = cart_item.product.price * cart_item.amount
            total_price += cart_item.total_price
    else:
        cart_item = request.session.get('cart', {})
        products = Product.objects.filter(pk__in=cart_item.keys())
        cart_items = []
        total_price = 0
        for product in products:
            product.total_price = product.price * cart_item[str(product.pk)]
            total_price += product.total_price
            cart_items.append(product)

    shipping_price = {
        'direct': 500,
        'pickup': 1000,
    }

    shipping_type = request.GET.get('shipping')
    print(shipping_type)
    if shipping_type == 'direct':
        total_price += shipping_price['direct']
    if shipping_type == 'pickup':
        total_price += shipping_price['pickup']

    return render(request, "products/product_checkout.html", {
        'title': "Оформление заказа",
        'cart_items': cart_items,
        'total_price': total_price,
        'sub_total_price': total_price - shipping_price.get(shipping_type, 0),
        'shipping_price': shipping_price,
        "form": form
    })


def users_order(request):
    if request.method == "POST":
        status = request.POST.get("status").split("_")
        order = Order.objects.get(pk=int(status[0]))
        order.status = status[1]
        order.save()

    orders = Order.objects.all().order_by("-create_at")

    status = orders[0]._meta.get_field("status").choices
    cart = Cart.objects.get(user=request.user)
    total_price = cart.total_price()

    return render(request, 'products/users_order.html',
                  {'orders': orders, 'total_price': total_price, "status": status})


def order_repeat(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == "POST":
        new_order = Order.objects.create(user=request.user, status='new', total_price=0)
        for item in order.order_items.all():
            ProductInOrder.objects.create(
                order=new_order,
                product=item.product,
                amount=item.amount,
            )
        new_order.total_price = sum(
            i.total_product_price() for i in new_order.order_items.all()
        )
        new_order.save()

        return redirect('products:order_repeat', pk=request.user.pk)

    return redirect('users:user_profile_orders', pk=request.user.pk)
