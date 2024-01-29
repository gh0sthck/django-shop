from django.conf import settings
from django.db import models


class ShopClient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", null=True)
    gender = models.CharField(max_length=1, verbose_name="Пол", null=False)
    balance = models.BigIntegerField(verbose_name="Баланс", null=False, default=0)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self) -> str:
        return f"client {self.user.username}"