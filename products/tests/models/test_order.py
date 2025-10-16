from products.models import Order, ProductInOrder

from fixtures.conftest import product, user, order


def test_order_creation(db, order, product):
    order.products.add(product)
    assert Order.objects.count() == 1
    assert order.products.count() == 1
    assert product in order.products.all()
    assert order.status == "new"
    assert order.total_price == product.price


def test_product_in_order_creation(db, order, product):
    ProductInOrder.objects.create(order=order, product=product)
    assert ProductInOrder.objects.count() == 1

    get_prod_in_order = ProductInOrder.objects.first()
    assert get_prod_in_order.order == order
    assert get_prod_in_order.product == product
    assert get_prod_in_order.quantity == 1
    assert (
        get_prod_in_order.total_product_price()
        == product.price * get_prod_in_order.quantity
    )


def test_order_str_method(db, order, product):
    order.products.add(product)
    assert str(order) == f"Заказ №{product.id} от {product.created_at.strftime('%d.%m.%Y')}"


def test_product_in_order(db, order, product):
    ProductInOrder.objects.create(order=order, product=product)
    get_prod = ProductInOrder.objects.first()
    assert str(get_prod) == f"{product} - {get_prod.quantity}"
