from products.models import ProductInCart

from django.db.models import Sum


def count_cart(request):
    cart = request.session.get("cart", {})
    if request.user.is_authenticated:
        cart = (
            ProductInCart.objects.filter(cart__user=request.user).aggregate(
                total=Sum("quantity")
            )["total"]
            or 0
        )
    else:
        cart = sum(cart.values())
    return {"cart_count": cart}
