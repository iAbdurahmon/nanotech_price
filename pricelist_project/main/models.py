from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)  # Название категории

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)  # Название товара
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Категория
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    description = models.TextField(blank=True, null=True)  # Описание
    created_at = models.DateTimeField(auto_now_add=True)  # Дата добавления

    def __str__(self):
        return self.name
