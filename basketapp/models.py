from django.db import models


# Create your models here.
from authapp.models import User
from mainapp.models import Products


class Basket(models.Model):
    ''' model fo basket '''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для - {self.user.username} | Продукт - {self.product.name}'

    @property
    def baskets(self):
        return Basket.objects.filter(user=self.user)

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        return sum(basket.sum() for basket in self.baskets)

    def total_quantity(self):
        return sum(basket.quantity for basket in self.baskets)
