def count_cart(request):

    cart = request.session.get('cart', {})

    return {
        'cart_count': len(cart)
    }