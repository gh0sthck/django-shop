from decimal import Decimal
from typing import List

from django.db import models
from django.urls import reverse

from pytils.translit import slugify

from users.models import ShopClient


class PruchasessPermissions:
    MODEL_NAME = "name"

    @classmethod
    def get_permissions(cls) -> List[str]:
        return [
            f"purchases.change_{cls.MODEL_NAME}",
            f"purchases.add_{cls.MODEL_NAME}",
            f"purchases.delete_{cls.MODEL_NAME}",
        ]


class AvailableProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter().filter(available=True)


class Category(models.Model, PruchasessPermissions):
    MODEL_NAME = "category"
    name = models.CharField(max_length=128, verbose_name="Имя")
    slug = models.SlugField(max_length=128, unique=True, verbose_name="Слаг")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("home", args=[self.slug])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Category: {self.name}>"

    class Meta:
        ordering = ["-name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model, PruchasessPermissions):
    MODEL_NAME = "product"
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    name = models.CharField(max_length=128, verbose_name="Имя")
    slug = models.SlugField(max_length=128, verbose_name="Слаг", unique=True)
    image = models.ImageField(upload_to="products/", blank=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True, verbose_name="В наличии")
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    available_products = AvailableProductManager()

    def get_rating(self) -> Decimal:
        return self.rating.get(product=self).product_rating

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", args=[self.slug])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Product: {self.name}>"

    class Meta:
        ordering = ["-name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Comments(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments", verbose_name="Товар"
    )
    client = models.ForeignKey(
        ShopClient,
        on_delete=models.CASCADE,
        related_name="comments_client",
        verbose_name="Клиент",
    )
    text = models.TextField(verbose_name="Текст комментария")
    rating = models.IntegerField(default=0, verbose_name="Оценка товара")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_product_rating(product: Product):
        """Return product decimal rating by specific Product."""
        product_comments = Comments.objects.filter(product=product)
        return (
            round(sum(comment.rating for comment in product_comments) / len(product_comments), 2)
            if product_comments
            else 0
        )

    def get_visual_rating(self) -> str:
        """Return Comment raiting in emoji hearts."""
        if self.rating > 0:
            return "💜" * self.rating
        return "🖤🖤🖤🖤🖤"

    def __str__(self) -> str:
        return f"{self.product}: {self.text}"

    def __repr__(self) -> str:
        return f"<Comment: {self.product}-{self.text}>"

    class Meta:
        ordering = ["-created"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Rating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="rating"
    )
    product_rating = models.DecimalField(default=0.0, max_digits=2, decimal_places=1)

    def __str__(self) -> str:
        return f"{self.product}: {self.product_rating}"
    
    def __repr__(self) -> str:
        return f"<Rating: {self.product}-{self.product_rating}>"

    class Meta:
        ordering = ["-product_rating"]
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
