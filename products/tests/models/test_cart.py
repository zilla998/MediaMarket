from products.models import Product, Cart, ProductInCart

from fixtures.conftest import product, user, cart


def test_cart_creation(db, user, product, cart):
    assert Cart.objects.count() == 1
    get_cart = Cart.objects.first()
    assert get_cart.user == user

    # Добавляем продукт в корзину через ManyToMany
    cart.products.add(product)
    assert cart.products.count() == 1
    assert product in cart.products.all()


def test_cart_str_method(db, product, cart):
    cart.products.add(product)


def test_product_in_cart_str_method(db, product, cart):
    cart.products.add(product)
    get_prod = ProductInCart.objects.first()
    assert str(get_prod) == f"{product} - {get_prod.quantity}"


def test_cart_user_relationship(db, user, cart):
    assert cart.user == user


def test_cart_total_price_method(db, cart, product):
    product2 = Product.objects.create(
        name="test_product2",
        description="test_description2",
        price=product.price,
        category=product.category,
        image=product.image,
    )
    cart.products.add(product, product2)
    assert cart.products.count() == 2
    assert cart.total_price() == 200


def test_product_in_cart_creation(db, cart, product):
    cart.products.add(product)

    assert ProductInCart.objects.count() == 1

    get_prod = ProductInCart.objects.first()
    assert get_prod.product == product
    assert get_prod.cart == cart
    assert get_prod.quantity == 1
    assert get_prod.total_product_price() == product.price * get_prod.quantity
