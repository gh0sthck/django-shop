from django.db import models
from django.urls import reverse

from pytils.translit import slugify


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
                                 on_delete=models.CASCADE)
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

    def __str__(self) -> str:
        return self.name

