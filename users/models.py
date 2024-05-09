from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class ShopClient(AbstractUser):
    username = models.CharField(max_length=127, null=True, unique=True, verbose_name="Имя")
    email = models.EmailField(max_length=127, null=True, unique=True)
    avatar = models.ImageField(upload_to="profile/", verbose_name="Аватар", null=True, blank=True,
                               default="user_not_found.jpg")
    gender = models.CharField(max_length=1, verbose_name="Пол", null=False)
    balance = models.BigIntegerField(verbose_name="Баланс", null=False, default=0)
    slug = models.SlugField(verbose_name="Слаг")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(ShopClient, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_page", args=[self.slug])

    def __str__(self) -> str:
        return f"{self.username}: {self.email}"
    
    def __repr__(self) -> str:
        return f"<ShopClient: {self.username}-{self.email}>"

    class Meta:
        ordering = ["-username"]
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
