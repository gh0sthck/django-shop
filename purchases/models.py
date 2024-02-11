from decimal import Decimal

from django.db import models
from django.urls import reverse

from pytils.translit import slugify

from users.models import ShopClient


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name="Имя")
    slug = models.SlugField(max_length=128, unique=True, verbose_name="Слаг")

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("home", args=[self.slug])

    def __str__(self) -> str:
        return self.name


class AvailableProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter().filter(available=True)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products",
                                 on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=128, verbose_name="Имя")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    image = models.ImageField(upload_to="products/", blank=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True, verbose_name="В наличии")
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", args=[self.slug])

    objects = models.Manager()
    available_products = AvailableProductManager()

    def get_rating(self) -> Decimal:
        return self.rating.get(product=self).product_rating

    def __str__(self) -> str:
        return self.name


class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments",
                                verbose_name="Товар")
    client = models.ForeignKey(ShopClient, on_delete=models.CASCADE, related_name="comments_client",
                               verbose_name="Клиент")
    text = models.TextField(verbose_name="Текст комментария")
    rating = models.IntegerField(default=0, verbose_name="Оценка товара")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def get_visual_rating(self) -> str:
        if self.rating > 0:
            return "💜" * self.rating
        else:
            return "🖤🖤🖤🖤🖤"

    @staticmethod
    def get_product_rating(product: Product):
        current = Comments.objects.filter(product=product)
        return round(sum(c.rating for c in current) / len(current), 2) if current else 0

    def __str__(self) -> str:
        return f"{self.product}: {self.text}"


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rating")
    product_rating = models.DecimalField(default=0.0, max_digits=2, decimal_places=1)

    class Meta:
        ordering = ["-product_rating"]
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self) -> str:
        return f"{self.product}: {self.product_rating}"