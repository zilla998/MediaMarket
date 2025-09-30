import pytest
from django.db import IntegrityError

from products.models import Favorite

from fixtures.conftest import product, user


def test_favorite_creation(db, user, product):
    Favorite.objects.create(user=user, product=product)
    assert Favorite.objects.count() == 1
    get_fav = Favorite.objects.first()
    assert get_fav.user == user
    assert get_fav.product == product
    assert get_fav.favorite_count() == Favorite.objects.count()


def test_favorite_user_product_unique(db, user, product):
    Favorite.objects.create(user=user, product=product)
    with pytest.raises(IntegrityError):
        Favorite.objects.create(user=user, product=product)


def test_favorite_str_method(db, user, product):
    favorite = Favorite.objects.create(user=user, product=product)
    assert str(favorite) == product.name
