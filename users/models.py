from django.conf import settings
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class ShopClient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profile/", verbose_name="Аватар", null=True)
    gender = models.CharField(max_length=1, verbose_name="Пол", null=False)
    balance = models.BigIntegerField(verbose_name="Баланс", null=False, default=0)
    slug = models.SlugField(verbose_name="Слаг")

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(ShopClient, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_page", args=[self.slug])

    def __str__(self) -> str:
        return f"client {self.user.username}"

