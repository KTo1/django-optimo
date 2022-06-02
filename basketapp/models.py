from select import select

from django.db import models


# Create your models here.
from authapp.models import User
from mainapp.models import Products


class BasketQuerySet(models.QuerySet):
    ''' manager for basket query set '''

    pass
    # def delete(self, *args, **kwargs):
    #     for item in self:
    #         item.product.quantity += item.quantity
    #         item.product.save()
    #     super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    ''' model fo basket '''

    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='basket')
    quantity = models.PositiveIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для - {self.user.username} | Продукт - {self.product.name}'

    @property
    def baskets(self):
        return Basket.objects.filter(user=self.user).select_related('product')

    def sum(self):
        return self.quantity * self.product.price
    #
    # def total_sum(self):
    #     return sum(basket.sum() for basket in self.baskets)
    #
    # def total_quantity(self):
    #     return sum(basket.quantity for basket in self.baskets)

    # def save(self, *args, **kwargs):
    #     pass
    #     # item = Basket.get_item(self.pk) if self.pk else 0
    #     # self.product.quantity -= self.quantity - item
    #     # self.product.save()
    #     # super(Basket, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(Basket, self).delete(*args, **kwargs)

    # @staticmethod
    # def get_item(pk):
    #     return Basket.objects.get(pk=pk).quantity