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
