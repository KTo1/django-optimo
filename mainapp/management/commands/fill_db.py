import json
from django.core.management.base import BaseCommand

from authapp.models import User
from mainapp.models import Products, ProductCategories


def load_from_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        User.objects.create_superuser('kto', 'kto@kto.ru', '1')

        products_json = load_from_json('mainapp/fixtures/products.json')
        categories_json = load_from_json('mainapp/fixtures/categories.json')

        ProductCategories.objects.all().delete()
        for category_json in categories_json:
            category = category_json.get('fields')
            category['id'] = category_json.get('pk')

            ProductCategories(**category).save()

        Products.objects.all().delete()
        for product_json in products_json:
            product = product_json.get('fields')
            product['id'] = product_json.get('pk')
            product['category'] = ProductCategories.objects.get(id=product.get('category'))

            Products(**product).save()


