import pytest

from products.models import Product, Category
from users.models import CustomUser


class TestUserAddProductToCard:
    @pytest.fixture(scope="class", autouse=True)
    def setUp(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            CustomUser.objects.filter(username="test_user").delete()
            TestUserAddProductToCard.user = CustomUser.objects.create(
                username="test_user", password="ahwbdiu"
            )
            # category = Category.objects.create(name="test_cat", slug="test-cat")
            # TestUserAddProductToCard.product = Product.objects.create(
            #     name="test_product",
            #     description="test_desc",
            #     price="100",
            #     image="test_image",
            #     category=category,
            # )

    def test_user_creation(self):
        assert self.user.username == "test_user"
        self.user.username = "user_test"
        assert self.user.username == "user_test"

    def test_add_product_to_card(self):
        assert self.user.username != "test_user"
