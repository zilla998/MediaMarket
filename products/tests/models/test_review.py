from products.models import Review

from fixtures.conftest import product, user


def test_review_creation(db, user, product):
    Review.objects.create(user=user, product=product, rating=5, text="test text")

    assert Review.objects.count() == 1

    get_review = Review.objects.first()
    assert get_review.user == user
    assert get_review.product == product
    assert get_review.rating == 5
    assert get_review.text == "test text"
