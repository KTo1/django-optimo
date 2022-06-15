import json
from django.core.management.base import BaseCommand
from django.db.models import Q

from authapp.models import User
from mainapp.models import Products, ProductCategories


class Command(BaseCommand):
    def handle(self, *args, **options):
        product = Products.objects.filter(
            Q(category__name='Обувь') | Q(id=18)
        )
        print('OR')
        print('\n'.join(list(map(str, product))))

        product = Products.objects.filter(
            Q(category__name='Обувь') & Q(id=55)
        )
        print('AND')
        print('\n'.join(list(map(str, product))))

        product = Products.objects.filter(
            ~Q(category__name='Обувь')
        )
        print('NOT')
        print('\n'.join(list(map(str, product))))