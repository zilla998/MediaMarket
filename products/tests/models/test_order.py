from products.models import Order, ProductInOrder, OrderItem

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


def test_order_item_creation(db, product, order):
    OrderItem.objects.create(
        order=order, product=product, quantity=1, price=product.price
    )
    assert OrderItem.objects.count() == 1

    get_order_item = OrderItem.objects.first()
    assert get_order_item.order == order
    assert get_order_item.product == product
    assert get_order_item.quantity == 1
    assert get_order_item.price == product.price


def test_order_str_method(db, order, product):
    order.products.add(product)
    assert str(order) == f"Заказ №{order.id}"


def test_product_in_order(db, order, product):
    ProductInOrder.objects.create(order=order, product=product)
    get_prod = ProductInOrder.objects.first()
    assert str(get_prod) == f"{product} - {get_prod.quantity}"


def test_order_item_str_method(db, order, product):
    order_item = OrderItem.objects.create(
        order=order, product=product, quantity=1, price=product.price
    )
    assert str(order_item) == f"{product.name} - {order_item.quantity}"
