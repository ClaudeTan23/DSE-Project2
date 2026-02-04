from django.test import TestCase
from django.contrib.auth.models import User
from apps.home.models import Product, Stock

class StockTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Pen",
            sku="PEN001",
            category="Stationery",
            price=1.50,
            stock=10
        )

    def test_stock_in(self):
        self.product.stock += 5
        self.product.save()

        Stock.objects.create(
            product=self.product,
            quantity=5,
            location="Main",
            transaction_type="IN"
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 15)
        print(f"{self.__class__.__name__} Passed")
