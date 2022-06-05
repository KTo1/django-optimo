from django.test import TestCase
from mainapp.models import Products, ProductCategories
from django.test.client import Client


class TestMainSmoke(TestCase):

    def setUp(self) -> None:
        category = ProductCategories.objects.create(name='Test')
        Products.objects.create(category=category, name='Product_1', price=100)
        self.client = Client()

    def test_product_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_product(self):
        for product_item in Products.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        pass


class ProductsTestCase(TestCase):

    def setUp(self):
        category = ProductCategories.objects.create(name="стулья")
        self.product_1 = Products.objects.create(name="стул 1", category=category, price=1999.5, quantity=150)
        self.product_2 = Products.objects.create(name="стул 2", category=category, price=2998.1, quantity=125, is_active=False)
        self.product_3 = Products.objects.create(name="стул 3", category=category, price=998.1, quantity=115)

    def test_product_get(self):

        product_1 = Products.objects.get(name="стул 1")
        product_2 = Products.objects.get(name="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):

        product_1 = Products.objects.get(name="стул 1")
        product_2 = Products.objects.get(name="стул 2")
        self.assertEqual(str(product_1), 'стул 1')
        self.assertEqual(str(product_2), 'стул 2')

    # def test_product_get_items(self):
    #
    #     product_1 = Products.objects.get(name="стул 1")
    #     product_3 = Products.objects.get(name="стул 3")
    #     products = product_1.get_items()
    #     self.assertEqual(list(products), [product_1, product_3])
