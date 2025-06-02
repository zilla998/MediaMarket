from products.models import Cart


def count_cart(request):

    cart = request.session.get('cart', {})
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user).products.all()
    return {
        'cart_count': len(cart)
    }