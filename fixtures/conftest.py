import pytest

from products.models import Product, Category, Cart, Order
from users.models import CustomUser

from pytest_factoryboy import register
from fixtures.factories import CustomUserFactory, ProductFactory, CartFactory

register(CustomUserFactory)
register(ProductFactory)
register(CartFactory)


@pytest.fixture
def custom_user_factory(db):
    return CustomUserFactory


@pytest.fixture
def user(db):
    return CustomUser.objects.create(username="test_user", password="kjwandjk")


@pytest.fixture
def auth_client(db, client):
    """Авторизованный клиент"""
    user = CustomUser.objects.create_user(
        username="auth_user",
        password="testpass123",
        email="auth@example.com",
        phone="+79991234567",
    )
    client.force_login(user)
    return client


@pytest.fixture
def product(db):
    category = Category.objects.create(name="test_category", slug="test-category")
    return Product.objects.create(
        name="test_product",
        description="test_description",
        price=100,
        category=category,
        image="test_image",
    )


@pytest.fixture
def cart(db, user):
    return Cart.objects.create(user=user)


@pytest.fixture
def order(db, product, user):
    return Order.objects.create(
        user=user,
        full_name="test fio",
        address="test adress 123",
        phone="1234456789",
        email="test@mail.com",
        total_price=product.price,
    )
