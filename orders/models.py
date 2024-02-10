from decimal import Decimal

from django.db import models

from purchases.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=120, verbose_name="Имя")
    last_name = models.CharField(max_length=120, verbose_name="Фамилия")
    email = models.EmailField()
    phone = models.PositiveIntegerField(default=7, verbose_name="Номер телефона")
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.CharField(max_length=250, verbose_name="Адрес доставки")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")
    paid = models.BooleanField(default=False, verbose_name="Статус оплаты")

    class Meta:
        ordering = ["paid", "-created", ]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_total_cost(self) -> Decimal:
        return sum(item.get_cost() for item in self.items())

    def __str__(self) -> str:
        return f"Order: {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", ]
        verbose_name = "Вещь заказа"
        verbose_name_plural = "Вещи заказов"

    def get_cost(self) -> Decimal:
        return self.count * self.price

    def __str__(self) -> str:
        return f"{self.order} : {self.product}"