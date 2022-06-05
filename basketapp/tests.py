from django.test import TestCase
from basketapp.models import Basket
from mainapp.models import Products, ProductCategories
from authapp.models import User

class BasketTestCase(TestCase):

    def setUp(self) -> None:
        category = ProductCategories.objects.create(name="столы")
        self.product = Products.objects.create(name="стол 1", category=category, price=1999.5, quantity=150)
        self.user = User.objects.create_user('test_user', 'test@e.mail', '1')
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=10)

    def test_basket_get(self):
        basket = Basket.objects.get(user=self.user)
        self.assertEqual(basket, self.basket)

    def test_basket_basket(self):
        basket = Basket.objects.filter(user=self.user).select_related('product')[0]
        self.assertEqual(self.basket, basket)

    def test_basket_sum(self):
        self.assertEqual(self.basket.sum(), self.basket.quantity * self.product.price)

    def tearDown(self) -> None:
        pass




