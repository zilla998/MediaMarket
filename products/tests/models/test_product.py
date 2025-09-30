import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from products.models import Product, Category

from fixtures.conftest import product, user, cart


def test_product_creation(db, product):
    assert Product.objects.count() == 1

    get_product = Product.objects.first()

    assert get_product.name == "test_product"
    assert get_product.description == "test_description"
    assert get_product.price == 100
    assert get_product.category == product.category
    assert get_product.image == "test_image"


def test_product_str_method(db, product):
    assert str(product) == "test_product"


def test_cart_str_method(db, product):
    assert str(product.category) == "test_category"


def test_product_in_stock_default(db, product):
    # Assert default == True
    assert product.in_stock


def test_category_creation(db):
    Category.objects.create(name="test_category", slug="test-slug")

    assert Category.objects.count() == 1

    get_cat = Category.objects.first()
    assert get_cat.name == "test_category"
    assert get_cat.slug == "test-slug"


def test_category_slug_unique(db):
    """
    Аналогично для уникальности slug:

    def test_category_slug_unique(db):
        Category.objects.create(name="test_category1", slug="test-slug")  # Сначала создаем
        with pytest.raises(IntegrityError):  # Ловим IntegrityError
            Category.objects.create(name="test_category2", slug="test-slug")  # Пытаемся создать дубль

    Здесь используется IntegrityError, потому что нарушение уникальности происходит на уровне базы данных при
    попытке сохранения.
    """
    Category.objects.create(name="test_category1", slug="test-slug")
    with pytest.raises(IntegrityError):
        Category.objects.create(name="test_category2", slug="test-slug")


def test_category_name_max_length(db):
    """
    Почему Category.objects.create() не работал:

    # НЕ РАБОТАЕТ:
    Category.objects.create(name="a" * 256, slug="test-slug")

    Django автоматически обрезает строки до максимальной длины поля при сохранении в базу данных. То есть
    строка из 256 символов просто обрежется до 255 символов и сохранится без ошибки.

    Правильный подход:

    # РАБОТАЕТ:
    category = Category(name="a" * 256, slug="test-slug")
    category.full_clean()  # Вызывает ValidationError до сохранения

    full_clean() проверяет валидность до сохранения в базу данных и вызывает ValidationError, если поле name
    превышает 255 символов.
    """
    category = Category(name="a" * 256, slug="test-slug")
    with pytest.raises(ValidationError):
        category.full_clean()
