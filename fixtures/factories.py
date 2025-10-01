import factory
from factory import fuzzy
from products.models import Category, Product, Cart
from users.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Сохраняем пользователя после вызова set_password"""
        if create:
            instance.save()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker("sentence")
    price = fuzzy.FuzzyDecimal(10, 500)
    image = "test_image"
    category = factory.SubFactory(CategoryFactory)


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(CustomUserFactory)
