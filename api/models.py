from django.contrib.auth.models import AbstractUser
from django.db import models


class ApiUser(AbstractUser):
    USER = 'Пользователь'
    SUPPLIER = 'Поставщик'
    CATEGORY_CHOICES = [
        (USER, 'пользователь'),
        (SUPPLIER, 'поставщик'),
    ]
    cat = models.CharField(max_length=16, choices=CATEGORY_CHOICES)


class Storage(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Product(models.Model):
    storage = models.ForeignKey(Storage, related_name='items', on_delete=models.CASCADE)
    user = models.ForeignKey(ApiUser, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.username}; {self.storage.name}"
