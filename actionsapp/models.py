from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from mainapp.models import ProductCategories, Products


class Action(models.Model):
    ''' model for actions '''

    name = models.CharField(max_length=128)
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, related_name='basket')
    percent = models.DecimalField(max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return f'Акция {self.name} для - {self.category}'

    @classmethod
    def update_products(self, category, percent):
        Products.objects.filter(category=category).update(price=F('basic_price') * ((100 - percent) / 100))
