import random
import string
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)  # Название категории
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    custom_id = models.CharField(max_length=5, unique=True, blank=True)
    name = models.CharField(max_length=100)  # Название товара
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Категория
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    description = models.TextField(blank=True, null=True)  # Описание
    created_at = models.DateTimeField(auto_now_add=True)  # Дата добавления

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = ''.join(random.choices('0123456789', k=5))  # Генерация 5-значного числового ID
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return f'/category/{self.category.id}'


    def __str__(self):
        return self.name
