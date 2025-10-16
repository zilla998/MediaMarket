from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from products.models import ProductInCart, Product, Cart


@receiver(user_logged_in)
def migrate_session_cart_to_db(sender, request, user, **kwargs):
    """Перенос корзины из сессии в БД после входа"""
    session_cart = request.session.get("cart", {})

    if session_cart:
        cart, _ = Cart.objects.get_or_create(user=user)

        for product_id, quantity in session_cart.items():
            product = Product.objects.get(pk=product_id)
            item, created = ProductInCart.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": quantity}
            )
            if not created:
                item.quantity += quantity
                item.save()

        request.session.pop("cart", None)