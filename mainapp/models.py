from django.db import models

# Create your models here.

class ProductCategories(models.Model):
    ''' model for categories  '''

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this category should be treated as active. '
    )

    def __str__(self):
        return self.name


class Products(models.Model):
    ''' model for products '''

    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='product_images', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    basic_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this product should be treated as active. '
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.price:
            self.price = self.basic_price
        super(Products, self).save()

    def __str__(self):
        # Категория лишний запрос, если убрать то будет работать быстрее
        # return f'{self.category} | {self.name}'
        return self.name
