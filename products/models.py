from django.conf import settings
from django.db import models
from django.db.models import F, Sum, DecimalField
from decimal import Decimal


# Описание товаров в каталоге
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to="products_images/", verbose_name="Изображение")
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="Категория"
    )
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


# Категории товаров
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    products = models.ManyToManyField(
        Product, through="ProductInCart", related_name="carts", verbose_name="Продукты"
    )

    class Meta:
        verbose_name = "Корзины"
        verbose_name_plural = "Корзины"

    def total_price(self):
        subtotal = self.productincart_set.aggregate(
            total=Sum(
                F("quantity") * F("product__price"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )["total"]
        return subtotal or Decimal("0.00")


class ProductInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.IntegerField(default=1, verbose_name="Кол-во товара")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Продукты в корзине"
        verbose_name_plural = "Продукты в корзинах"

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    def total_product_price(self):
        return self.product.price * self.quantity


# Избранные товары пользователя
class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
        unique_together = ("user", "product")

    def __str__(self):
        return self.product.name

    def favorite_count(self):
        return Favorite.objects.filter(user=self.user).count()


# Основная сущность заказа
class Order(models.Model):
    choices = (
        ("new", "Новый"),
        ("paid", "Оплачен"),
        ("sent", "Отправлен"),
        ("done", "Выполнен"),
        ("cancelled", "Отменен"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Заказчик"
    )
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    products = models.ManyToManyField(
        Product,
        through="ProductInOrder",
        related_name="orders",
        verbose_name="Продукты",
    )
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    phone = models.CharField(max_length=255, verbose_name="Контактный номер")
    email = models.EmailField(verbose_name="Email")
    status = models.CharField(
        max_length=20, choices=choices, default="new", verbose_name="Статус заказа"
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Итоговая стоимость"
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Время оформления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id}"


class ProductInOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Корзина",
        related_name="order_items",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.IntegerField(default=1, verbose_name="Кол-во")

    class Meta:
        verbose_name = "Продукты в заказе"
        verbose_name_plural = "Продукты в заказах"

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    def total_product_price(self):
        return self.product.price * self.quantity


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    rating = models.IntegerField(verbose_name="Рейтинг")
    text = models.TextField(verbose_name="Текст отзыва")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
