from django.conf import settings
from django.db import models


# Описание товаров в каталоге
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to="products_images/", verbose_name="Изображение")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


# Категории товаров
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"





class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(
        Product,
        through="ProductInCart",
        related_name="carts",
        verbose_name="Продукты"
    )

    class Meta:
        verbose_name = "Корзины"
        verbose_name_plural = "Корзины"

    def total_price(self):
        return sum(item.price for item in self.products.all())

    # def __str__(self):
    #     return self.user


class ProductInCart(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name = "Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт"
    )
    amount = models.IntegerField(default=1, verbose_name="Кол-во")

    class Meta:
        verbose_name = "Продукты в корзине"
        verbose_name_plural = "Продукты в корзинах"

    def total_product_price(self):
        return self.product.price * self.amount

    def __str__(self):
        return f"{self.product} - {self.amount}"

# Позиция товара в корзине пользователя
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(verbose_name="Кол-во")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"


# Избранные товары пользователя
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"


# Основная сущность заказа
class Order(models.Model):
    choices = (
        ("new", "Новый"),
        ("paid", "Оплачен"),
        ("sent", "Отправлен"),
        ("done", "Выполнен"),
        ("cancelled", "Отменен"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Заказчик")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    phone = models.CharField(max_length=255, verbose_name="Контактный номер")
    email = models.EmailField(verbose_name="Email")
    status = models.CharField(choices=choices, default="new", verbose_name="Статус заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая стоимость")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Время оформления")

    def __str__(self):
        return f"Заказ №{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


# Привязка товаров к заказу
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент покупки")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"