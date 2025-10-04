# import pytest

# @pytest.mark.django_db
# class TestUserAddProductToCart:
#     @pytest.fixture(scope="class", autouse=True)
#     def setUp(
#         self,
#         request,
#         django_db_setup,
#         django_db_blocker,
#     ):
#         with django_db_blocker.unblock():
#             request.cls.user = CustomUserFactory(username="test_user")
#             request.cls.product = ProductFactory(name="test_prod", price=250)
#             request.cls.cart = CartFactory(user=request.cls.user)
#
#     def test_user_creation(self):
#         assert self.user.username == "test_user"
#
#     def test_product_creation(self):
#         assert self.product.name == "test_prod"
#         assert self.product.price == 250
#
#     def test_add_product_to_card(self):
#         self.cart.products.add(self.product)
#         assert self.product in self.cart.products.all()
from django.test import TestCase

from fixtures.factories import CartFactory, CustomUserFactory, ProductFactory


class TestUserAddProductToCart(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUserFactory(username="test_user")
        cls.product = ProductFactory(name="test_prod", price=250)
        cls.cart = CartFactory(user=cls.user)

    def test_correct_create_user(self):
        assert self.user.username == "test_user"

    def test_product_creation(self):
        assert self.product.name == "test_prod"
        assert self.product.price == 250

    def test_add_product_to_card(self):
        self.cart.products.add(self.product)
        assert self.product in self.cart.products.all()
